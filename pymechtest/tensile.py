"""
Core Tensile class definition.

Author: Tom Fleet
Created: 29/11/2020
"""

from __future__ import annotations

import csv
import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

import numpy as np
import pandas as pd

# Data for testing & development only
LONG_DATA = Path(__file__).parents[1].resolve().joinpath("data/Long")
TRANS_DATA = Path(__file__).parents[1].resolve().joinpath("data/Trans")

LONG_FILE = [f for f in LONG_DATA.rglob("*.csv")][0]
TRANS_FILE = [f for f in TRANS_DATA.rglob("*.csv")][0]


@dataclass
class Tensile:
    """
    Base Tensile data class representing a group of data from Tensile tests.

    Args:
        folder (Union[Path, str]): String or 'pathlike' folder containing the data csv files.

        stress_col (str): Name of the column containing stress data. Must be in MPa.

        strain_col (str): Name of the column containing strain data. Must be in %.

        id_row (int): Row number of the specimen ID. Most test machines export a headed csv
            file with some metadata like date, test method name etc, specimen ID should be
            contained in this section.

            Pass the row number of the line containing this information.

        skip_rows (Union[int, List[int]]): Rows to skip during loading of the csv file.
            Typically there is some metadata at the top, skip this and load only the data
            by passing skip_rows.

            Follows pandas skiprows syntax so can be an integer or a list of integers.

            Don't worry about conflict between skipping rows and the id_row, grabbing the
            specimen ID is handled seperately.

        strain1 (float): Lower strain bound for modulus calculation. Must be in %.

        strain2 (float): Upper strain bound for modulus calculation. Must be in %.

        expect_yield (bool): Whether the specimens are expected to be elastic to failure (False)
            or they are expected to have a yield strength (True).
    """

    folder: Union[Path, str]
    stress_col: str
    strain_col: str
    id_row: int
    skip_rows: Union[int, List[int]]
    strain1: float
    strain2: float
    expect_yield: bool

    @classmethod
    def _test_long(cls) -> Tensile:
        """
        Development method to make life easier.

        Returns:
            Tensile: Tensile object: longitudinal
        """
        return Tensile(
            folder=LONG_DATA,
            stress_col="Tensile stress",
            strain_col="Tensile strain (Strain 1)",
            id_row=3,
            skip_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
            strain1=0.05,
            strain2=0.15,
            expect_yield=False,
        )

    @classmethod
    def _test_trans(cls) -> Tensile:
        """
        Development method to make life easier.

        Returns:
            Tensile: Tensile object: transverse
        """
        return Tensile(
            folder=TRANS_DATA,
            stress_col="Tensile stress",
            strain_col="Tensile strain (Strain 1)",
            id_row=3,
            skip_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
            strain1=0.005,
            strain2=0.015,
            expect_yield=True,
        )

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
            fp (Path): csv file to load.

        Returns:
            pd.DataFrame: DataFrame containing single sample's data.
        """

        df = pd.read_csv(fp, skiprows=self.skip_rows, thousands=",")
        df["Specimen ID"] = self._get_specimen_id(fp)

        # Reorder the column for OCD reasons
        col = df.pop("Specimen ID")
        df.insert(0, "Specimen ID", col)

        return df

    def _calc_modulus(self, df: pd.DataFrame) -> float:
        """
        Modulus calculation method. Uses numpy to rapidly calculate the elastic modulus
        from a single specimen's data using strain1 and strain2 as the upper and lower limits.

        Args:
            df (pd.DataFrame): DataFrame for the specimen.

        Returns:
            float: Elastic modulus (in GPa).
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
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]

        # If stress is in MPa and strain is in % this will always work
        modulus = 0.1 * m

        return modulus

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

        df = pd.concat([self._load(f) for f in fp.rglob("*.csv")])

        # Cast to categorical for memory saving
        df["Specimen ID"] = df["Specimen ID"].astype("category")

        return df
