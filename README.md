### Suspicion Machines Sweden 

This repository contains the code and data related to Lighthouse Reports and Svenske Dagbladet's investigation into AI risk assessments deployed within the Swedish welfare system. Inn 2024, we received outcome data from a model deployed by the Swedish Social Insurance Agency (Forsakringskassan) to select applicants for fraud investigations. 

The dataset delivered to Lighthouse pertains to the model used to score applicants for Sweden’s temporary parental allowance benefit scheme. The scheme pays compensation to parents who take time off work to care for sick children. The dataset contains 6,129 people that were selected for investigation in 2017 and the outcome of that investigation: whether mistakes were or were not found in the benefit recipients’ application. Of the 6,129 cases, 1,047 were randomly selected and 5,082 were selected by the machine learning model. 

We tested this dataset against a number of fairness definitions outlined in the academic literature. You can the dataset [here](data/data_english.xlsx) and a Jupyter notebook analyzing it [here](sweden_algo_fairness.ipynb). We also tested the dataset against an internal fairness procedure developed by the agency. You can find that [here](sweden_sia_fairness.ipynb). 

The above notebooks make use of a number of utility functions and classes, including a class that defines a ConfusionMatrix object and a probability bootstraping procedure in the util folder. 

[TO-do] links to article. 
