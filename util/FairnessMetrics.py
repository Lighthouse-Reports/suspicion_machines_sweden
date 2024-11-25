from util.ConfusionMatrix import ConfusionMatrix


def calc_fn_diff(cm_group0 : ConfusionMatrix, cm_group1 : ConfusionMatrix):
    fnr_0 = cm_group0.false_negative_share/(cm_group0.false_negative_share + cm_group0.true_positive_share)
    fnr_1 = cm_group1.false_negative_share/(cm_group1.false_negative_share + cm_group1.true_positive_share)
    return fnr_0 - fnr_1

def calc_fn(cm_group : ConfusionMatrix) : 
    fnr = cm_group.false_negative_share/(cm_group.false_negative_share + cm_group.true_positive_share)

    return fnr 

def calc_fp_diff(cm_group0 : ConfusionMatrix, cm_group1 : ConfusionMatrix):
    fpr_0 = cm_group0.false_positive_share/(cm_group0.false_positive_share + cm_group0.true_negative_share)
    fpr_1 = cm_group1.false_positive_share/(cm_group1.false_positive_share + cm_group1.true_negative_share)
    return fpr_0 - fpr_1

def calc_fpr(cm_group : ConfusionMatrix) : 
    fpr = cm_group.false_positive_share/(cm_group.false_positive_share + cm_group.true_negative_share)

    return fpr

def calc_precision_diff(cm_group0 : ConfusionMatrix, cm_group1 : ConfusionMatrix):
    precision_0 = cm_group0.true_positive_share/(cm_group0.true_positive_share + cm_group0.false_positive_share)
    precision_1 = cm_group1.true_positive_share/(cm_group1.true_positive_share + cm_group1.false_positive_share)
    return precision_0 - precision_1

def calc_precision(cm_group : ConfusionMatrix) : 
    precision = cm_group.true_positive_share/(cm_group.true_positive_share + cm_group.false_positive_share)

    return precision

def main() : 
    pass 

if __name__ == "__main__" : 
    pass 