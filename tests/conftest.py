"""
Fixtures and other test configuration.

Author: Tom Fleet
Created: 31/12/2020
"""

from pathlib import Path

import pytest

from pymechtest import Tensile


@pytest.fixture
def tensile_long():
    """
    Equivalent to calling Tensile pointing at the
    longitudinal test data.
    """

    return Tensile(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Long"),
        header=8,
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )


@pytest.fixture
def tensile_trans():
    """
    Equivalent to calling Tensile pointing at the
    transverse test data.
    """

    return Tensile(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Trans"),
        header=8,
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        id_row=3,
        strain1=0.005,
        strain2=0.015,
        expect_yield=True,
    )
