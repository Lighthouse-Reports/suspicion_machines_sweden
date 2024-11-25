import pandas as pd 
import numpy as np 
from util.ConfusionMatrix import ConfusionMatrix
from util.FairnessMetrics import * 

"""
Author: Justin-Casimir Braun & Gabriel Geiger
Date: 17-04-2024 
"""


"""
This function setups our metrics dict for a particular category. 
Metrics dict will store each iteration of the Bootstraping. For example, 
"""
def setup_metrics_dict(cur_metric : str, cur_group_values:list) -> dict[str : list] : 
    
    metrics_dict = {
        "category":[],
        "group0" : [],
        "group1" : []
    }

    """
    1.We also want to create columns for that metric for each group (e.g. predictive_parity_men, predictive_parity_women
    2.For each fairness metric, we want to create a column for the difference for this metric (e.g. difference in predictive parity). 
    """

    # 1.  
    for group in cur_group_values : 
        metrics_dict[f"{cur_metric}_{group}"] = []

    # 2.  
    metrics_dict[f"{cur_metric}_difference"] = []
    
    return metrics_dict

"""
Samples from the dataframe for a group with replacement and calculates a set of fairness metrics. 
@category_df: A dataframe contaning the data for this category (e.g. gender)
@metrics_dict: The dictionary containing the results of each sampling iteration. 
@metrics: A list of the fairness metrics to run. 
@category_name : The name of the current category (e.g. gender)
@cur_group_values: A list with the unique groups for this category (e.g. men and women)
@sample_size: The size of teh sample to take from the dataframe. 

@return metrics_dict: The metrics dictionary updated with the new data for this iteration 
"""
def sample(category_df : pd.DataFrame, metrics_dict : dict, cur_metric : str, category_name : str, cur_group_values : list, sample_size : int) -> dict[str : list] : 
    
    #sample with replacement from cur_df
    sample_df = category_df.sample(n = sample_size, replace = True)
        
    #get confusion matrices for both dfs
    cm_group0 = ConfusionMatrix(category_name, cur_group_values[0], sample_df)
    cm_group1 = ConfusionMatrix(category_name, cur_group_values[1], sample_df)

    metrics_dict["category"].append(category_name)
    metrics_dict['group0'].append(cur_group_values[0])
    metrics_dict['group1'].append(cur_group_values[1]) 

    #calculate metrics
    if cur_metric == 'false_negative_balance':

        # Caclulate the different between the two groups 
        metrics_dict[f'{cur_metric}_difference'].append(calc_fn_diff(cm_group0, cm_group1))

        # Calculate the actual metric or each group 
        metrics_dict[f'{cur_metric}_{cur_group_values[0]}'].append(calc_fn(cm_group0))
        metrics_dict[f'{cur_metric}_{cur_group_values[1]}'].append(calc_fn(cm_group1))

    elif cur_metric == 'false_positive_error_rate':
        metrics_dict[f'{cur_metric}_difference'].append(calc_fp_diff(cm_group0, cm_group1))

        metrics_dict[f'{cur_metric}_{cur_group_values[0]}'].append(calc_fpr(cm_group0))
        metrics_dict[f'{cur_metric}_{cur_group_values[1]}'].append(calc_fpr(cm_group1))

    elif cur_metric == 'predictive_parity':
        metrics_dict[f'{cur_metric}_difference'].append(calc_precision_diff(cm_group0, cm_group1))
        metrics_dict[f'{cur_metric}_{cur_group_values[0]}'].append(calc_precision(cm_group0))
        metrics_dict[f'{cur_metric}_{cur_group_values[1]}'].append(calc_precision(cm_group1))
    
    else : 
        raise Exception("Unknown metric",cur_metric)
    
    return metrics_dict 

def calculate_aggregate_results(metrics_df, category_name, cur_metric, cur_group_values) -> pd.DataFrame : 

    results_dict = {}

    #calculate mean, sd, and p.values for each metrics
    results_dict["metric"] = [cur_metric]
    results_dict["category_name"] = [category_name]
    results_dict["group0"] = [cur_group_values[0]]
    results_dict["group1"] = [cur_group_values[1]]
    results_dict["conf_low_group0"] = [metrics_df[f'{cur_metric}_{cur_group_values[0]}'].quantile(0.05)]
    results_dict["mean_group0"] = [metrics_df[f'{cur_metric}_{cur_group_values[0]}'].mean(skipna=True)]
    results_dict["conf_high_group0"] = [metrics_df[f'{cur_metric}_{cur_group_values[0]}'].quantile(0.95)]
    results_dict["conf_low_group1"] = [metrics_df[f'{cur_metric}_{cur_group_values[1]}'].quantile(0.05)]
    results_dict['mean_group1'] = [metrics_df[f'{cur_metric}_{cur_group_values[1]}'].mean(skipna=True)]
    results_dict["conf_high_group1"] = [metrics_df[f'{cur_metric}_{cur_group_values[1]}'].quantile(0.95)]
    results_dict['mean_conf_low'] = [metrics_df[f'{cur_metric}_difference'].quantile(0.05)]
    results_dict['mean_difference'] = [metrics_df[f'{cur_metric}_difference'].mean(skipna=True)]
    results_dict['mean_conf_high'] = [metrics_df[f'{cur_metric}_difference'].quantile(0.95)]
    results_dict['sd_difference'] = [metrics_df.loc[:,f'{cur_metric}_difference'].std(skipna = True)]
    results_dict['se_difference'] = [1.96 * (results_dict['sd_difference'][0] / np.sqrt(len(metrics_df)))]


    results_dict['gt_difference_zero'] = [(metrics_df.loc[:,f'{cur_metric}_difference'] > 0).mean(skipna = True)]
    results_dict['st_difference_zero'] = [(metrics_df.loc[:,f'{cur_metric}_difference'] < 0).mean(skipna = True)]

    # Round all of our float values 
    results_dict = {key: round(value[0],4) if isinstance(value[0],float) else value for key, value in results_dict.items()}

    return pd.DataFrame(results_dict)

def bootstrap(category_df : pd.DataFrame, iterations = 10000, cur_metric = "", seed = 42) -> pd.DataFrame : 
    
    np.random.seed(seed)

    category_name = category_df.columns[-1]

    # Get groups (e.g. men and women)
    cur_group_values = category_df[category_name].unique()

    print(f"Bootstraping metrics {cur_metric} for category {category_name} and values {cur_group_values}")

    # Setup our metrics dict 
    metrics_dict = setup_metrics_dict(cur_metric, cur_group_values)

    # Get our sample size (which is just the size of the dataframe
    sample_size = category_df.shape[0]

    for i in range(iterations) : 
        metrics_dict = sample(category_df, metrics_dict, cur_metric, category_name, cur_group_values, sample_size)

    # Convert our dictionary to a dataframe 
    metrics_df = pd.DataFrame(metrics_dict)

    results = pd.DataFrame(calculate_aggregate_results(metrics_df, category_name, cur_metric, cur_group_values))

    return results

    

def main() : 
    pass 

if __name__ == "__main__" : 
    main()