# -*- coding: utf-8 -*-
"""movie_Recommendation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ToXwF3SC918Du79SMyvkjC6h9Kly9WvB

**Pre-Processing**
"""

#Install kaggle
!pip install -q kaggle

#upload the  kaggle json file
from google.colab import files
files.upload()

# Create a directory named "kaggle"
!mkdir ~/.kaggle

#Copy the kaggle.json to created folder
! cp kaggle.json ~/.kaggle/

#permisson for the json to act
! chmod 600 ~/.kaggle/kaggle.json

#upload here api command that taken from the dataset
!kaggle datasets download -d aayushsoni4/tmdb-5000-movie-dataset-with-ratings

#unzip the file
!unzip tmdb-5000-movie-dataset-with-ratings.zip

import pandas as pd
credits=pd.read_csv('/content/tmdb_movie_credits.csv')
dataset=pd.read_csv('/content/tmdb_movie_dataset.csv')
rating =pd.read_csv('/content/tmdb_movie_ratings.csv')

movie=dataset.merge(credits,on='title')
movie.info()

# Select specific columns
movie=movie[['title','genres', 'keywords', 'original_language', 'overview', 'cast', 'crew']]

# Display the first row
movie.head(1)

movie.isnull().sum() #before dropping null value

# movie.dropna(inplace=True)  #in overview section only 1 value is null so I droped it

# movie.isnull().sum() #after droping null value

movie.duplicated().sum() #checking the duplicated row

movie.iloc[1].genres #invide movie with row 0 we are accessing only genres value

import ast  # helps in converting string to dictionary or list format

def convert1(obj):  # function
    fetch = []  # empty list
    try:
        for i in ast.literal_eval(obj):     # accessing the value
            fetch.append(i['name'])
    except ValueError:
        print("Error: Input is not a valid Python expression.")
    return fetch  # returning the list

movie['genres'] = movie['genres'].apply(convert1)

movie['keywords'][0]

movie['keywords'] = movie['keywords'].apply(convert1)

def convert3(obj):  # function
    fetch = []  # empty list
    counter=0
    try:
        for i in ast.literal_eval(obj):
          if counter!=3:    # accessing the value
            fetch.append(i['name'])
          else:
            break
    except ValueError:
        print("Error: Input is not a valid Python expression.")
    return fetch  # returning the list

movie['cast'] = movie['cast'].apply(convert3)

def convert(obj):  # function
    fetch = []  # empty list
    try:
        for i in ast.literal_eval(obj):    # accessing the value
          if i['job']=='Director':
            fetch.append(i['name'])
            break
    except ValueError:
        print("Error: Input is not a valid Python expression.")
    return fetch  # returning the list

movie['crew'] = movie['crew'].apply(convert3)

movie['overview'][1]  #Before split

movie.head(1)

# Applying lambda function to split each overview text into a list of words
movie['overview']= movie['overview'].apply(lambda x: x.split() if isinstance(x, str) else [])

#Removing all the spaces
movie['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movie['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movie['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movie['crew'].apply(lambda x:[i.replace(" ","") for i in x])

#Concating genres, keywords , cast ,crew
movie['tags']=movie['genres']+movie['keywords']+movie['cast']+movie['crew']

movie_df=movie[['title','tags']]  #creating new dataframe with title and tags

#converting list of tags into string format
movie_df['tags']=movie_df['tags'].apply(lambda x:" ".join(x))

movie_df['tags']=movie_df['tags'].apply(lambda x:x.lower())

movie_df.sample(5)

"""**Text Visulization**

The Porter Stemmer is a stemming algorithm, specifically designed to transform words into their root forms. It's part of the Natural Language Toolkit (NLTK), which is a Python library commonly used for natural language processing tasks.
"""

import nltk # eg. love,loves,loved conveted into it's root form as love
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)

movie_df['tags']=movie_df['tags'].apply(stem)

#Convert a collection of text documents to a matrix of token counts.
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer( max_features=5000,stop_words='english')  #here stop words means it not count the stop words like to, in from, by etc
vector=cv.fit_transform(movie_df['tags']).toarray()

vector #converting most frequently tags used in movie into binary formate inside the array

# checking the first 100 frequent counts in inside the 5000 list
empty=[]
for i in range(0,100):
  empty.append(cv.get_feature_names_out()[i]) #these are the 5000 words that are mostly repeated in the movie dataset
empty

#this will give the list of stop words
cv.get_stop_words()

from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vector)

#This will help in giving the index of the movie name
movie_df[movie_df['title']=='Four Rooms'].index[0]
sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[0])[1:6]

def recommend(movie):
  index_value=movie_df[movie_df['title']==movie].index[0]
  distance=similarity[index_value]
  movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
  for i in movie_list:
    print(movie_df.iloc[i[0]].title)

import pickle

pickle.dump(movie_df.to_dict(),open('movie_list.pkl','wb'))



pickle.dump(similarity,open('similarity.pkl','wb'))