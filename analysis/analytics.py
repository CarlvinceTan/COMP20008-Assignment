import pandas as pd
from numpy import array
from seaborn import heatmap
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix


# Ploat average rating for authors and countries
def avg_ratings(data):
    # Prepare data
    ratings_by_country = data [['User-Country', 'Book-Rating']].groupby ('User-Country').agg (['count', 'mean']).reset_index ()
    ratings_by_country = ratings_by_country.drop (ratings_by_country.loc [ratings_by_country ['Book-Rating'] ['count'] < 5].index).reset_index (drop = True)
    ratings_by_book = data [['Book-Author', 'Book-Rating']].groupby ('Book-Author').agg (['count', 'mean']).reset_index ()
    ratings_by_book = ratings_by_book.drop (ratings_by_book.loc [ratings_by_book ['Book-Rating'] ['count'] < 250].index).reset_index (drop = True)

    # Plot settings
    fig = plt.figure (figsize = (40, 8))
    fig.subplots_adjust (bottom = 0.3)
    def apply_plot_settings ():
        plt.xticks (rotation = 90)
        plt.yticks (ticks = [x/2 for x in range (1, 20)])
        plt.grid (axis = 'y', which = 'major')
        plt.ylabel ('Rating')

    # Plot for countries
    plt.bar (ratings_by_country ['User-Country'].apply (lambda x: x.title ()), ratings_by_country ['Book-Rating'] ['mean'])
    apply_plot_settings ()
    plt.xlabel ('Countries')
    plt.title ('Countries Average Rating')
    plt.savefig ('graphs/Countries Average Ratings.png', bbox_inches = 'tight')
    plt.cla ()

    # Plot for authors
    plt.bar (ratings_by_book ['Book-Author'].apply (lambda x: x.title ()), ratings_by_book ['Book-Rating'] ['mean'])
    apply_plot_settings ()
    plt.xlabel ('Authors')
    plt.title('Authors Average Rating')
    plt.savefig('graphs/Authors Average Ratings.png', bbox_inches = 'tight')
    plt.close()


# Plot age vs rating distribution
def age_vs_rating(data):
    scatter = data[['User-Age','Book-Rating']]
    scatter = scatter.dropna(subset=['User-Age', 'Book-Rating'])
    plt.scatter(scatter['User-Age'], scatter['Book-Rating'])
    plt.yticks (ticks = range (1, 11))
    plt.xlabel('User Age')
    plt.ylabel('Book Rating')
    plt.title('Book ratings distribution across users ages')
    plt.savefig('graphs/Age vs Rating.png')
    plt.close()


# Plot confusion matrices
def confusion_matrix_graph(list_true, list_predicted, title):
    cm = confusion_matrix(list_true, list_predicted, labels=range(11))
    plt.figure(figsize=(8, 6))
    ax = heatmap(cm, annot=True, fmt='d', cmap='plasma', cbar=True)#, xticklabels=range(1, 11), yticklabels=range(1,11))
    plt.tick_params ('y', left=False, labelleft=False, right=True, labelright=True, labelrotation=0)
    plt.xlabel('Predicted ratings')
    plt.ylabel('True ratings')

    # Set label and save to proper file depending on model type
    if title == 'kNN':
        plt.title('Confusion Matrix For kNN Model')
        plt.savefig('graphs/Confusion Matrix for kNN Model.png')
    else:
        plt.title('Confusion Matrix For DT Model')
        plt.savefig('graphs/Confusion Matrix for DT Model.png')
    plt.close()


# Plot clusters
def fig_clusters(clustered_data):
    plt.figure(figsize=(10, 10))
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'brown', 'magenta', 'cyan', 'teal']
    for i, cluster in enumerate(clustered_data.values()):
        cluster = array(cluster)
        if cluster.ndim == 1:
            cluster = cluster.reshape(-1, 1)
        plt.scatter(cluster[:, 0], cluster[:, 1], color=colors[i], label=f'Cluster {i+1}')

    # Draw
    plt.xlabel('User Age')
    plt.ylabel('Book Rating')
    plt.title('Clustered Users')
    plt.legend()
    plt.grid()
    plt.savefig('graphs/Clustered Plots.png')
    plt.close()


# Plot rating counts
def rating_amount_table():
    lis = {
        0:[0,0,164],1:[79,0,229],2:[147,0,359],3:[321,0,1119],4:[433,331,2662],5:[2767,199,1814],
        6:[1982,3971,4375],7:[4127,13772,5492],8:[5469,1978,3622],9:[3700,2894,3309],10:[4120,0,0]
    }
    
    # Code to obtain data above (needs to be ran in main.py)
    '''
        print(new_data['Book-Rating'].value_counts())
        print(predicted_ratings_1.value_counts())
        print(predicted_ratings_2.value_counts())
    '''
    df = pd.DataFrame.from_dict(lis, orient='index', columns=['True number of Ratings', 'Predicted number of Ratings (kNN)', 'Predicted number of Ratings (DT)'])

    # Convert DataFrame to a table
    fig, ax = plt.subplots(figsize=(10, 8))
    table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center', cellLoc='center')

    # Adjust layout
    ax.axis('off')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    plt.title('Actual vs Predicted Ratings')
    plt.savefig('graphs/Actual vs Predicted Ratings Table.png')
    plt.close()


# Plot knn accuracy vs number of neighbours
def accuracy_line_graph():
    x = [10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370, 390, 410, 430, 450]
    y = [
        0.1883344135, 0.2039749406, 0.2147332037, 0.2180168503, 0.2209980557, 0.2225102614, 0.2260963491, 0.22786779,
        0.2286022899, 0.2292503781, 0.2299416721, 0.2301577014, 0.2319291424, 0.2321451717, 0.2323179952, 0.2332253186,
        0.2326636423, 0.2333117304, 0.2340462303, 0.2338734068, 0.2340462303, 0.2340894362, 0.2346511126
    ]

    # Code to obtain data above (needs to be ran in main.py)
    ''' 
    for i in range(5,460, 10):
        train_with_kNN(data, new_data, selected_features_MI, i, True)
    '''

    # Adding labels and title, plotting
    plt.plot(x, y, marker='o', color='blue', linestyle='-')
    plt.xlabel('K-neighbours')
    plt.ylabel('Accuracy')
    plt.title('Accuracy vs Number of Neighbours')
    plt.grid()
    plt.savefig('analysis/Accuracy vs Number of Neighbours.png')
    plt.close()
