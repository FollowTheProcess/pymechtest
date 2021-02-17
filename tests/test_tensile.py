"""
Tests for the Tensile class.

Author: Tom Fleet
Created: 01/01/2021
"""


from pymechtest import Tensile


def test_tensile_init():

    obj = Tensile(
        folder="made/up/directory",
        header=8,
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert obj.folder == "made/up/directory"
    assert obj.header == 8
    assert obj.stress_col == "Tensile stress"
    assert obj.strain_col == "Tensile strain (Strain 1)"
    assert obj.id_row == 3
    assert obj.strain1 == 0.05
    assert obj.strain2 == 0.15
    assert obj.expect_yield is False


def test_tensile_repr():

    obj = Tensile(
        folder="made/up/directory",
        stress_col="Tensile stress",
        strain_col="Tensile strain (Strain 1)",
        id_row=3,
        header=8,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert (
        obj.__repr__() == "Tensile(folder='made/up/directory', "
        "id_row=3, "
        "stress_col='Tensile stress', "
        "strain_col='Tensile strain (Strain 1)', "
        "header=8, "
        "strain1=0.05, strain2=0.15, expect_yield=False)"
    )
