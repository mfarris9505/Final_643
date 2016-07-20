# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 18:37:43 2016

@author: Matts42
"""
import pandas as pd 
import numpy as np

def subset(ratings,movies,users, )


def svd_red(movies,n):
    col = list(movies.columns.values)
    index = list(movies.index.values)
    U1, s1, V1 = np.linalg.svd(movies, full_matrices=True)
    k = np.zeros((len(s1),len(s1)),float)
    np.fill_diagonal(k,s1)
    k = k[:n,:n]
    k = np.sqrt(k)
    U2 = U1[:,:n]
    V2 =V1[:,:n].T
    Uk = np.dot(U2,k.T)
    Vk = np.dot(k,V2)
    R_red = np.dot(Uk,Vk)
    R_red = pd.DataFrame(R_red, index = index, columns=col)
    return R_red


def pred_fin(Q,sim):
    pred = Q.dot(sim) / np.array([np.abs(sim).sum(axis=1)]) 
    return pred

def ALS_Factor(Q, lambda_, n_factors, n_iterations):
    W = Q != 0
    W[W == True] = 1
    W[W == False] = 0
    # To be consistent with our Q matrix
    W = W.astype(np.float64, copy=False)
    m, n = Q.shape

    X = 5 * np.random.rand(m, n_factors) 
    Y = 5 * np.random.rand(n_factors, n)


    for ii in range(n_iterations):
        for u, Wu in enumerate(W):
            X[u] = np.linalg.solve(np.dot(Y, np.dot(np.diag(Wu), Y.T)) + lambda_ * np.eye(n_factors), np.dot(Y, np.dot(np.diag(Wu), Q[u].T))).T
        for i, Wi in enumerate(W.T):
            Y[:,i] = np.linalg.solve(np.dot(X.T, np.dot(np.diag(Wi), X)) + lambda_ * np.eye(n_factors), np.dot(X.T, np.dot(np.diag(Wi), Q[:, i])))

        print('{}th iteration is completed'.format(ii))
        
    weighted_Q_hat = np.dot(X,Y)    
    return weighted_Q_Hat, X, Y

jobs = {"other":0, "academic/educator":1, "artist":2, "clerical/admin":3, 
        "college/grad student":4, "customer service":5, "doctor/health care":6, 
        "executive/managerial":7, "farmer":8, "homemaker":9, "K-12 student":10, 
        "lawyer":11, "programmer":12, "retired":13, "sales/marketing":14, 
        "scientist":15, "self-employed":16, "technician/engineer":17,
        "tradesman/craftsman":18, "unemployed":19,"writer":20}

def find_random(age,gender=None,job=None):
    if age < 18:
        Age_col="age_1"
    elif age in range(18,25):
        Age_col="age_18"
    elif age in range(25,35):
        Age_col="age_25"
    elif age in range(35,45):
        Age_col="age_35"
    elif age in range(45,50):
        Age_col="age_45"
    elif age in range(50,55):
        Age_col="age_50"
    elif age >= 56:
        Age_col="age_56"
    
    if gender == "M":
        Gender_col = 0
    elif gender == "F":
        Gender_col = 1
    else:
        pass
    
    if job != None:
        ind = jobs[job]
        Job_col = "job_"+str(ind)
    else:
        pass
    
