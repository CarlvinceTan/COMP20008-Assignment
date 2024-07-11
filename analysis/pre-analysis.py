from re import search

# Check user id
def check_user_id(dataset):
    text = r'[\d\s]'
    for user_id in dataset["User-ID"]:
        match = search(text, user_id)
    if match == True:
        return "Has user id containing number or whitespace"
    else:
        return 'All user id meet with requirement'

# Check book isbn
def check_isbn(dataset):
    for isbn in dataset["ISBN"]:
        if len(isbn) != 13:
            return 'Has isbn that lenth < 13'
        else:
            return 'All user id meet with requirement'

# Check book rating
def check_book_rating(dataset):
    for rating in dataset["Book-Rating"]:
        if rating < 1 and rating > 10:
            return 'Has rating out of range'
        else:
            return 'All rating meet with requirement'

# Check user city
def check_user_citys(dataset):
    text = r'\d?\s?'
    for city in dataset["User-City"]:
        match = search(text, city)
    if match == True or len(dataset["User-City"]):
        return "Has user city containing number or whitespace"
    else:
        return 'All user city  id meet with requirement'

# Check user state
def check_user_state(dataset):
    text = r'\d\s'
    for city in dataset["User-City"]:
        match = search(text, city)
    if match == True:
        return "Has user city containing number or whitespace"
    else:
        return 'All user city  id meet with requirement'

# Check user age
def check_user_age(dataset):
    text = r'[^0-9\s]'
    for user_age in dataset['User-Age']:
        match = search(text, user_age)
        #based on the information from web adn document, the most old people are 116 and most young age that alawys to use phone is 5
        if match == True
            return "Has user age containing word or symbol"
        if user_age < 5 or user_age >116:
            return 'has user age out of reasonable range'
        else:
            return 'All user age meet with requirement'


