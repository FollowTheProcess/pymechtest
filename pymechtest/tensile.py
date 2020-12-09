"""
Tensile class definition.

Author: Tom Fleet
Created: 29/11/2020
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Union

import altair as alt
import altair_data_server

from pymechtest.base import BaseMechanicalTest


class Tensile(BaseMechanicalTest):
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
        Tensile data class representing a group of data from Tensile tests.

        Args:
            folder (Union[Path, str]): String or Path-like folder containing Tensile
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
            folder,
            stress_col,
            strain_col,
            id_row,
            skip_rows,
            strain1,
            strain2,
            expect_yield,
        )

    def __repr__(self) -> str:
        return super().__repr__()

    def __eq__(self, other) -> bool:
        if other.__class__ is self.__class__:

            return (
                self.folder,
                self.stress_col,
                self.strain_col,
                self.id_row,
                self.skip_rows,
                self.strain1,
                self.strain2,
                self.expect_yield,
            ) == (
                other.folder,
                other.stress_col,
                other.strain_col,
                other.id_row,
                other.skip_rows,
                other.strain1,
                other.strain2,
                other.expect_yield,
            )
        return NotImplemented

    @classmethod
    def _test_long(cls) -> Tensile:
        """
        Development method to make life easier.

        Returns:
            Tensile: Tensile object: longitudinal
        """
        return Tensile(
            folder=Path(__file__).parents[1].resolve().joinpath("data/Long"),
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
            folder=Path(__file__).parents[1].resolve().joinpath("data/Trans"),
            stress_col="Tensile stress",
            strain_col="Tensile strain (Strain 1)",
            id_row=3,
            skip_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
            strain1=0.005,
            strain2=0.015,
            expect_yield=True,
        )

    def plot_curves(
        self,
        title: str = "Tensile Stress-Strain Curves",
        height: int = 500,
        width: int = 750,
    ) -> alt.Chart:
        """
        Generates a nice looking stress-strain plot for every specimen in your sample.

        Uses Altair in the backend so any plot can be easily exported as png, svg etc.
        Or hosted on a web page if you're really fancy!

        Args:
            title (str, optional): Title for the plot.
                Defaults to "Stress-Strain Curves".
            height (int, optional): Height of the plot. Defaults to 500.
            width (int, optional): Width of the plot. Defaults to 750.

        Returns:
            alt.Chart: Stress-strain plot.
        """
        # Altair will warn if over 5,000 rows. This is cleanest solution.
        alt.data_transformers.enable("data_server")

        df = self.load_all()

        chart = (
            alt.Chart(data=df, title=title, height=height, width=width)
            .mark_line(size=1)
            .encode(
                x=alt.X(f"{self.strain_col}:Q", title="Tensile Strain (%)"),
                y=alt.Y(f"{self.stress_col}:Q", title="Tensile Stress (MPa)"),
                color=alt.Color("Specimen ID:N", title="Specimen ID"),
            )
        )

        return chart
