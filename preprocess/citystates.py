import pandas as pd
from preprocess.regex_filters import *

# Get world cities and states from https://github.com/dr5hn/countries-states-cities-database
def get_citystates ():
    source = 'https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/'

    # Get and preprocess cities
    cities = pd.read_csv (source + 'cities.csv')
    cities = cities [['name', 'state_name', 'country_name']]
    cities ['name'] = clean_user_text (cities ['name'])
    cities ['state_name'] = clean_user_text (cities ['state_name'])
    cities ['country_name'] = clean_user_text (cities ['country_name'])
    cities.loc [cities ['country_name'] == 'united states', 'country_name'] = 'usa'

    # Get and preprocess states
    states = pd.read_csv (source + 'states.csv')
    states = states [['name', 'country_name']]
    states ['name'] = clean_user_text (states ['name'])
    states ['country_name'] = clean_user_text (states ['country_name'])
    states.loc [states ['country_name'] == 'united states', 'country_name'] = 'usa'

    return (cities, states)

