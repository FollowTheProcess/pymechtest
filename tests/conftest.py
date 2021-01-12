"""
Fixtures and other test configuration.

Author: Tom Fleet
Created: 31/12/2020
"""

from pathlib import Path

import pytest

from pymechtest.base import BaseMechanicalTest


@pytest.fixture
def base_long():
    """
    Equivalent to calling BaseMechanicalTest pointing at the
    longitudinal test data.

    Stress and strain col refer to Tensile because
    the data I'm using for testing is from a static tensile test.
    """

    return BaseMechanicalTest(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Tens_No_Yield"),
        header=8,
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )


@pytest.fixture
def base_long_no_id():
    """
    Same as base long but without specifying an ID row.
    """

    return BaseMechanicalTest(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Tens_No_Yield"),
        header=8,
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )


@pytest.fixture
def base_trans():
    """
    Equivalent to calling BaseMechanicalTest pointing at the
    transverse test data.

    Stress and strain col refer to Tensile because
    the data I'm using for testing is from a static tensile test.
    """

    return BaseMechanicalTest(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Tens_Yield"),
        header=8,
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        id_row=3,
        strain1=0.005,
        strain2=0.015,
        expect_yield=True,
    )


@pytest.fixture
def base_long_no_stress_strain_cols():
    """
    Like above but not specifying stress and strain col
    names to test the auto-detection.
    """

    return BaseMechanicalTest(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Tens_No_Yield"),
        header=8,
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )


@pytest.fixture
def base_trans_no_stress_strain_cols():
    """
    Like above but not specifying stress and strain col
    names to test the auto-detection.
    """

    return BaseMechanicalTest(
        folder=Path(__file__).parents[1].resolve().joinpath("tests/data/Tens_Yield"),
        header=8,
        id_row=3,
        strain1=0.005,
        strain2=0.015,
        expect_yield=True,
    )
