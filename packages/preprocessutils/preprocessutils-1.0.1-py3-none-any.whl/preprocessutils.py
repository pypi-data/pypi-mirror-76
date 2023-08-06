import pandas as pd
import numpy as np
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler


def remove_imbalance(self, data, target, threshold=10.0, oversample=True, smote=False):
    """
    Method Name: remove_imbalance
    Description: This method will be used to handle unbalanced datasets(rare classes) through oversampling/ undersampling
                 techniques
    Input Description: data: the input dataframe with target column.
                       threshold: the threshold of mismatch between the target values to perform balancing.

    Output: A balanced dataframe.
    On Failure: Raise Exception

    Written By: Punit Nanda
    Version: 1.1
    Revisions: None

    """
    try:
        X = data.drop(target, axis=1)
        y = data[target]
        no_of_classes = y.nunique()

        if no_of_classes == 2:
            thresh_satisfied = ((y.value_counts() / float(len(y)) * 100).any() < threshold)
            # pdb.set_trace()
            if thresh_satisfied:
                if smote:
                    smote = SMOTE()
                    X, y = smote.fit_resample(X, y)
                elif oversample:
                    ROS = RandomOverSampler(sampling_strategy='auto', random_state=42)
                    X, y = ROS.fit_sample(X, y)
                else:
                    ROS = RandomUnderSampler(sampling_strategy='auto', random_state=42)
                    X, y = ROS.fit_sample(X, y)
        else:

            high = (y.value_counts() / float(len(y)) * 100).ravel().max()
            low = (y.value_counts() / float(len(y)) * 100).ravel().min()

            thresh_satisfied = (high - low > 100.0 - threshold)

            while thresh_satisfied:
                if smote:
                    smote = SMOTE(sampling_strategy='minority')
                    X, y = smote.fit_resample(X, y)
                elif oversample:
                    ROS = RandomOverSampler(sampling_strategy='minority', random_state=42)
                    X, y = ROS.fit_sample(X, y)
                else:
                    ROS = RandomUnderSampler(sampling_strategy='auto', random_state=42)
                    X, y = ROS.fit_sample(X, y)

                high = (y.value_counts() / float(len(y)) * 100).ravel().max()  # added v0.1
                low = (y.value_counts() / float(len(y)) * 100).ravel().min()  # added v0.1
                thresh_satisfied = (high - low > 100.0 - threshold)
                # pdb.set_trace()

        y.to_frame(name=target)
        dfBalanced = pd.concat([X, y], axis=1)
        return dfBalanced

    except Exception as e:
        raise Exception()  # raising exception and exiting