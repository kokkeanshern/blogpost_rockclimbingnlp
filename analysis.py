import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Creates a dual-axis bar chart.
def create_dualbar(brand, models, reviews):
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

