"""
Tests for the Flexure class.

Author: Tom Fleet
Created: 01/01/2021
"""


from pymechtest import Flexure


def test_flexure_init():

    obj = Flexure(
        folder="made/up/directory",
        header=8,
        stress_col="Flexure stress",
        strain_col="Flexure strain (Strain 1)",
        id_row=3,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert obj.folder == "made/up/directory"
    assert obj.header == 8
    assert obj.stress_col == "Flexure stress"
    assert obj.strain_col == "Flexure strain (Strain 1)"
    assert obj.id_row == 3
    assert obj.strain1 == 0.05
    assert obj.strain2 == 0.15
    assert obj.expect_yield is False


def test_flexure_repr():

    obj = Flexure(
        folder="made/up/directory",
        stress_col="Flexure stress",
        strain_col="Flexure strain (Strain 1)",
        id_row=3,
        header=8,
        strain1=0.05,
        strain2=0.15,
        expect_yield=False,
    )

    assert (
        obj.__repr__() == "Flexure(folder='made/up/directory', "
        "id_row=3, "
        "stress_col='Flexure stress', "
        "strain_col='Flexure strain (Strain 1)', "
        "header=8, "
        "strain1=0.05, strain2=0.15, expect_yield=False)"
    )
