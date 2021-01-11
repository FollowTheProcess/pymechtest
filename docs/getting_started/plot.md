# Plot Curves

Probably the most important thing to do when analysing mechanical test data is to plot stress-strain curves for the batch so you can compare. pymechtest uses [altair] makes it super easy to plot really nice looking stress-strain curves by default.

The pymechtest plot style is very opinionated, the plots will come out looking the same every time and the API exposes very little in the way of customisation. If you want full control over how you want the plots to look, you might want to just do it manually by loading the data in with `.load_all()` and then using whatever plotting tool you like.

[altair]: https://altair-viz.github.io

Every static test method currently supported in pymechtest has a `.plot_curves()` method. Lets take a look at it...

## `plot_curves`

::: pymechtest.base.BaseMechanicalTest.plot_curves

## Making your plot

In 90% of the cases, you will probably just need to call `plot_curves()` with no arguments. Again, following the principle of **sensible defaults**, pymechtest will fill out a lot of the information for you.

For instance, if you're calling `plot_curves()` from an instance of the `Tensile` class, the title will be "Tensile Stress Strain Curves" and the axes titles will be "Tensile Stress" and "Tensile Strain".
