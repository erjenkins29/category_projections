# category_projections

This repository is for the postprocess applied to predictions of q30.  It is being treated as a separate project for now, as it is uncertain at this point how we integrate into the current prediction framework.  Additionally, there are a few customer requests for category size which fall outside the scope of JD (for which our q30 predictions currently only are modeled for).  This project allows for category size estimates without the need for the very advanced, and likely heavily JD-biased, q30 prediction algorithm currently employed by Early Data.

### Simple use

To load 50 categories of data into a list of dataframes, do the following:

import cat100xxxxx as catread
dfs = catread.get50Categories(ref\_date\_i=2) ## where i is an integer from 0 to 5, representing a month from 201605 to 201610


To generate a prediction using method 1, 2, 3 or 4....

import plotcategories as pcat
pcat.plotConfidence(dfs[11], method=4, std=.015) ## replace the number 11 with any integer from 0 to 49