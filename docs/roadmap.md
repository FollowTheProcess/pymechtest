# Roadmap

Like every project, it's never truly finished! Here are some of the things I want to implement, change or add in future releases.

If you think you can help make some of these things happen, thats great! See the [contributing] guide on how to get involved!

## Improve Column Autodetection

Currently pymechtest naively searches for data columns with the words "stress" or "strain" in them and that's how it determines which column is which. This is currently implemented in a bit of a hacky way.

There are a few potential improvements here:

* Firstly, I'm sure there must be a more sophisticated method of determining which column is which than simply doing a string search
* This implementation is called in every method that requires loading in data. This is fine for now but if the project grows, this will become a "code smell". I tried initially to get it to work using the `@property` decorator for `self.stress_col` and `self.strain_col` but I had no joy getting it to work reliably. Someone with more python experience might be able to solve this one easily!

## Unit Conversion

Currently, pymechtest assumes SI units for everything. In 90% of cases this is likely to be true as test machines (especially modern ones) are fairly well standardised.

However, in the future it would be good if the user could pass something like `stress_units = 'kPa'` for example. Or better yet, to autodetect what the units are! and all the conversion would be handled under the hood.

## Alternative Calculation Methods

The default calculation for modulus and yield strength are currently "Elastic Modulus" and "0.2% offset yield" respectively. These are probably the most common calculations to perform and what 90% of people want.

It would be good though to have a range of different calculations available like "chord modulus" or "slope threshold yield" etc. that the user could choose from in an argument like `yield_method = "slope threshold"` for example.

## More

There's probably loads more improvements that could be made! Full disclosure: this is my first python package ever :eyes:

I'm sure there's lots of work to do!

Check out the [contributing] page and the [full guide] on how to do it!

[contributing]: contributing/help.md
[full guide]: contributing/guide.md
