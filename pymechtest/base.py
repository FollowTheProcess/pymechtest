"""
Base mechanical test class definition.

Author: Tom Fleet
Created: 09/12/2020
"""

import collections
import csv
import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple, Union

import altair as alt
import altair_data_server  # noqa: F401
import numpy as np
import pandas as pd
from altair_saver import save


@dataclass
class BaseMechanicalTest:
    """
    Mechanical Test Base class.

    Args:
        folder (Union[Path, str]): String or Path-like folder containing
            test data.

        stress_col (str): Name of the column containing stress data.

        strain_col (str): Name of the column containing strain data.

        id_row (int): Row number of the specimen ID. Most test machines export a
            headed csv file with some metadata like date, test method name etc,
            specimen ID should be contained in this section.

        header (int, optiona;): 0-indexed row number of the table header
            (i.e. the row containing things like "Stress", "Strain", "Load" etc.).
            Defaults to 0.

        strain1 (float, optional): Lower strain bound for modulus calculation.
            Must be in %. Defaults to 0.05.

        strain2 (float, optional): Upper strain bound for modulus calculation.
            Must be in %. Defaults to 0.05.

        expect_yield (bool, optiona;): Whether the specimens are expected to be
        elastic to failure (False) or they are expected to have a
        yield strength (True). Defaults to True.
    """

    folder: Union[Path, str]
    stress_col: str
    strain_col: str
    id_row: int
    header: int
    strain1: float = 0.05
    strain2: float = 0.15
    expect_yield: bool = True

    def _get_specimen_id(self, fp: Union[Path, str]) -> str:
        """
        Uses arg: self.id_row to grab the Specimen ID from a csv file.
        Only loads the row specified using itertools.islice for performance.

        Args:
            fp (Union[Path, str]): Individual specimen's data csv file.

        Raises:
            ValueError: If specimen ID not found in row specified.

        Returns:
            (str): Specimen ID.
        """

        with open(fp, "r") as f:
            spec_id = next(
                itertools.islice(csv.reader(f), self.id_row, self.id_row + 1)
            )

        if spec_id is not None and len(spec_id) == 2:
            return spec_id[1]
        else:
            raise ValueError(f"Specimen ID in file: {str(fp)} not found!")

    def _load(self, fp: Path) -> pd.DataFrame:
        """
        Method to load individual data csv file into a pandas DataFrame.

        Args:
            fp (Path): csv file to load. Exclusively pathlib.Path as files
                are discovered with an rglob in load_all.

        Returns:
            pd.DataFrame: DataFrame containing single sample's data.
        """
        # Incase there are any non-numerics below header
        df = (
            (pd.read_csv(fp, header=self.header))
            .applymap(lambda x: x.strip().replace(",", "") if isinstance(x, str) else x)
            .apply(pd.to_numeric, errors="coerce")
            .dropna(how="all")
        )
        df["Specimen ID"] = self._get_specimen_id(fp)

        return df

    def _calc_slope(self, df: pd.DataFrame) -> Tuple[float, float]:
        """
        Calculates the slope and the intercept of the linear portion
        of the stress-strain curve.

        Uses numpy to rapidly calculate the slope and intercept
        from a single specimen's data using strain1 and strain2
        as the upper and lower limits.

        Args:
            df (pd.DataFrame): DataFrame for the specimen.

        Returns:
            Tuple[float, float]: slope, intercept.
        """
        # Grab stress and strain data between strain1 and strain2
        # Elastic portion of the stress-strain curve
        mod_filt = (df[self.strain_col] >= self.strain1) & (
            df[self.strain_col] <= self.strain2
        )

        mod_df = df[mod_filt][[self.strain_col, self.stress_col]]

        # A is here to convert x to a matrix so numpy can be used
        x = np.array(mod_df[self.strain_col])
        y = np.array(mod_df[self.stress_col])

        A = np.vstack([x, np.ones(len(x))]).T

        # As in y = mx + c
        slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]

        return slope, intercept

    def _calc_modulus(self, df: pd.DataFrame) -> float:
        """
        Uses the calc slope method to get elastic modulus in GPa.

        Args:
            df (pd.DataFrame): Input df passed to _calc_slope.

        Returns:
            float: Elastic Modulus in GPa.
        """
        # If stress is MPa and strain is in % this will always work
        return 0.1 * self._calc_slope(df)[0]

    def _calc_yield(self, df: pd.DataFrame, offset: float = 0.2) -> float:
        """
        Calculates the % offset yield strength for a specimen who's data is contained
        in 'df'.

        Args:
            df (pd.DataFrame): DataFrame containing single specimens' data.

            offset (float, optional): Strain offset to apply (%). Defaults to 0.2.

        Returns:
            float: Offset yield strength in MPa
        """

        if not self.expect_yield:
            raise AttributeError(
                f"""Cannot calculate yield strength when expect_yield is False.
                expect_yield = {self.expect_yield}"""
            )

        slope, intercept = self._calc_slope(df)

        # Avoids pandas view/copy warning
        offset_df = df.copy()

        # Apply the offset to determine offset stress at each row
        # Offset stress vs strain is straight line of gradient = modulus
        # Yield is where this line intersects the original curve
        offset_df["offset_stress"] = slope * (df[self.strain_col] - offset) + intercept

        # Diff between offset stress and actual
        # Intersect is where this is = 0
        offset_df["offset_delta"] = (
            offset_df["offset_stress"] - offset_df[self.stress_col]
        )

        # Find actual stress value of the intersect
        yield_index = offset_df["offset_delta"].abs().idxmin()

        yield_strength = offset_df.iloc[yield_index][self.stress_col]

        return yield_strength

    def _extract_values(self, df: pd.DataFrame) -> pd.Series:
        """
        Extracts key test values from a specimens' data.

        Uses a pd.Series to make summarising in a dataframe later
        much easier.

        Args:
            df (pd.DataFrame): Specimens' data

        Returns:
            pd.Series: Series of key test values.
        """

        cols = ["Specimen ID", "Strength", "Modulus"]

        # Only one specimen in df here so specimen ID is constant for each
        spec_id = df["Specimen ID"].iloc[0]
        uts = df[self.stress_col].max()
        modulus = self._calc_modulus(df)

        vals = [spec_id, uts, modulus]

        if self.expect_yield:
            cols.append("Yield Strength")
            yield_strength = self._calc_yield(df)

            vals.append(yield_strength)

        data_dict = collections.OrderedDict(
            {col: val for (col, val) in zip(cols, vals)}
        )

        return pd.Series(data=data_dict)

    def load_all(self) -> pd.DataFrame:
        """
        Loads all the found files in 'folder' into a dataframe.

        Recursively searches 'folder' for all csv files, grabs the specimen identifier
        specified during 'id_row' and includes this in the dataframe.

        Returns:
            pd.DataFrame: All found test data with specimen identifier.
        """

        # Cast to Path so can glob even if user passed str
        fp = Path(self.folder).resolve()

        df = (
            (pd.concat([self._load(f) for f in sorted(fp.rglob("*.csv"))]))
            .assign(spec_id=lambda x: pd.Categorical(x["Specimen ID"]))
            .drop(columns=["Specimen ID"])
            .rename(columns={"spec_id": "Specimen ID"})
        )

        # Reorder the columns for OCD reasons
        col = df.pop("Specimen ID")
        df.insert(0, "Specimen ID", col)

        # So we can avoid having to load data repeatedly
        self._loaded_all = True
        self._df = df

        return df

    def summarise(self) -> pd.DataFrame:
        """
        High level summary method, generates a dataframe containing key
        test values such as UTS, Modulus etc. for all the data in the
        target folder.

        Returns:
            pd.DataFrame: Dataframe containing test summary values for each
                specimen.
        """

        fp = Path(self.folder).resolve()

        rows = [
            self._extract_values(df)
            for df in [self._load(f) for f in sorted(fp.rglob("*.csv"))]
        ]

        # .T transposes to that it's the expected dataframe format
        return (pd.concat(rows, axis=1, ignore_index=True).T).convert_dtypes()

    def stats(self) -> pd.DataFrame:
        """
        Returns a table of summary statistics e.g. mean, std, cov etc.
        for the data in folder.

        Uses pandas df.describe() to do the bulk of the work, just adds in
        cov for good measure.

        Returns:
            pd.DataFrame: Summary statistics.
        """

        df = self.summarise().describe()

        df.loc["cov%"] = df.loc["std"] / df.loc["mean"] * 100

        # Reorganise so cov is close to std
        new_index = ["count", "mean", "std", "cov%", "min", "25%", "50%", "75%", "max"]
        df = df.reindex(new_index)

        return df

    def plot_curves(
        self,
        title: Optional[str] = None,
        save_path: Optional[Union[str, Path]] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        height: int = 500,
        width: int = 750,
    ) -> alt.Chart:
        """
        Creates a nice looking stress strain plot of all the specimens using altair.

        Will use the class name to fill in axis labels if not passed, e.g
        'Tensile' Strain

        Args:
            title (str, optional): Title for the plot.
                Defaults to "Stress-Strain Curves".

            save_path (Union[str, Path], optional): str or Pathlike path to save
                a png of the plot. Requires chrome and selenium. If not passed, plot
                is simply returned and not saved.

            x_label (str, optional): Label for x-axis.
                Defaults to "{class name}Strain (%)".

            y_label (str, optional): Label for y-axis.
                Defaults to "{class name}Stress (MPa)".

            height (int, optional): Height of the plot.
                Defaults to 500.

            width (int, optional): Width of the plot.
                Defaults to 750.

        Returns:
            alt.Chart: Stress strain plot.
        """

        # Altair will warn if over 5,000 rows in a notebook. This is cleanest solution.
        alt.data_transformers.enable("data_server")

        if not x_label:
            x_label = f"{self.__class__.__qualname__} Strain (%)"

        if not y_label:
            y_label = f"{self.__class__.__qualname__} Stress (MPa)"

        if not title:
            title = f"{self.__class__.__qualname__} Stress Strain Curves"

        df = self.load_all()

        chart = (
            alt.Chart(data=df)
            .mark_line(size=1)
            .encode(
                x=alt.X(f"{self.strain_col}:Q", title=x_label),
                y=alt.Y(f"{self.stress_col}:Q", title=y_label),
                color=alt.Color("Specimen ID:N", title="Specimen ID"),
            )
            .properties(title=title, height=height, width=width)
        )

        if save_path:
            fp = Path(save_path).resolve()
            save(
                chart,
                fp=str(fp),
                fmt="png",
                scale_factor=6.0,
                method="selenium",
                webdriver="chrome",
            )

        return chart
