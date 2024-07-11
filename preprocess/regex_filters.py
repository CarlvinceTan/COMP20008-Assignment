from unicodedata import normalize
from numpy import nan
from preprocess.dictionaries import *
from gc import collect

# Remove n/a, na, nan and none strings
def remove_na(series):
    s1 = series.str.replace(r'\bn/a\b', '', regex=True)
    s2 = s1.str.replace(r'\bna\b', '', regex=True)
    s3 = s2.str.replace(r'\bnan\b', '', regex=True)
    s4 = s3.str.replace(r'\bnone\b', '', regex=True)
    series = s4

    del s1, s2, s3, s4
    collect ()
    return series

def remove_bracketed_info(series):
    return series.str.replace(r'\(.*?\)', '', regex=True)

def remove_symbols_exclude_period(series):
    return series.str.replace(r'[^a-z\.]', ' ', regex=True)

def remove_symbols_exclude_colon(series):
    return series.str.replace(r'[^\sa-z:]', '', regex=True)

def remove_symbols(series):
    return series.str.replace(r'[^\sa-z]', '', regex=True)

def normalize_to_ascii(text):
    return text if text is nan else normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii')

def remove_short_form(series): 
    return series.str.replace(r'\b\w+\.\b', '', regex=True)

def remove_extra_spaces(series):
    return series.str.replace(r'\s+', ' ', regex=True).str.strip()

def empty_to_nan(series):
    return series.replace('', nan)

# Clean user columns
def clean_user_text(series):
    series = series.str.lower()
    series = remove_na(series)
    series = series.apply(normalize_to_ascii)
    series = remove_bracketed_info(series)
    series = remove_symbols_exclude_period(series)
    collect ()
    
    # Replace short forms and delete others not in the dictionary
    for short, long_ in short_forms.items():
        series = series.str.replace(short, long_, regex = True)

    series = remove_short_form(series)
    series = remove_symbols(series)
    series = remove_extra_spaces(series)
    series = empty_to_nan(series)

    collect ()
    return series

# Clean book title
def clean_title(series):
    series = series.str.lower()
    series = remove_na(series)
    series = series.apply(normalize_to_ascii)
    series = remove_symbols_exclude_colon(series)
    series = remove_bracketed_info(series)
    series = remove_extra_spaces(series)
    series = empty_to_nan(series)

    collect ()
    return series

# Clean book author
def clean_author(series):
    series = series.str.lower()
    series = remove_na(series)
    series = series.apply(normalize_to_ascii)
    series = remove_symbols(series)
    series = remove_extra_spaces(series)
    series = empty_to_nan(series)

    collect ()
    return series

# Clean book publisher
def clean_publisher(series):
    series = series.str.lower()
    series = remove_na(series)
    series = series.apply(normalize_to_ascii)
    series = remove_bracketed_info(series)
    collect ()

    # Delete words in dictionary
    for word in key_words:
        series = series.str.replace(word, '', regex = True)
    for country in countries:
        series = series.str.replace(country, '', regex = True)

    series = remove_extra_spaces(series)
    series = empty_to_nan(series)

    collect ()
    return series

