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
import matplotlib.pyplot as plt
import seaborn as sns

# Data pre-processing
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Importing functions from another dir
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

# import custom class
# import log_transform as cf

# Dimensionality reduction
from sklearn.decomposition import PCA


class TransformationPipeline:
    """
    A class for transformation pipeline
    """

    def __init__(self):
        """
        Define parameters
        """

    def pipeline(self, X_train, X_test):
        """
        Transformation pipeline of data with only numerical variables

        Parameters
        ___________
        X_train: Training feature matrix
        X_test: Test feature matrix

        Returns
        __________
        Transformation pipeline and transformed data in array
        """
        numerical_columns = X_train.select_dtypes(include=np.number).columns.values
        categorical_columns = X_train.select_dtypes(
            include=["object", "category"]
        ).columns.values

        # Create pipelines
        num_pipeline = Pipeline(
            [
                ("num_impute", SimpleImputer(strategy="median")),
                ("p_transf", PowerTransformer(standardize=False)),
                ("std_scaler", StandardScaler()),
            ]
        )

        cat_pipeline = Pipeline(
            [("cat_impute", OneHotEncoder(handle_unknown="ignore"))]
        )

        pipeline = Pipeline(
            steps=[
                (
                    "features",
                    FeatureUnion(
                        [
                            ("numerical_features", num_pipeline, numerical_columns),
                            ("categorical_features", cat_pipeline, categorical_columns),
                        ]
                    ),
                )
            ]
        )
        pipeline.fit(X_train)
        # Transform the training set
        X_train_scaled = pipeline.transform(X_train)
        X_test_scaled = pipeline.transform(X_test)

        return X_train_scaled, X_test_scaled

    def pipeline2(self, X_train, X_test):
        """
        Transformation pipeline of data with only numerical variables

        Parameters
        ___________
        X_train: Training feature matrix
        X_test: Test feature matrix

        Returns
        __________
        Transformation pipeline and transformed data in array
        """
        numerical_columns = X_train.select_dtypes(include=np.number).columns.values
        categorical_columns = X_train.select_dtypes(
            include=["object", "category"]
        ).columns.values

        # Create pipelines
        num_pipeline = Pipeline(
            [
                ("num_impute", SimpleImputer(strategy="median")),
                ("p_transf", PowerTransformer(standardize=False)),
                ("std_scaler", StandardScaler()),
            ]
        )

        cat_pipeline = Pipeline(
            [("cat_impute", OneHotEncoder(handle_unknown="ignore"))]
        )

        transformer = ColumnTransformer(
            [
                ("numerical_features", num_pipeline, numerical_columns),
                ("categorical_features", cat_pipeline, categorical_columns),
            ],
            remainder="passthrough",
        )

        # pipeline = Pipeline(
        #     steps=[
        #         (
        #             "features",
        #             FeatureUnion(
        #                 [
        #                     ("numerical_features", num_pipeline, numerical_columns),
        #                     ("categorical_features", cat_pipeline, categorical_columns),
        #                 ]
        #             ),
        #         )
        #     ]
        # )
        transformer.fit(X_train)
        # Transform the training set
        X_train_scaled = transformer.transform(X_train)
        X_test_scaled = transformer.transform(X_test)

        return X_train_scaled, X_test_scaled

    def pca_plot_labeled(self, data_, labels, palette=None):
        """
        Dimensionality reduction of labeled data using PCA 

        Parameters
        __________
        data: scaled data
        labels: labels of the data
        palette: color list

        Returns
        __________
        Matplotlib plot of two component PCA
        """
        # PCA
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(data_)

        # put in dataframe
        X_reduced_pca = pd.DataFrame(data=X_pca)
        X_reduced_pca.columns = ["PC1", "PC2"]
        X_reduced_pca["class"] = labels.reset_index(drop=True)

        # plot results
        plt.rcParams.update({"font.size": 15})
        plt.subplots(figsize=(12, 8))
        sns.scatterplot(
            x="PC1", y="PC2", data=X_reduced_pca, hue="class", palette=palette
        )

        # axis labels
        plt.xlabel("Principal component 1")
        plt.ylabel("Principal component 2")
        plt.title("Dimensionality reduction")
        plt.legend(loc="best")
        plt.savefig("../image/pca.png")
        plt.show()
        pca_ = PCA(n_components=50).fit(data_)

        return pca_, X_pca
