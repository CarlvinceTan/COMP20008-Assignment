from concurrent.futures import ThreadPoolExecutor
from requests import get
from re import findall
from tqdm import tqdm

# Obtains missing book years from API
def get_years (books):
    # ISBNs of the books and a progress bar
    isbns = books.loc [books ['Year-Of-Publication'] == 0] ['ISBN'].tolist ()
    pbar = tqdm (total = len (isbns), desc = "Obtaining missing book years from openlibrary.org", \
                bar_format = '{l_bar}{bar}|{n}/{total}, time elapsed: {elapsed}  ')

    # Get book year - use in async calls
    def get_year_async (isbn):
        try:
            data = get ('https://openlibrary.org/isbn/' + isbn + '.json').json ()
            year = findall (r'\d{4}', data ['publish_date'])
            return (isbn, 0 if len (year) != 1 else int (year [0]))
        except:
            return (isbn, 0)
        finally:
            pbar.update (1)

    # Create pool of threads and start looking for publication dates
    with ThreadPoolExecutor (64) as pool:
        result = pool.map (get_year_async, isbns)
        for index, year in result:
            books.loc [books ['ISBN'] == index, 'Year-Of-Publication'] = year

    pbar.close ()


# Obtains missing book titles from API
def get_titles (books):
    # ISBNs of the books
    isbns = books.loc [books ['Book-Title'].isna ()] ['ISBN'].tolist ()

    # Get book title - use in async calls
    def get_title_async (isbn):
        try:
            data = get ('https://openlibrary.org/isbn/' + isbn + '.json').json ()
            return (isbn, data ['title'])
        except:
            return (isbn, 'How to pass EODP')

    # Create pool of threads and start looking for publication dates
    with ThreadPoolExecutor (32) as pool:
        result = pool.map (get_title_async, isbns)
        for index, title in result:
            books.loc [books ['ISBN'] == index, 'Book-Title'] = title

