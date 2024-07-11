import pandas as pd
from preprocess.citystates import *
from preprocess.process_users import *
from preprocess.process_books import *

from os import system
from gc import collect

# Preprocess the datasets
def preprocess ():
    # Read CSVs
    books = pd.read_csv ("data/BX-Books.csv")
    users = pd.read_csv ("data/BX-Users.csv")
    ratings = pd.read_csv ("data/BX-Ratings.csv")
    new_books = pd.read_csv ("data/BX-NewBooks.csv")
    new_users = pd.read_csv ("data/BX-NewBooksUsers.csv")
    new_ratings = pd.read_csv ("data/BX-NewBooksRatings.csv")
    print ('CSVs read!')
    print ('\nMemory state:'); system ('free -m'); print ()


    # Pre-process ratings for training and testing datasets
    ratings ['Book-Rating'] = ratings ['Book-Rating'].astype ('Int16')
    new_ratings ['Book-Rating'] = new_ratings ['Book-Rating'].astype ('Int16')


    # Pre-process users for training and testing datasets
    cs = get_citystates ()
    users = process_users (users, cs)
    new_users = process_users (new_users, cs)

    del cs
    collect ()
    print ('Users preprocessed!')
    print ('\nMemory state:'); system ('free -m'); print ()


    # Pre-process books for training and testing datasets
    books = process_books (books)
    new_books = process_books (new_books)

    collect ()
    print ('Books preprocessed!')
    print ('\nMemory state:'); system ('free -m'); print ()


    # Save datasets
    books.to_csv ('processed/books.csv', index = False)
    users.to_csv ('processed/users.csv', index = False)
    ratings.to_csv ('processed/ratings.csv', index = False)
    new_books.to_csv ('processed/new_books.csv', index = False)
    new_users.to_csv ('processed/new_users.csv', index = False)
    new_ratings.to_csv ('processed/new_ratings.csv', index = False)
