# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 23:06:06 2016

@author: DIP 
"""
from sklearn import metrics
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def build_feature_matrix(documents, feature_type='frequency',
                         ngram_range=(1, 1), min_df=0.0, max_df=1.0):

    feature_type = feature_type.lower().strip()  
    
    if feature_type == 'binary':
        vectorizer = CountVectorizer(binary=True, min_df=min_df,
                                     max_df=max_df, ngram_range=ngram_range)
    elif feature_type == 'frequency':
        vectorizer = CountVectorizer(binary=False, min_df=min_df,
                                     max_df=max_df, ngram_range=ngram_range)
    elif feature_type == 'tfidf':
        vectorizer = TfidfVectorizer(min_df=min_df, max_df=max_df, 
                                     ngram_range=ngram_range)
    else:
        raise Exception("Wrong feature type entered. Possible values: 'binary', 'frequency', 'tfidf'")

    feature_matrix = vectorizer.fit_transform(documents).astype(float)
    
    return vectorizer, feature_matrix
    
    
    
def display_evaluation_metrics(true_labels, predicted_labels, positive_class='positive'):
    accuracy = np.round(metrics.accuracy_score(true_labels, predicted_labels),
                        2)
    precision = np.round(metrics.precision_score(true_labels, predicted_labels,
                                                 pos_label=positive_class, average='binary'),
                        2)
    recall = np.round(metrics.recall_score(true_labels,
                                           predicted_labels,
                                           pos_label=positive_class,
                                           average='binary')
                     )
    f1_score = np.round(metrics.f1_score(true_labels,
                                         predicted_labels,
                                         pos_label=positive_class,
                                         average='binary')
                       )
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1 Score: ", f1_score)
    
    
def display_confusion_matrix(true_labels, predicted_labels, classes=['positive','negative']):
    cm = metrics.confusion_matrix(y_true=true_labels,
                                  y_pred=predicted_labels,
                                  labels=classes)
    cm_frame = pd.DataFrame(data=cm,
                            columns=pd.MultiIndex(levels=[['Predicted:'], classes],
                                                  codes=[[0, 0], [0, 1]]),
                            index=pd.MultiIndex(levels=[['Actual:'], classes],
                                               codes=[[0,0], [0,1]])
                           )
    print(cm_frame)

def display_classification_report(true_labels, predicted_labels, classes=['positive','negative']):

    report = metrics.classification_report(y_true=true_labels, 
                                           y_pred=predicted_labels, 
                                           labels=classes) 
    print(report)