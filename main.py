if input ('Preprocess data or run models? (p/r): ') == 'p':
    from preprocess.preprocess import preprocess
    preprocess ()
    exit (0)


# Import Libraries
import pandas as pd
from feature_selection import *
from train_model import *
from os import system
from gc import collect


# Read already preprocessed CSV datasets
try:
    books = pd.read_csv ("processed/books.csv")
    users = pd.read_csv ("processed/users.csv")
    ratings = pd.read_csv ("processed/ratings.csv")
    new_books = pd.read_csv ("processed/new_books.csv")
    new_users = pd.read_csv ("processed/new_users.csv")
    new_ratings = pd.read_csv ("processed/new_ratings.csv")
except:
    print ('Could not find processed datasets!')
    exit (1)


# Merge datasets
book_ratings = pd.merge (ratings, books, on = 'ISBN', how = 'inner')
user_ratings = pd.merge (ratings, users, on = 'User-ID', how = 'inner')
data = pd.merge (user_ratings, books, on = 'ISBN', how = 'inner')
new_book_ratings = pd.merge (new_ratings, new_books, on = 'ISBN', how = 'inner')
new_user_ratings = pd.merge (new_ratings, new_users, on = 'User-ID', how = 'inner')
new_data = pd.merge (new_user_ratings, new_books, on = 'ISBN', how = 'inner')


# Validate all values have been imputed; no missing values
if False:
    print (data ['Book-Rating'].value_counts ())
    print (new_data ['Book-Rating'].value_counts ())
    from analysis.check_for_na import *
    check_for_na(users, books, new_users, new_books)

# Clear Memory
del users, books, ratings, new_users, new_books, new_ratings, book_ratings, user_ratings, new_book_ratings, new_user_ratings
collect ()
print ('\nMemory state:'); system ('free -m'); print ()


# Feature selection
selected_features_MI = feature_selection (data, 0.1, 0) 
selected_features_nMI = feature_selection (data, 0.1, 1) # Use instead of IG

# Model training
print("Models are Training...")
predicted_ratings_1 = pd.DataFrame({'Predicted-Rating' : train_with_kNN(data, new_data, selected_features_MI, 35, True)})
predicted_ratings_2 = pd.DataFrame({'Predicted-Rating' : train_with_DT(data, new_data, selected_features_nMI, True)})
print("Finished Training!")


# Analytics
if input ('Run analytics? (y/n): ') == 'y':
    from analysis.analytics import *
    avg_ratings(data)
    age_vs_rating(data)
    confusion_matrix_graph (new_data ['Book-Rating'], predicted_ratings_1, 'kNN')
    confusion_matrix_graph (new_data ['Book-Rating'], predicted_ratings_2, 'DT')
    rating_amount_table()
    accuracy_line_graph()
    print("Graphs generated!")


# Book Recommendation System
new_data = pd.concat([new_data,predicted_ratings_2], axis = 1)[['ISBN','Predicted-Rating']]
new_data = new_data.groupby('ISBN').agg({'Predicted-Rating': ['mean', 'count']})
new_data.columns = ['Predicted-Rating', 'Number_Bought']
new_data = new_data.sort_values(by=['Predicted-Rating', 'Number_Bought'], ascending=[False, False])
new_data = new_data [new_data ['Predicted-Rating'] > 7] # Recommend only those with rating above 7
new_data.to_csv('processed/RecommendedBooks.csv')
print("RecommendedBooks.csv generated in /processed!")

