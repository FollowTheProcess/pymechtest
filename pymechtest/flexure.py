"""
Flexure class definition.

Author: Tom Fleet
Created: 31/12/20
"""

from pathlib import Path
from typing import List, Union

from pymechtest.base import BaseMechanicalTest


class Flexure(BaseMechanicalTest):
    def __init__(
        self,
        folder: Union[Path, str],
        stress_col: str,
        strain_col: str,
        id_row: int,
        skip_rows: Union[int, List[int]],
        strain1: float,
        strain2: float,
        expect_yield: bool,
    ) -> None:
        """
        Flexure data class representing a group of data from Flexure tests.

        Args:
            folder (Union[Path, str]): String or Path-like folder containing Flexure
                test data.

            stress_col (str): Name of the column containing stress data.

            strain_col (str): Name of the column containing strain data.

            id_row (int): Row number of the specimen ID. Most test machines export a
                headed csv file with some metadata like date, test method name etc,
                specimen ID should be contained in this section.

            skip_rows (Union[int, List[int]]): Rows to skip during loading of the csv.
                Typically there is some metadata at the top, skip this and load
                only the data by passing skip_rows.

                Follows pandas skiprows syntax so can be an integer or a list
                of integers.

                Don't worry about conflict between skipping rows and the id_row,
                grabbing the specimen ID is handled seperately.

            strain1 (float): Lower strain bound for modulus calculation. Must be in %.

            strain2 (float): Upper strain bound for modulus calculation. Must be in %.

            expect_yield (bool): Whether the specimens are expected to be elastic to
                failure (False) or they are expected to have a yield strength (True).
        """

        super().__init__(
            folder=folder,
            stress_col=stress_col,
            strain_col=strain_col,
            id_row=id_row,
            skip_rows=skip_rows,
            strain1=strain1,
            strain2=strain2,
            expect_yield=expect_yield,
        )
