# Anomaly-Detection
Project emplying machine learning techniques for imbalanced data. 

In this repo is study of  anomaly detection specifically CreditCard Fraud. Creditcard fraud cost several individual and financial institution a lot of money and so the ability to identify and stop it is a desired problem to solve.  Here we use data from Kaggle with two imbalance cases. This means, the number of positive outcome are way fewer, specifically only 0.17% correspond to fraudulent transactions. Given this, special care is needed with such a problem. It has 31 features, 28 of which have been anonymized and are labeled V1 through V28. The remaining three features are the time, amount of the transaction as well as whether that transaction was fraudulent or not. It is anonymus and the V's are actually the Principal Component Analysis.

Anomaly detection can be treated in three main categories:

   1. Outlier Detection:

In outlier detection, the training data contains outliers which are defined as observations that are far from the others. The objective is to detect the outliers in a new observation and identify them

    2. Novelty Detection:

In novelty detection, a semi-supervised learning technique, the training data is not polluted by outliers. It is trained to learn the high and low density regions in the feature space, and we are interested in detecting whether a new observation is an outlier.

There are different ways we will approach this. We will perform undersampling, achieved by balancing the dominant class to the minority.
