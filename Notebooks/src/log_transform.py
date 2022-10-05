####################################
# Author: jnsofini
# Date modified: 12/03/2021
####################################

# Filter warnings
import warnings

warnings.filterwarnings("ignore")

# Data manipulation and visualization
import pandas as pd
import numpy as np

# Data pre-processing
from sklearn.base import BaseEstimator, TransformerMixin


class LogTransformer(BaseEstimator, TransformerMixin):
    """
  A class to perform log(1+x) transformation on numerical features
  """

    def __init__(self):
        """
    Define parameters
    """

    def fit(self, X, y=None):
        """
    Do nothing
    """
        return self

    def transform(self, X, y=None):
        """
    Log transform numerical variables
    """
        num_attribs = list(X.select_dtypes("number"))
        self.X_num = X[num_attribs]
        return np.log1p(self.X_num)

