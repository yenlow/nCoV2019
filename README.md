# nCoV2019
1. Downloads line lists from [Google spreadsheet](https://docs.google.com/spreadsheets/d/1itaohdPiAeniCXNlntNztZ_oRvjh0HsGuJXUJWET008/edit#gid=0)
2. Sources R scripts to clean, preprocess and summarize data (from [beoutbreakprepared/nCoV2019](https://github.com/beoutbreakprepared/nCoV2019) 
and [jameshay218/case_to_infection](https://github.com/jameshay218/case_to_infection))
3. Alternatively, I've implemented that in Python to do #2 and identify determinants of death cases. 

As expected, risk factors are: 
- chronic illness
- being in Wuhan
- increasing age

# Acknowledgements
A big thanks to individuals and organizations who have shared their data, code, and ideas openly and timely. 
This repo draws from open repos [beoutbreakprepared/nCoV2019](https://github.com/beoutbreakprepared/nCoV2019) 
and [jameshay218/case_to_infection](https://github.com/jameshay218/case_to_infection)
who have kindly shared their R code to download, clean and summarize the data. 

These repos also have extensive analysis drawing from additional data sources (kudo, GIS) which I have excluded here.

Where possible, I tried to re-use their R code but also re-implemented them in Python to suit my needs


## Citation

To cite https://github.com/beoutbreakprepared/nCoV2019:

```{bibtex}
@misc{kraemer2020epidemiological,
  author =       {nCoV-2019 Data Working Group},
  title =        {{Epidemiological Data from the nCoV-2019 Outbreak: Early
                  Descriptions from Publicly Available Data}},
  howpublished = {Accessed on yyyy-mm-dd from
                  \url{http://virological.org/t/epidemiological-data-from-the-ncov-2019-outbreak-early-descriptions-from-publicly-available-data/337}},
  year =         2020
}
```
