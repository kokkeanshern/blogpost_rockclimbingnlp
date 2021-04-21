import matplotlib.pyplot as plt
import numpy as np

# Display a piechart with option to save as image file.
def create_barchart(vals, mylabels, save):
    vals = np.array(vals)
    plt.bar(mylabels, vals)
    plt.show()

    if save == True:
        plt.savefig('reviews_distribution.png')