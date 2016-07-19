# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 20:40:52 2016
@author: Matts42
"""
import pandas as pd 
import numpy as np

#Data file containing ratings data
ratings = pd.read_csv("data/ratings.dat", delimiter ="::", header=None, 
                      names=["user_id", "movies_id","rating","timestamp"],engine='python')

#Data containing movie data
movies = pd.read_csv("data/movies.dat", delimiter ="::", header=None, 
                      names=["movies_id","title","genre"], engine='python')

#Data containing User Data 
users = pd.read_csv("data/users.dat", delimiter ="::", header=None, 
                      names=["user_id", "gender","age","occupation","zip"], engine='python')

#Extracting Data Ratings data:
ratings = ratings.drop(["timestamp"], 1)
ratings = ratings.pivot(index = "user_id", columns = "movies_id", values = "rating")

#Extracting Movies Data
movie_titles = movies 

genres = {"Action":0,"Adventure":1,"Animation":2,"Children's":3,"Comedy":4,"Crime":5,
          "Documentary":6,"Drama":7,"Fantasy":8,"Film-Noir":9,"Horror":10,"Musical":11,
          "Mystery":12,"Romance":13,"Sci-Fi":14,"Thriller":15,"War":16,"Western":17}

movies = movies.drop(["title"],1)
movies = movies.set_index("movies_id")
movies = movies['genre'].str.split("|", expand = True)

dummies1 = pd.get_dummies(movies[0], prefix='genre', prefix_sep='_')
col_names_dummies = dummies1.columns.values

dummies2 = pd.get_dummies(movies[1], prefix='genre', prefix_sep='_')
col_names_dummies = dummies1.columns.values

dummies3 = pd.get_dummies(movies[2], prefix='genre', prefix_sep='_')
col_names_dummies = dummies1.columns.values

dummies4 = pd.get_dummies(movies[3], prefix='genre', prefix_sep='_')
col_names_dummies = dummies1.columns.values

dummies5 = pd.get_dummies(movies[4], prefix='genre', prefix_sep='_')
col_names_dummies = dummies1.columns.values

dummies6 = pd.get_dummies(movies[5], prefix='genre', prefix_sep='_')
col_names_dummies = dummies1.columns.values

names = dummies1.columns.values

dummies = dummies1.replace(0,np.nan)
dummies2 = dummies2.replace(0,np.nan)
dummies3 = dummies3.replace(0,np.nan)
dummies4 = dummies4.replace(0,np.nan)
dummies5 = dummies5.replace(0,np.nan)
dummies = dummies.combine_first(dummies2)
dummies = dummies.combine_first(dummies3)
dummies = dummies.combine_first(dummies4)
dummies = dummies.combine_first(dummies5)

dummies = dummies.fillna(0)
movies = dummies
name = list(ratings.columns.values)
movies = movies.T
movies = movies[name]
movies = movies.T

#Extracting User Data
users = users.set_index("user_id")
#Creating Dummy col for jobs
dummies = pd.get_dummies(users['occupation'], prefix='job', prefix_sep='_')
col_names_dummies = dummies.columns.values

for i,value in enumerate(col_names_dummies):
    users[value] = dummies.iloc[:,i]

#Creating Dummy col for age
dummies = pd.get_dummies(users['age'], prefix='age', prefix_sep='_')
col_names_dummies = dummies.columns.values

for i,value in enumerate(col_names_dummies):
    users[value] = dummies.iloc[:,i]

map_gender = {"M":0,"F":1}
users = users.replace({"gender": map_gender})
users = users.drop(["age","occupation","zip"], 1)



"""
#Extracting Initial Data
user_pd = pd.DataFrame(users, columns = ["user_id","age","gender","occupation","zip"])
user_pd = user_pd.set_index("user_id")
items_pd = pd.DataFrame(movies, columns = ["movie_id","title","release","video_release","IMDB",
                                         "unknown","Action","Adventure","Animation","Child",
                                         "Comedy","Crime","Doc","Drama","Fantasy","Film-Noir",
                                         "Horror","Musical","Mystery","Romance","Sci-Fi", 
                                         "Thriller","War", "Western"])

items_pd = items_pd.drop(["movie_id","release","video_release","IMDB"], 1)
ratings_pd = pd.DataFrame(ratings, columns = ["user_id","movie_id", "rating","timestamp"])
ratings_pd = ratings_pd.drop(["timestamp"], 1)
movies = ratings_pd.pivot(index = "user_id", columns = "movie_id", values = "rating")

#Making the User Dataset Matrix friendly
map_gender = {"M":0,"F":1}
map_jobs = {}
Age_range = {"0-18":0, "18-25":1,"25-40":2,"40-60":3, "65-80":4}


#Creathing Jobs Dict
i = 0 
for job in jobs:
    map_jobs[job[0]] = i
    i = i + 1

def Age_Range(x):
    if x in range(19):
        x = 0
        return x
    elif x in range(18,26):
        x = 1
        return x
    elif x in range(25,41):
        x = 2
        return x
    elif x in range(40,66):
        x = 3
        return x
    elif x in range(65,81):
        x = 4
        return x

user_pd['age'] = user_pd['age'].astype(int)
user_pd['age'] = user_pd['age'].map(Age_Range)
user_pd = user_pd.replace({"gender": map_gender,'occupation': map_jobs})

#Creating Dummy col for Jobs
dummies = pd.get_dummies(user_pd['occupation'], prefix='job', prefix_sep='_')
col_names_dummies = dummies.columns.values

for i,value in enumerate(col_names_dummies):
    user_pd[value] = dummies.iloc[:,i]

#Creating Dummy col for age
dummies = pd.get_dummies(user_pd['age'], prefix='age', prefix_sep='_')
col_names_dummies = dummies.columns.values

for i,value in enumerate(col_names_dummies):
    user_pd[value] = dummies.iloc[:,i]

user_pd = user_pd.drop(["age","occupation","zip"], 1)
movies = movies.apply(pd.to_numeric, errors='coerce')
movies_int = np.array(movies)
np.nan_to_num(movies_int)

# Borrowed some code here from Padebetttu et. al. -DATA643- Project 2
user_mean = movies.T.mean(skipna=True)
item_mean = movies.mean(skipna=True)
movies = movies.apply(lambda x: x.fillna(x.mean(skipna = True)),axis=1)
movies_mean = movies.apply(lambda x: x-x.mean(), axis = 1).round(5)

#Finalizing our datasets
movies_np = np.array(movies_mean)
movies_np = movies_np.astype(float)

#items dataset 
items = items_pd.set_index(["title"])
items = items.replace('0', np.nan)
items = items.apply(pd.to_numeric, errors='coerce')
items = items.apply(lambda x: x.fillna(.000001),axis=1)

#users dataset
users = user_pd
users = users.replace('0', np.nan)
users = users.apply(pd.to_numeric, errors='coerce')
users = users.apply(lambda x: x.fillna(.000001),axis=1)


#Some Functions including an Error function from Bugra[5]
def get_error(Q, X, Y, W):
    return np.sum((W * (Q - np.dot(X, Y)))**2)

def svd_red(movies_mean,n):
    U1, s1, V1 = np.linalg.svd(movies_mean, full_matrices=True)
    k = np.zeros((len(s1),len(s1)),float)
    np.fill_diagonal(k,s1)
    k = k[:n,:n]
    k = np.sqrt(k)
    U2 = U1[:,:n]
    V2 =V1[:,:n].T
    Uk = np.dot(U2,k.T)
    Vk = np.dot(k,V2)
    R_red = np.dot(Uk,Vk)
    return R_red, Uk, Vk


"""


