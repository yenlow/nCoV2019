# About
Many scientists have come together to share their data, code and ideas openly and timely to fight the COVID-19 epidemic. 
Here I've gathered and incorporated snippets from several publications and repos (see [Acknowledgments](https://github.com/yenlow/nCoV2019/wiki/Acknowledgements)) and also experimented with methods inspired by their work or other related fields (e.g. Social Network Analysis, gene expression networks, compartmental modeling).

# What this repo does (so far)
1. Downloads line lists from [Google spreadsheet](https://docs.google.com/spreadsheets/d/1itaohdPiAeniCXNlntNztZ_oRvjh0HsGuJXUJWET008/edit#gid=0)
2. Sources R scripts to clean, preprocess and summarize data (from [beoutbreakprepared/nCoV2019](https://github.com/beoutbreakprepared/nCoV2019) 
and [jameshay218/case_to_infection](https://github.com/jameshay218/case_to_infection))
3. Where possible, I tried to re-use their R code but also re-implemented them in Python to suit my needs and identify determinants of death cases. 

As expected, risk factors are: 
- chronic illness
- being in Wuhan
- increasing age

# Other ideas to try (not done here)
Epidemiology has always thrived on big data. Even back in the 1840s, [John Snow](https://en.wikipedia.org/wiki/John_Snow), the father of Epidemiology, cleverly collected addresses from the local water utility provider and created the first outbreak dot map which located the Cholera epicenter to be the water pump on Broad St in London.

Today, we have even more data and methods available. This [figure](http://doi.org/10.1098/rstb.2018.0276) is a good way to see how they may all come together. With advances in deep sequential models, graph networks, stochastic agent-based modeling, etc, we can get really inventive!
![Outbreak epidemiology methods](https://royalsocietypublishing.org/cms/asset/7a1b3117-3a4c-4fda-a837-720ded4f8a84/rstb20180276f02.jpg)

## What scientists know so far:
1. **Reproductive number** (*R0*)**:** 2.2 [95% CI: 1.4 - 3.9] (Li et al. *NEJM* [doi:10.1056/NEJMoa2001316](https://www.nejm.org/doi/full/10.1056/NEJMoa2001316))
2. **Incubation period:** mean 5 days [95% CI: 4 - 7 days], 95% percentile: 12.5 days, max(rare!): 21 days (Li et al. *NEJM* [doi:10.1056/NEJMoa2001316](https://www.nejm.org/doi/full/10.1056/NEJMoa2001316))
3. **Mortality rate:**
4. **Recovery rate:**

## Data and code suggestions
If you chance upon good papers and code for corroborating data and methods, pls suggest so in [Issues](https://github.com/yenlow/nCoV2019/issues/new) or [Wiki](https://github.com/yenlow/nCoV2019/wiki/Home)
- Social media data
- Traffic patterns
- Health utilization data
