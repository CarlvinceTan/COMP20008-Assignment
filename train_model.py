from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier

import numpy as np
from sklearn.cluster import KMeans


# Machine Learning technique 1: KNN
def train_with_kNN(train, test, features, neighbours, testing = False):  
    # Encode categorical features
    encoder = OrdinalEncoder()
    X_train = encoder.fit_transform(train[features])
    y_train = encoder.fit_transform(train[['Book-Rating']]).ravel()
    X_test = encoder.fit_transform(test[features])  # Use the same encoder for test data
    y_test = encoder.fit_transform(test[['Book-Rating']]).ravel()  # Use the same encoder for test data

    # Instantiate the KNN model
    knn_model = KNeighborsClassifier(neighbours)

    # Fit the model to the training data
    knn_model.fit(X_train, y_train)

    # Make predictions on the testing data
    y_pred = knn_model.predict(X_test)

    # Evaluate the model
    if testing:
        accuracy = accuracy_score(y_test, y_pred)
        print("KNN accuracy:", accuracy)
    
    return y_pred


# Machine Learning techinque 2: Decision Trees
def train_with_DT(train, test, features, testing = False):
    # Encode categorical features
    encoder = OrdinalEncoder()
    X_train = encoder.fit_transform(train[features])
    y_train = encoder.fit_transform(train[['Book-Rating']]).ravel()
    X_test = encoder.fit_transform(test[features])  # Use the same encoder for test data
    y_test = encoder.fit_transform(test[['Book-Rating']]).ravel()  # Use the same encoder for test data

    # Train the decision tree model
    dt = DecisionTreeClassifier(criterion='entropy')
    dt.fit(X_train, y_train)

    # Make predictions on the testing data
    y_pred = dt.predict(X_test)

    # Evaluate the model
    if testing:
        accuracy = accuracy_score(y_test, y_pred)
        print("DT accuracy:", accuracy)

    return y_pred


# Cluster model training
def train_with_cluster(data, n_clusters):
    data_array = np.array(list(data))
    kmeans = KMeans(n_clusters=n_clusters)
    cluster_labels = kmeans.fit_predict(data_array)
    data_center = kmeans.cluster_centers_
    return cluster_labels, data_center

