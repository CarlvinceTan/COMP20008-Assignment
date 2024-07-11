import pandas as pd
from preprocess.dictionaries import countries
from preprocess.regex_filters import *
from numpy import nan
from random import choices

# Preprocess users
def process_users (users, cs):
    cities, states = cs

    # Users - City
    users ['User-City'] = clean_user_text(users ['User-City'])

    # Users - State
    users ['User-State'] = clean_user_text(users ['User-State'])

    # Users - Country
    users.loc [users ['User-Country'].isna (), 'User-Country'] = ''
    users ['User-Country'] = users ['User-Country'].str.replace ('"', '').str.strip ().str.lower ()
    users.loc [users ['User-Country'].str.contains ('united sta'), 'User-Country'] = 'usa'  # for those 8 🦅🦅 users
    users.loc [users ['User-Country'].str.contains ('england'), 'User-Country'] = 'united kingdom'  # for those 5 🍵🍵 users
    users.loc [~(users ['User-Country'].isin (countries)), 'User-Country'] = ''
    users ['User-Country'] = empty_to_nan (users ['User-Country'])


    # Get most common places
    most_common_countries = users.groupby ('User-Country') ['User-State'].count ().sort_values (ascending = False).reset_index () ['User-Country'].to_list ()
    most_common_state = users.groupby ('User-Country') ['User-State'].apply (lambda x: x.value_counts ().idxmax () if not x.value_counts ().empty else nan).to_dict ()
    most_common_city = users.groupby ('User-State') ['User-City'].apply (lambda x: x.value_counts ().idxmax () if not x.value_counts ().empty else nan).to_dict ()
    most_common_city [nan] = nan

    # Assign user to one of the most common 10 countries with proper distribution
    def comuser (index):
        randcountry = choices (most_common_countries [:10], weights = range (100, 0, -10)) [0]
        users.at [index, 'User-Country'] = randcountry
        users.at [index, 'User-State'] = most_common_state [randcountry]
        users.at [index, 'User-City'] = most_common_city [most_common_state [randcountry]]
    
    # Fill user's city and state
    def fill_citystate (index, country):
        mcs = most_common_state [country]
        mcc = most_common_city [mcs]
        if pd.isnull (mcs) or pd.isnull (mcc):
            comuser (index)
        else:
            users.at [index, 'User-State'] = mcs
            users.at [index, 'User-City'] = mcc
    

    # fill missing countries
    for index, row in users.loc [users ['User-Country'].isna ()].iterrows ():
        # if city and state are missing, take the most popular [country, state, city]
        if pd.isnull (row ['User-State']) and pd.isnull (row ['User-City']):
            comuser (index)

        # if state is present, try get from dataset [country], otherwise most popular [country, state, city]
        elif not pd.isnull (row ['User-State']):
            matches = states.loc [states ['name'] == row ['User-State']]
            if len (matches) > 0:
                users.at [index, 'User-Country'] = matches ['country_name'].iloc [0]
            else:
                comuser (index)
        
        # if city is present, try get from dataset [country, state], otherwise most popular [country, state, city]
        elif not pd.isnull (row ['User-City']):
            matches = cities.loc [(cities ['name'] == row ['User-City']) & (cities ['state_name'] == row ['User-State'])]
            if len (matches) > 0:
                users.at [index, 'User-Country'] = matches ['country_name'].iloc [0]
            else:
                subm = cities.loc [cities ['name'] == row ['User-City']]
                if len (subm) > 0:
                    users.at [index, 'User-Country'] = subm ['country_name'].iloc [0]
                    users.at [index, 'User-State'] = subm ['state_name'].iloc [0]
                else:
                    comuser (index)


    # fill missing states
    for index, row in users.loc [users ['User-State'].isna ()].iterrows ():
        # if city is missing, take the most popular [state, city]
        if pd.isnull (row ['User-City']):
            fill_citystate (index, row ['User-Country'])
        
        # if city is present, try get from dataset [state], otherwise most popular [state, city]
        else:
            matches = cities.loc [(cities ['name'] == row ['User-City']) & (cities ['country_name'] == row ['User-Country'])]
            if len (matches) > 0:
                users.at [index, 'User-State'] = matches ['state_name'].iloc [0]
            else:
                subm = cities.loc [cities ['name'] == row ['User-City']]
                if len (subm) > 0:
                    users.at [index, 'User-Country'] = subm ['country_name'].iloc [0]
                    users.at [index, 'User-State'] = subm ['state_name'].iloc [0]
                else:
                    fill_citystate (index, row ['User-Country'])


    # fill missing cities with most popular [city]
    for index, row in users.loc [users ['User-City'].isna ()].iterrows ():
        city = most_common_city [row ['User-State']]
        if pd.isnull (city):
            fill_citystate (index, row ['User-Country'])
        else:
            users.at [index, 'User-City'] = city


    # Users - Age
    users ['User-Age'] = users ['User-Age'].str.replace ('"', '').astype ('Int16')
    users.loc [(users ['User-Age'] < 5) | (users ['User-Age'] > 116), 'User-Age'] = nan
    users ['User-Age'] = users ['User-Age'].fillna (int(users ['User-Age'].mean (skipna = True)))

    return users


