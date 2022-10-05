# Filter warnings
import warnings

warnings.filterwarnings("ignore")

# Data manipulation
import pandas as pd
import numpy as np

# Data pre-processing
from sklearn.base import TransformerMixin


class DataFrameImputer(TransformerMixin):
    """ 
    Based on http://stackoverflow.com/a/25562948
   
    Impute missing categorical and numerical  values.
    Columns of dtype = object are imputed with the most frequent value in column.
    Columns of other types are imputed with median of column.
    """

    def __init__(self):
        """
        Define parameters
        """

    def fit(self, X, y=None):

        self.impute = pd.Series(
            [
                X[col].value_counts().index[0]
                if X[col].dtype == np.dtype("O")
                else X[col].median()
                for col in X.columns
            ],
            index=X.columns,
        )
        return self

    def transform(self, X, y=None):
        return X.fillna(self.impute)
