# Title : get_clean_data.R
# Objective :
# 1. Download line list from google spreadsheet
# 2. Clean dates and saves to combine_dat.feather
# 3. Plots delays and counts
# 3. de-dupes
# (#1-3 sources https://github.com/jameshay218/case_to_infection/blob/master/code/pull_and_clean_linelist.R)
# Created by: yensia-low
# Created on: 2/7/20
getwd()

require(dplyr)
require(tidyverse)
require(feather)
source("src/utils.R")

# download supporting files from https://github.com/jameshay218/case_to_infection
# see get_scripts.py
source("other_authors/analysis_functions.R")
source("other_authors/date_functions.R")          #stores prev confounding_dates
source("other_authors/augmentation_functions.R")

# common columns between the 2 google sheets
cols_all = c('ID','age','sex',
'city','province','country','wuhan(0)_not_wuhan(1)','latitude','longitude','geo_resolution',
'date_onset_symptoms','date_admission_hospital','date_confirmation',
'symptoms','lives_in_Wuhan','travel_history_dates','travel_history_location',
'reported_market_exposure','additional_information','chronic_disease_binary','chronic_disease',
'source','sequence_available','outcome','date_death_or_discharge','notes_for_discussion',
'location','admin3','admin2','admin1','country_new','admin_id')

#  get cols_to_match set for de_dupe_linelist.R
# sourcePartial("other_authors/de_dupe_linelist.R",
#               startTag='^cols_to_match', endTag='^cols_to_match')
cols_to_match = cols_all
print("cols_to_match: ")
print(cols_to_match)

# source key_colnames, use_colnames
sourcePartial("other_authors/analysis_standalone.R",
              startTag='key_colnames <- c',
              endTag='use_colnames <- c')
print("key_colnames:")
print(key_colnames)
use_colnames_old = use_colnames
use_colnames = cols_all  #too limiting! use col_all instead
print("use_colnames:")
print(use_colnames)

# This sources the first part of other_authors/pull_and_clean_linelist.R
# where it downloads and identifies problematic dates (outside range, wrong format)
# This needs to be run in part so that we can update confounding_dates
sourcePartial("other_authors/pull_and_clean_linelist.R",
              startTag='url <- "https://docs.google.com/spreadsheets',
              endTag='Already excluded entries')

#update confounding dates (these will be later looked up when cleaning dates)
confounding_dates = c(confounding_dates, all_failed_conversions, all_outside_range)
print(paste("Valid dates:",valid_date_start,"to",valid_date_end))
print("confounding_dates: ")
print(confounding_dates)

# This sources the second part of other_authors/pull_and_clean_linelist.R
# Can't run to completion as combined_dat_melted has too few columns
# and will be incompatible with beoutbreakprepared's scripts
sourcePartial("other_authors/pull_and_clean_linelist.R",
              startTag='1. CLEAN DATES',
              endTag='combined_dat_melted <- reshape2::melt',  endskip=1)

# melts combined_dat[,columns_melt] for ggplot instead of full combined_dat
columns_melt = unique(c(use_colnames_old,
                'date_onset_symptoms', 'date_admission_hospital', 'date_confirmation', 'date_death_or_discharge',
                'hubei','outcome','country'))
combined_dat_melted <- reshape2::melt(combined_dat[,columns_melt],
                                      id.vars=c(key_colnames,"outcome"))

# This sources the 3rd and last part of other_authors/pull_and_clean_linelist.R
sourcePartial("other_authors/pull_and_clean_linelist.R",
              startTag='combined_dat_melted <- reshape2::melt', startskip=1)

# combined_dat$chronic_disease_binary is a column of lists and can't  be saved as feather
# Recode to numeric
combined_dat$chronic_disease_binary = as.character(combined_dat$chronic_disease_binary)
table(combined_dat$chronic_disease_binary,useNA = "ifany")
combined_dat$chronic_disease_binary[!(combined_dat$chronic_disease_binary %in% c('0','1'))] = NA
table(combined_dat$chronic_disease_binary,useNA = "ifany")
combined_dat$chronic_disease_binary = as.numeric(combined_dat$chronic_disease_binary)
table(combined_dat$chronic_disease_binary,useNA = "ifany")

age checker


# Save clean dataframe
path_combined_dat = 'data/combined_dat.feather'
write_feather(combined_dat, path_combined_dat)
#combined_dat = read_feather(path_combined_dat)

# Output the graphs to outdir
# N.B: graphics are not explicitly printed and saved when sourcing R script
# unless called with saveGraphics()
saveGraphics("other_authors/pull_and_clean_linelist.R", outdir="output/plots")


# To combined_dat with dates cleaned by jameshay218/case_to_infection's scripts,
# apply beoutbreakprepared/nCoV2019's scripts
#full_data = combined_dat[,cols_to_match]
ageChecker(combined_dat$age)

# get cross-sectional counts by sex and country from
source("other_authors/routine_summary.R")
sexSummary(combined_dat)        #barchart of gender counts
plot.new()
countrySummary(combined_dat)    #grid.table of country counts