"""
Base mechanical test class definition.

Author: Tom Fleet
Created: 09/12/2020
"""

import collections
import csv
import itertools
from pathlib import Path
from typing import Optional, Tuple, Union

import altair as alt
import altair_data_server  # noqa: F401
import numpy as np
import pandas as pd
from altair_saver import save


class BaseMechanicalTest:
    def __init__(
        self,
        folder: Union[Path, str],
        id_row: Optional[int] = None,
        stress_col: Optional[str] = None,
        strain_col: Optional[str] = None,
        header: int = 0,
        strain1: float = 0.05,
        strain2: float = 0.15,
        expect_yield: bool = True,
    ) -> None:
        """
        Base Mechanical test class.

        Args:
            folder (Union[Path, str]): String or Path-like folder containing
                test data.

            id_row (int, optional): Row number of the specimen ID.
                Most test machines export a headed csv file with some
                metadata like date, test method name etc. Specimen ID
                should be contained in this section. If not passed, pymechtest
                will use the filename as the specimen ID.

            stress_col (str, optional): Name of the column containing stress data.
                If not passed, pymechtest will try to autodetect it from your data.

            strain_col (str, optional): Name of the column containing strain data.
                If not passed, pymechtest will try to autodetect it from your data.

            header (int, optional): 0-indexed row number of the table header
                (i.e. the row containing things like "Stress", "Strain", "Load" etc.).
                Defaults to 0.

            strain1 (float, optional): Lower strain bound for modulus calculation.
                Must be in %. Defaults to 0.05.

            strain2 (float, optional): Upper strain bound for modulus calculation.
                Must be in %. Defaults to 0.15.

            expect_yield (bool, optional): Whether the specimens are expected to be
                elastic to failure (False) or they are expected to have a
                yield strength (True). Defaults to True.
        """
        self.folder = folder
        self.id_row = id_row
        self._stress_col = stress_col
        self._strain_col = strain_col
        self.header = header
        self.strain1 = strain1
        self.strain2 = strain2
        self.expect_yield = expect_yield

    def __repr__(self) -> str:

        return (
            self.__class__.__qualname__ + f"(folder={self.folder!r}, "
            f"id_row={self.id_row!r}, "
            f"stress_col={self._stress_col!r}, "
            f"strain_col={self._strain_col!r}, "
            f"header={self.header!r}, "
            f"strain1={self.strain1!r}, "
            f"strain2={self.strain2!r}, "
            f"expect_yield={self.expect_yield!r})"
        )

    def __eq__(self, other) -> bool:

        if other.__class__ is self.__class__:

            return (
                self.folder,
                self.id_row,
                self._stress_col,
                self._strain_col,
                self.header,
                self.strain1,
                self.strain2,
                self.expect_yield,
            ) == (
                other.folder,
                other.id_row,
                other._stress_col,
                other._strain_col,
                other.header,
                other.strain1,
                other.strain2,
                other.expect_yield,
            )
        return NotImplemented

    @property
    def stress_col(self) -> Union[str, None]:
        return self._stress_col

    @stress_col.setter
    def stress_col(self, value: str) -> None:
        self._stress_col = value

    @property
    def strain_col(self) -> Union[str, None]:
        return self._strain_col

    @strain_col.setter
    def strain_col(self, value: str) -> None:
        self._strain_col = value

    def _get_specimen_id(self, fp: Path) -> str:
        """
        Uses arg: self.id_row to grab the Specimen ID from a csv file.
        Only loads the row specified using itertools.islice for performance.

        If no id_row passed, will just grab the filename.

        Args:
            fp (Path): Individual specimen's data csv file.

        Raises:
            ValueError: If specimen ID not found in row specified.

        Returns:
            (str): Specimen ID.
        """

        if self.id_row is not None:
            # If user passes int for id_row

            with open(fp, "r") as f:
                spec_id = next(
                    itertools.islice(csv.reader(f), self.id_row, self.id_row + 1)
                )

            if spec_id is not None and len(spec_id) == 2:
                return spec_id[1]
            else:
                raise ValueError(f"Specimen ID in file: {str(fp)} not found!")
        else:
            # Nothing passed for id_row
            # Use filename instead
            return fp.name

    def _get_stress_strain_cols(self, df: pd.DataFrame) -> None:
        """
        Attempts to auto-detect the names of the stress and strain columns
        using a naive text match.

        If one is passed and the other not, this should only auto-detect the other.

        If none can be found, raises an exception and asks the user to specify.

        Args:
            df (pd.DataFrame): DataFrame from which to detect the column names.

        Raises:
            ValueError: If no match for "stress" or "strain" found.
        """

        if not self.stress_col:
            for col in df.columns.tolist():
                if "stress" in col.strip().lower():
                    self.stress_col = col
        if not self.strain_col:
            for col in df.columns.tolist():
                if "strain" in col.strip().lower():
                    self.strain_col = col
        else:
            pass

        # Now that's been done, neither should be None
        # If either are still None, it means detection failed

        if self.stress_col is None:
            raise ValueError("Could not detect stress_col.")
        elif self.strain_col is None:
            raise ValueError("Could not detect strain_col.")

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

        # Attempt to detect stress/strain columns
        self._get_stress_strain_cols(df)

        return df

    def _calc_slope(self, df: pd.DataFrame) -> Tuple[float, float]:
        """
        Calculates the slope and the intercept of the linear portion
        of the stress-strain curve.

        Uses numpy to calculate the slope and intercept
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

        Note: stress must be in MPa and strain must be in % for this to work.

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
        save_method: Optional[str] = "selenium",
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
                Defaults to "{class_name} Stress-Strain Curves".

            save_path (Union[str, Path], optional): str or Pathlike path to save
                a png of the plot. Requires chrome and selenium. If not passed, plot
                is simply returned and not saved.

            save_method (str, optional): One of 2 altair save methods:
                'selenium' or 'node'.
                if 'selenium' requires a configured geckodriver or chromedriver on PATH.
                if 'node' requires nodejs installation. Defaults to 'selenium'

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

        if save_method not in set(["selenium", "node"]):
            raise ValueError(
                f"Save method must be one of 'selenium' or 'node'. Got: {save_method}"
            )

        if save_path:
            fp = Path(save_path).resolve()
            save(
                chart,
                fp=str(fp),
                scale_factor=6.0,
                method=save_method,
            )

        return chart
