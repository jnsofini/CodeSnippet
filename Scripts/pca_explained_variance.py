# explained_variance_ratio_ method of PCA is used to get the ration of variance (eigenvalue / total eigenvalues)
# Bar chart is used to represent individual explained variances.
# Step plot is used to represent the variance explained by different principal components.
# Data needs to be scaled before applying PCA technique.
#
# Scale the dataset; This is very important before you apply PCA
#
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.model_selection import train_test_split

import numpy as np
import matplotlib.pyplot as plt
import notebook_resources.preprocess as pp

TARGET = "B1_DEFLT_IN_12MO_PERF_WNDW_IND"


sc = StandardScaler()
TRANSFORM_DATA_PATH = "data.parquet"
RAW_DATA_PATH = "data2.parquet"

y = pp.load_data(RAW_DATA_PATH)[TARGET].astype("int8")
transformed_data = pd.read_parquet(TRANSFORM_DATA_PATH)
# transformed_data.drop(columns = ["B1_AMEND_IN_PAST_30_DAYS_CNT_CSS"], inplace=True)
# transformed_data[TARGET] = transformed_data[TARGET].astype("int8")

# split into train test sets
X_train, X_test, y_train, y_test = train_test_split(transformed_data, y, stratify=y)

sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)
#
# Instantiate PCA
#
pca = PCA()
#
# Determine transformed features
#
X_train_pca = pca.fit_transform(X_train_std)
#
# Determine explained variance using explained_variance_ration_ attribute
#
exp_var_pca = pca.explained_variance_ratio_
#
# Cumulative sum of eigenvalues; This will be used to create step plot
# for visualizing the variance explained by each principal component.
#
cum_sum_eigenvalues = np.cumsum(exp_var_pca)
#
# Create the visualization plot
#
plt.bar(range(0,len(exp_var_pca)), exp_var_pca, alpha=0.5, align='center', label='Individual explained variance')
plt.step(range(0,len(cum_sum_eigenvalues)), cum_sum_eigenvalues, where='mid',label='Cumulative explained variance')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal component index')
plt.legend(loc='best')
plt.tight_layout()
plt.show()