import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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

    # Rotate labels and make them fit in the plot.
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)
    plt.tight_layout()

    plt.show()

# Produces positivity, negativity, neutrality and compound scores per review.
def get_sentiment_score(review):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # oject gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(review)

    # print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    # print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    # print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
    # print("sentence has a compound score of ", sentiment_dict['compound'])

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        classification = 'pos'
  
    elif sentiment_dict['compound'] <= - 0.05 :
        classification = 'neg'
  
    else :
        classification = 'neu'

    compound_score = sentiment_dict['compound']

    return classification, compound_score

# Create positivity rate which is num_pos/num_reviews*100.
def positivity_rate(classification, num_reviews):
    pos_rate = (classification.count('pos')/num_reviews)*100
    return pos_rate

def quad_plot(num_reviews, pos_rate, model):
    fig, ax = plt.subplots()
    ax.scatter(pos_rate, num_reviews)

    for i, txt in enumerate(model):
        ax.annotate(txt, (pos_rate[i], num_reviews[i]), fontsize=8)
    
    plt.xlabel("Positivity Rate")
    plt.ylabel("Number of Reviews") 

    plt.axhline(y=sum(num_reviews)/len(num_reviews), color='k', linestyle='--', linewidth=1)           
    plt.axvline(x=sum(pos_rate)/len(pos_rate), color='k',linestyle='--', linewidth=1) 

    plt.show()