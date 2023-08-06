# preprocessutils

This packages has data processing tools which can be used to make developer work easier

## Installation

pip install preprocessutils

## Usage

from preprocessutils import fix_imbalance

# OVER-SAMPLE
balanced_dataframe = fix_imbalance(data=df, target=target, threshold=10.0, oversample=True)

# OVER-SAMPLE SMOTE
balanced_dataframe = fix_imbalance(data=df, target=target, threshold=10.0, smote=True)

# UNDER-SAMPLE
balanced_dataframe = fix_imbalance(data=df, target=target, threshold=10.0, oversample=False)