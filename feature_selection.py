from sklearn.metrics import normalized_mutual_info_score, mutual_info_score

# Feature selection methods
def feature_selection(data, threshold, selection_type, display_scores = False):
    selected_features = []
    features = ['User-ID','User-City','User-State','User-Country','User-Age','ISBN','Book-Title','Book-Author','Year-Of-Publication','Book-Publisher'] # User-ID and ISBN were removed
    merged_ratings = [data[[feature, 'Book-Rating']] for feature in features]
    
    # Mutual information
    if selection_type == 0:
        for feature, merged_rating in zip(features, merged_ratings):
            MI = mutual_info_score(merged_rating[feature], merged_rating['Book-Rating'])
            if MI > threshold:
                selected_features.append(feature)
                if display_scores:
                    print(f'Mutual Information score for {feature}: {MI:.4f}')
    
    # Normalized mutual information
    elif selection_type == 1:
        for feature, merged_rating in zip(features, merged_ratings):
            nMI = normalized_mutual_info_score(merged_rating[feature], merged_rating['Book-Rating'])
            if nMI > threshold:
                selected_features.append(feature)
                if display_scores:
                    print(f'Normalized Mutual Information score for {feature}: {nMI:.4f}')

    return selected_features


