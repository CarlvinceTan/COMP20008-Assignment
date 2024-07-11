README for code file  

Descriptions
---------------
Brief desrciption of the project

**Root**
---------------
> /data/
>> Folder with all initial datasets
---------------
> /graphs/
>> Folder where the graphs are saved to
---------------
> /processed/
>> Folder with processed datasests code
---------------
> /README.md
>> Here I am!
---------------
> /main.py
>> 1. Offers to do a preprocessing, if user agrees, runs related functions and terminates execution, otherwise continues
>> 2. Imports all the necessary packages
>> 3. Tries to read the processed datasets, terminates in case of failure
>> 4. Merges datasets together
>> 5. Clears unused memory (optional: set condition to True to get datasets diagnostics)
>> 6. Perform feature selection and model training based on it
>> 7. If user desires, performs analytics in form of various graphs
>> 8. Runs recommendation system to predict book scores
---------------
> /feature_selection.py
>> feature_selection : gain information and normalized mutual information
---------------
> /train_model.py
>> train_with_kNN : use KNN to train model used to do prediction
>> train_with_DT : use decision trees to train model used to do prediction
>> train_with_cluster : use cluster to train model used to do prediction
---------------
**Pre-processing**
---------------
> /preprocess/
>> Folder with all preprocessing code
---------------
> /preprocess/preprocess.py
>> preprocess : read datasets from files, perform a pre-processing on them, save to files
---------------
> /preprocess/regex_filters.py
>> remove_na : remove n/a, na, nan and none string
>> remove_bracketed_info : remove all the information in bracket
>> remove_symbols_exclude_period : remove symbols except lowercase letters, whitespaces and dots
>> remove_symbols_exclude_colon : remove symbols except lowercase letters, whitespaces and colons
>> remove_symbols : remove symbols except lowercase letters and whitespaces
>> normalize_to_ascii : normalize unicode to ensure string are expressed in same way (keep nan values)
>> remove_short_form : remove the shortened form from word
>> remove_extra_spaces : replace multiple whitespaces with single whitespace and delete if it appear at head or tail
>> empty_to_nan : replace empty data with nan
>> filter_first_last_word : find first and last words and split with whitespace
>> clean_user_text : turn all text to lowercase and ascii format and remove redundant text(n/a, bracketed information,symbols exclude dot)
>> clean_title : turn all text to lowercase and ascii format and remove redundant text(n/a, bracketed information,symbols exclude colon, multiple whitespaces, blank)
>> clean_author :turn all text to lowercase,split first&last word and ascii format and remove redundant text(n/a, bracketed information,symbols,blank,multiple whitespace)
>> clean_publisher :turn all text to lowercase and ascii format and remove redundant text(n/a, bracketed information,extra whitespace,word in dictionary:key_words,countries)
---------------
> /preprocess/process_book.py
>> process_books : Preprocess books datasets
---------------
> /preprocess/process_users.py
>> process_users : Preprocess users datasets
---------------
> /preprocess/api.py
>> get_years : function get book year from an [external resource]('https://openlibrary.org/isbn) through ISBN to fill missing year of publication
>> get_titles :function get book title from an [external resource]('https://openlibrary.org/isbn) through ISBN to fill missing book title
---------------
> /preprocess/citystates.py
>> get_citystates : obtain cities and states from an [external resource]('https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv) and process them
---------------
> /preprocess/dictionaries.py
>> countries : dictionary of countries names
>> short_forms : dictionary of places shortened forms
>> key_words : dictionary of publisher key words
---------------
**Analytics**
---------------
> /analysis/
>> Folder with all analytics code
---------------
> /analysis/analytics.py
>> avg_ratings : function used to draw a figure of an average rating for authors and countries
>> age_vs_rating : function used to draw a figure of an age vs rating distribution
>> confusion_matrix_graph : function used to draw confusion matrices
>> fig_clusters : function used to draw clusters
>> rating_amount_table : function used to draw rating counts
>> accuracy_line_graph : function used to draw a relation between knn accuracy and number of neighbours it uses
---------------
> /analysis/preanalysis.py
>> check_user_id : check is there any digit or whitespace in user id
>> check_isbn : check the length of isbn is 13 digits long
>> check_book_rating : check book rating is in range from 1 to 10 inclusive
>> check_user_citys : check is there any digit or whitespace in city
>> check_user_state : check is there any digit or whitespace in state
>> check_user_age : check the age is in range from 5 to 116 inclusive
---------------
> /analysis/check_for_na.py
>> check_for_na : check the missing values in provided datasets

