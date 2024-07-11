from preprocess.regex_filters import *
from preprocess.api import *

# Preprocess books dataset
def process_books(books):
    # Books - Title
    books ['Book-Title'] = clean_title (books ['Book-Title'])
    get_titles (books)
    books.loc [books ['Book-Title'].isna (), 'Book-Title'] = 'Unknown Title'

    # Books - Author
    books ['Book-Author'] = clean_author (books ['Book-Author'])
    books.loc [books ['Book-Author'].isna (), 'Book-Author'] = 'Unknown Author'

    # Books - Book-Publisher
    books ['Book-Publisher'] = clean_publisher (books ['Book-Publisher'])
    books.loc [books ['Book-Publisher'].isna (), 'Book-Publisher'] = 'Unknown Publisher'

    # Books - Year-Of-Publication
    books.loc [books ['Year-Of-Publication'] > 2024, 'Year-Of-Publication'] = 0
    get_years (books)

    # Get average publication years for authors, publishers and all books in collection
    authors_avg_year = books.loc [books ['Year-Of-Publication'] > 0].groupby ('Book-Author').mean (numeric_only = True).astype (int).reset_index ()
    publishers_avg_year = books.loc [books ['Year-Of-Publication'] > 0].groupby ('Book-Publisher').mean (numeric_only = True).astype (int).reset_index ()
    book_avg_year = books ['Year-Of-Publication'].median ()

    # Fill in book years that API calls could not find - iterative approach 😊😊 (happy now cuz it's only 28 books)
    for index, book in books.loc [books ['Year-Of-Publication'] == 0].iterrows ():
        avg_author = authors_avg_year.loc [authors_avg_year ['Book-Author'] == book ['Book-Author']]
        avg_publisher = publishers_avg_year.loc [publishers_avg_year ['Book-Publisher'] == book ['Book-Publisher']]
        # Try to get average date from the author
        if not avg_author.empty:
            books.at [index, 'Year-Of-Publication'] = avg_author ['Year-Of-Publication'].iloc [0]
        # Try to get average date from the publisher
        elif not avg_publisher.empty:
            books.at [index, 'Year-Of-Publication'] = avg_publisher ['Year-Of-Publication'].iloc [0]
        # None found, setting year to mean in the whole collection
        else:
            books.at [index, 'Year-Of-Publication'] = book_avg_year
    
    return books
