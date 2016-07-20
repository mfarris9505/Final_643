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

genres = ["Action","Adventure","Animation","Children's","Comedy","Crime",
          "Documentary","Drama","Fantasy","Film-Noir","Horror","Musical",
          "Mystery","Romance","Sci-Fi","Thriller","War","Western"]

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

# Borrowed some code here from Padebetttu et. al. -DATA643- Project 2
ratings = ratings.apply(lambda x: x.fillna(x.mean(skipna = True)),axis=1)
ratings = ratings.apply(lambda x: x-x.mean(), axis = 1).round(5)


#Context Break-down to "Decouple" Data for age
def subset_users(ratings,users,col):
    Rating= ratings.loc[list(users[users[col] >0].T.columns.values)]
    return Rating
    
#Context Break_down by Genre(NOT A COMPLETE LIST)
def subset_movies(ratings, movies,col):
    Rating = ratings[list(movies[movies[col] >0].T.columns.values)]
    return Rating

#SVD Function we are using (time efficient)
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


#Final Variable

Ratings_1 = subset_users(ratings,users,'age_1')
Ratings_2 = subset_users(ratings,users,'age_18')
Ratings_3 = subset_users(ratings,users,'age_25')
Ratings_4 = subset_users(ratings,users,'age_35')
Ratings_5 = subset_users(ratings,users,'age_45')
Ratings_6 = subset_users(ratings,users,'age_50')
Ratings_7 = subset_users(ratings,users,'age_56')


genre_1 = movies(ratings, movies,'genre_Action')
genre_2 = movies(ratings, movies,"genre_Children's")
genre_3 = movies(ratings, movies,'genre_Comedy')
genre_4 = movies(ratings, movies,'genre_Drama')
genre_5 = movies(ratings, movies,'genre_Horror')
genre_6 = movies(ratings, movies,'genre_Romance')
genre_7 = movies(ratings, movies,'genre_Sci-Fi')


Total = svd_red(ratings, 50)
rate_1 = svd_red(Ratings_1, 50)
rate_2 = svd_red(Ratings_2, 50)
rate_3 = svd_red(Ratings_3, 50)
rate_4 = svd_red(Ratings_4, 50)
rate_5 = svd_red(Ratings_5, 50)
rate_6 = svd_red(Ratings_6, 50)
rate_7 = svd_red(Ratings_7, 50)


g_rate_1 = svd_red(genre_1, 50)
g_rate_2 = svd_red(genre_2, 50)
g_rate_3 = svd_red(genre_3, 50)
g_rate_4 = svd_red(genre_4, 50)
g_rate_5 = svd_red(genre_5, 50)
g_rate_6 = svd_red(genre_6, 50)
g_rate_7 = svd_red(genre_7, 50)


np.save
np.savetxt("ratings.csv", ratings, fmt='%1.3f', delimiter=",")
np.savetxt("Total.csv", Total, fmt='%1.3f', delimiter=",")
np.savetxt("movies.csv", movies, fmt='%1.3f', delimiter=",")
np.savetxt("users.csv", users, fmt='%1.3f', delimiter=",")


np.savetxt("g_rate_1.csv", g_rate_1, fmt='%1.3f', delimiter=",")
np.savetxt("g_rate_2.csv", g_rate_2, fmt='%1.3f', delimiter=",")
np.savetxt("g_rate_3.csv", g_rate_3, fmt='%1.3f', delimiter=",")
np.savetxt("g_rate_4.csv", g_rate_4, fmt='%1.3f', delimiter=",")
np.savetxt("g_rate_5.csv", g_rate_5, fmt='%1.3f', delimiter=",")
np.savetxt("g_rate_6.csv", g_rate_6, fmt='%1.3f', delimiter=",")
np.savetxt("g_rate_7.csv", g_rate_7, fmt='%1.3f', delimiter=",")

np.savetxt("rate_1.csv", rate_1, fmt='%1.3f', delimiter=",")
np.savetxt("rate_2.csv", rate_2, fmt='%1.3f', delimiter=",")
np.savetxt("rate_3.csv", rate_3, fmt='%1.3f', delimiter=",")
np.savetxt("rate_4.csv", rate_4, fmt='%1.3f', delimiter=",")
np.savetxt("rate_5.csv", rate_5, fmt='%1.3f', delimiter=",")
np.savetxt("rate_6.csv", rate_6, fmt='%1.3f', delimiter=",")
np.savetxt("rate_7.csv", rate_7, fmt='%1.3f', delimiter=",")