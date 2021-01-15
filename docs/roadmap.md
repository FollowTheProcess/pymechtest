# Roadmap

Like every project, it's never truly finished! Here are some of the things I want to implement, change or add in future releases.

If you think you can help make some of these things happen, thats great! See the [contributing] guide on how to get involved!

## Improve Column Autodetection

Currently pymechtest naively searches for data columns with the words "stress" or "strain" in them and that's how it determines which column is which. This is currently implemented in a bit of a hacky way.

I'm sure there must be a more sophisticated method of determining which column is which than simply doing a string search

## Unit Conversion

Currently, pymechtest assumes SI units for everything. In 90% of cases this is likely to be true as test machines (especially modern ones) are fairly well standardised.

However, in the future it would be good if the user could pass something like `stress_units = 'kPa'` for example. Or better yet, to autodetect what the units are! and all the conversion would be handled under the hood.

## Alternative Calculation Methods

The default calculation for modulus and yield strength are currently "Elastic Modulus" and "0.2% offset yield" respectively. These are probably the most common calculations to perform and what 90% of people want.

It would be good though to have a range of different calculations available like "chord modulus" or "slope threshold yield" etc. that the user could choose from in an argument like `yield_method = "slope threshold"` for example.

## Support Dynamic Test Data

Aside from static tests, it's common for engineers to perform 'dynamic' tests where the specimen is loaded cyclically (fatigue) or the load is held for a great deal of time (creep) and the strain of the specimen is monitored. It would be good to support this here!

I have limited data on cyclic tests currently so if you're reading this and you have some you don't mind sharing please get in touch! See the [contributing] page for info.

It would also be good to hear from engineers more experienced in these tests to get an idea of the kinds of analysis they do and what would be good candidates for automation using pymechtest!

## CLI

I'd like to add a CLI at some point so that pymechtest (or maybe just a subset of it's capabilities) can be invoked from the command line in a flash!
Who knows, maybe even a GUI at some point!? :bar_chart:

## More

There's probably loads more improvements that could be made! Full disclosure: this is my first python package ever :eyes:

I'm sure there's lots of work to do!

Check out the [contributing] page and the [full guide] on how to do it!

[contributing]: contributing/help.md
[full guide]: contributing/guide.md
