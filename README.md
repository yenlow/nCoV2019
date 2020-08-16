# Latest Updates:
See risk factors analyzed from one of the largest studies, OpenSafely, studying 17 million UK adults
```
Williamson, E.J., Walker, A.J., Bhaskaran, K. et al. 
Factors associated with COVID-19-related death using OpenSAFELY. 
Nature (2020). https://doi.org/10.1038/s41586-020-2521-4
```

# About
Many scientists have come together to share their data, code and ideas openly and timely to fight the COVID-19 epidemic ([news link](https://qz.com/1795103/coronavirus-is-a-proving-ground-for-scientific-transparency/), [free Alibaba cloud services](https://blog.deeplearning.ai/blog/the-batch-hotter-dating-profiles-pandas-in-love-compute-for-coronavirus-deepfake-detection-self-driving-cars-run-amok))
Here I've gathered and incorporated snippets from several publications and repos (see [Acknowledgments](https://github.com/yenlow/nCoV2019/wiki/Acknowledgements)) and also experimented with methods inspired by their work or other related fields (e.g. Social Network Analysis, gene expression networks, compartmental modeling).

# Join our Workgroup
We are based in SF Bay but collaborate remotely to solve this public health crisis. We come from diverse backgrounds ranging from Epidemiology, Public Health, Cheminformatics, Astrophysics, Mechanical Engineering.
- **Github:** https://github.com/yenlow/nCoV2019
- **Slack channel:** [coronavirus2020.slack.com](https://app.slack.com/client/TT3PHCRFG/CSRBY0Y9X)
- **[Google shared drive](https://drive.google.com/drive/folders/1K8UVAS1KKkukU-WlcUYVeeI7DsXXoGU_?usp=sharing)** 

Contact [Yen Low](https://www.linkedin.com/in/yenlow/) to join or [contribute](https://github.com/yenlow/nCoV2019/wiki/Data-and-code-suggestions) code and ideas here in the [Wiki](https://github.com/yenlow/nCoV2019/wiki/Data-and-code-suggestions) or [Issues](https://github.com/yenlow/nCoV2019/issues)!

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

# Read more
- [What scientists have found](https://github.com/yenlow/nCoV2019/wiki/What-scientists-know-so-far)
- [Contribute](https://github.com/yenlow/nCoV2019/wiki/Data-and-code-suggestions) code and ideas!
- [Scientific transparency news link, 1st Feb, 2020](https://qz.com/1795103/coronavirus-is-a-proving-ground-for-scientific-transparency/)
- [Scientific American, 13 Feb 2020](https://www.scientificamerican.com/article/heres-how-computer-models-simulate-the-future-spread-of-new-coronavirus)
