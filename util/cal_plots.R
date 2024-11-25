library(predtools)
library(magrittr)
library(dplyr)
library(readxl)
library(ggplot2)
library(probably)
library(tidymodels)
library(gbm)
library(scales)

setwd("/Users/justin-casimirbraun/GitHub/Sweden_Fairness_v2")

gender <- read_xlsx('raw_data/data_english.xlsx', sheet = 'Gender 2 Decimals') %>%
  filter(!is.na(`Risk Score`)) %>%
  rename(risk_score = 'Risk Score') %>%
  mutate(true_outcome = case_when(Result %in% c('Errors Found', 'Control Investigation') ~ 1, 
                                  Result %in% c('No Errors Found', 'No Control Investigation') ~ 0,
                       .default = NA),
         risk_score = rescale(risk_score))

cal_plot_breaks(gender, true_outcome, risk_score, num_breaks = 20,conf_level = 0.95, .by = Gender)+
  ggtitle('Calibration plots by Gender')+
  scale_x_continuous(labels = scales::number_format(accuracy = 0.1, decimal.mark = '.'))

ggsave('cal_plots/gender.png', plot = last_plot())

income <- read_xlsx('raw_data/data_english.xlsx', sheet = 'Income 2 Decimals') %>%
  filter(!is.na(`Risk Score`)) %>%
  rename(risk_score = 'Risk Score') %>%
  mutate(true_outcome = case_when(Result %in% c('Errors Found', 'Control Investigation') ~ 1, 
                                  Result %in% c('No Errors Found', 'No Control Investigation') ~ 0,
                                  .default = NA),
         risk_score = rescale(risk_score),
         Income = as.numeric(Income),
         income_binary = case_when(Income < median(Income, na.rm = T) ~ 'low',
                                   Income > median(Income, na.rm = T) ~ 'high',
                                   .default = NA)) %>%
  filter(!is.na(income_binary))

cal_plot_breaks(income, true_outcome, risk_score, num_breaks = 20,conf_level = 0.95, .by = income_binary)+
  ggtitle('Calibration plots by income')+
  scale_x_continuous(labels = scales::number_format(accuracy = 0.1, decimal.mark = '.'))

ggsave('cal_plots/income.png', plot = last_plot())


education <- read_xlsx('raw_data/data_english.xlsx', sheet = 'Education 2 Decimals') %>%
  filter(!is.na(`Risk Score`)) %>%
  rename(risk_score = 'Risk Score') %>%
  mutate(true_outcome = case_when(Result %in% c('Errors Found', 'Control Investigation') ~ 1, 
                                  Result %in% c('No Errors Found', 'No Control Investigation') ~ 0,
                                  .default = NA),
         risk_score = rescale(risk_score)) %>%
  filter(!is.na(Education))

cal_plot_breaks(education, true_outcome, risk_score, num_breaks = 20,conf_level = 0.95, .by = Education)+
  ggtitle('Calibration plots by Education')+
  scale_x_continuous(labels = scales::number_format(accuracy = 0.1, decimal.mark = '.'))

ggsave('cal_plots/education.png', plot = last_plot())


foreign <- read_xlsx('raw_data/data_english.xlsx', sheet = 'Foreign 2 Decimals') %>%
  filter(!is.na(`Risk Score`)) %>%
  rename(risk_score = 'Risk Score',
         foreign = 'Foreign Background',
         immigrant = 'Born Abroad') %>%
  mutate(true_outcome = case_when(Result %in% c('Errors Found', 'Control Investigation', 'No Control Investigation') ~ 1, 
                                  Result %in% c('No Errors Found', 'No Control Investigation') ~ 0,
                                  .default = NA),
         risk_score = rescale(risk_score))

cal_plot_breaks(foreign, true_outcome, risk_score, num_breaks = 20,conf_level = 0.95, .by = foreign)+
  ggtitle('Calibration plots by foreign')+
  scale_x_continuous(labels = scales::number_format(accuracy = 0.1, decimal.mark = '.'))

ggsave('cal_plots/foreign.png', plot = last_plot())

cal_plot_breaks(foreign, true_outcome, risk_score, num_breaks = 20,conf_level = 0.95, .by = immigrant)+
  ggtitle('Calibration plots by immigrant')+
  scale_x_continuous(labels = scales::number_format(accuracy = 0.1, decimal.mark = '.'))

ggsave('cal_plots/immigrant.png', plot = last_plot())

