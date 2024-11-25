import pandas as pd 


"""
A class that represents a Confusion Matrix for each table (e.g. gender, foreign background) and group (e.g. woman, Swedish)

In practice, the Confusion Matrix looks like this: 

|-------------|
|  FP |  TP   | PP
|-------------|
|  TN |  FN   | PN
|-------------|
   AN |  AP 

Where : 
FP = False positive: The number of cases where the model incorrectly predicts an applicant made a mistake. 
TP = True positive: The number of cases where the model correctly predicts an applicant made a mistake. 
TN = True negatives: The number of cases where the model correctly predicts an applicant did not make a mistake. 
FN = False negatives: The number of cases where the model incorrectly predicts an applicant did not make a mistake

And where margins: 
PP = Predicted Positive: The number of cases the model predicted an applicant made a mistake. 
PN = Predicted Negative: The number of cases where the model predicted an applicant did not make a mistake. 
AN = Actual Negatives: The number of cases where an applicant did not make a mistake. 
AP = Actual Postiives: The number of cases where an applicant did make a mistake. 

@input category: The category (e.g. gender, foreign background) for this ConfusionMatrix 
@input group: The group (e.g. man, woman) for this ConfusionMatrix 
@input table: The dataframe containing the data for this group and category
"""

class ConfusionMatrix() : 
    def __init__(self,category : str, group : str, table : pd.DataFrame) : 
        self.category = category
        self.group = group 
       
        # Margins 
        self.predicted_positive_share = None   
        self.predicted_negative_share = None 
        self.actual_positive_share = None 
        self.actual_negative_share = None 

        # Cells
        self.true_positive_share = None
        self.false_positive_share = None
        self.true_negative_share = None
        self.false_negative_share = None


        # Use our margins to construct the matrix. 
        self.construct_matrix(table)
    
    def __str__(self) -> str : 
        output_string = """
        Confusion Matrix: {category} {title}
        TP: {tp} 
        FP: {fp} 
        TN: {tn} 
        FN: {fn} 
        """.format(category = self.category,
                   title=self.group,
                   tp=self.true_positive_share,
                   fp=self.false_positive_share,
                   tn=self.true_negative_share,
                   fn=self.false_negative_share)
        
        return output_string

    """
    This function build our matrix. 

    @input table: The dataframe contaning the data. 
    @total_population_count: The number of people in the total welfare population. 
    """
    def construct_matrix(self,table:pd.DataFrame,total_population_count=977730) -> None: 

        # Split our table into the random sample and non-random sample. 
        # We'll need these to deduce certain numbers 
        algorithm_sample = table[table["Selection Method"] != "Random"]
        random_sample = table[table["Selection Method"] == "Random"]
        
        # Filter our algorithm and random samples for the category (e.g. women) that we are interested in  
        algorithm_filtered = algorithm_sample[algorithm_sample[self.category] == self.group]
        random_filtered = random_sample[random_sample[self.category] == self.group]

        # Calculate the number of x category (e.g. women) in the entire benefit applicant population 
        # First we get the share of that category in the random sample and then we multiply that by the total size of the benefit applicant population
        share_of_class_random = len(random_filtered) / len(random_sample)
        class_count_total = int(share_of_class_random * total_population_count)

        """
        In order to infer some of our missing shares, we need to calculate the margins of our confusion matrix 
        (1) Predicted positive share: The share of predicted positives for category x in the total benefit applicant population
        (2) Predicted negative share: The share of predicted negatives for category x in the total benefit applicant population 
        (3) Actual positive share: The share of actual positives (e.g. true rate of error) for category x 
        (4) Actual negative share: The share of actual negatives (e.g. true rate of error) for category x 
        """

        # Predicted Positive Share:
        predicted_positive_count = len(algorithm_filtered)
        pred_p_share = predicted_positive_count / class_count_total

        # Predicted Negative Share
        pred_n_share = 1 - pred_p_share

        # Actual P Share 
        actual_positive_count = len(random_filtered[random_filtered["Result"] == "Errors Found"])
        class_count_random = len(random_filtered)

        actual_p_share = actual_positive_count / class_count_random

        # Actual N Share
        actual_n_share = 1 - actual_p_share

        """
        Once we have our margins, we derive some of our missing inner cell values. 
        We can learn our true positive and false positive shares from the algorithm sample 
        We can then learn our true and false negative shares from subtracting our true and false positive shares
        from our actual positive and negative shares (ie. bottom margin)
        """

        # True Positive Share 
        true_positive_count = len(algorithm_filtered[algorithm_filtered["Result"] == "Errors Found"])
        true_p_share = true_positive_count / class_count_total 

        # False Positive Share 
        false_positive_count = len(algorithm_filtered[algorithm_filtered["Result"] == "No Errors Found"])
        false_p_share = false_positive_count / class_count_total 

        # True Negative Share 
        true_n_share = actual_n_share - false_p_share

        # False Negative Share
        false_n_share = actual_p_share - true_p_share 

        # Sanity Check: 
        #assert round(false_n_share + true_n_share,8) == round(pred_n_share,8)

        self.predicted_positive_share = pred_p_share 
        self.predicted_negative_share = pred_n_share

        self.true_positive_share = true_p_share 
        self.false_positive_share = false_p_share
        self.true_negative_share = true_n_share
        self.false_negative_share = false_n_share

