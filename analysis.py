import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# apply the min-max scaling in Pandas using the .min() and .max() methods
def min_max_scaling(brand,models,reviews):
    # Create dataframe and set brand as the index.
    df = pd.DataFrame(list(zip(brand, models, reviews)), columns = ['brand', 'num_models','num_reviews'])
    df.set_index("brand", inplace = True)
    # copy the dataframe
    df_norm = df.copy()
    # apply min-max scaling
    for column in df_norm.columns:
        df_norm[column] = (df_norm[column] - df_norm[column].min()) / (df_norm[column].max() - df_norm[column].min())
        
    print(df_norm)

# Prints out min,max,median,mean and skewness.
def get_summary_stats(brand,models,reviews):
    df = pd.DataFrame(list(zip(brand, models, reviews)), columns = ['brand', 'num_models','num_reviews'])
    print(df.agg({"num_models": ["min", "max", "median","mean", "skew"],"num_reviews": ["min", "max", "median","mean", "skew"]}))


# Creates a dual-axis bar chart.
def create_dualbar(brand,models,reviews):
    df = pd.DataFrame(list(zip(brand, models, reviews)), columns = ['brand', 'num_models','num_reviews'])
    df.set_index("brand", inplace = True)
    fig = plt.figure() # Create matplotlib figure

    ax = fig.add_subplot(111) # Create matplotlib axes
    ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.

    width = 0.4

    df.num_models.plot(kind='bar', color='red', ax=ax, width=width, position=1)
    df.num_reviews.plot(kind='bar', color='blue', ax=ax2, width=width, position=0)

    ax.set_ylabel('num_models')
    ax2.set_ylabel('num_reviews')

    plt.xticks(rotation=45)

    plt.show()