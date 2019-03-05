import os, sys
import argparse
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import math


parser = argparse.ArgumentParser(description="Compute some similarity statistics.")
parser.add_argument("vectorfile", type=str,
                    help="The name of the input file for the matrix data.")
parser.add_argument("-M", "--markdown", action="store_true",
                    help="Get the output in markdown format.")
                

args = parser.parse_args()
vectorfile = args.vectorfile

print("Reading matrix from {}.".format(args.vectorfile))

# read csv
doc_csv = pd.read_csv(vectorfile, sep=',', delimiter=None, header='infer', names=None)
multindex = pd.MultiIndex.from_arrays([doc_csv["topic"], doc_csv["document"]], names=('topic', 'document'))
doc_csv.index = multindex
doc_csv = doc_csv.drop(["topic", "document"], axis=1)

# cosine similarity of every vector of one topic againt every vector of the same topic
def get_cos_sim1(some_df):
    sim = cosine_similarity(some_df)
    # the cosine_similarity function returns a simmetric matrix, any row/column contains all the values we need:
    mean = (sum(sim[0]) - 1) / len(sim[0]) # we substract that 1 to not count the similarity with the vector with itself
    return round(mean, 3)

means_pairs = list()
for topic in doc_csv.index.levels[0]:
    mean = get_cos_sim1(doc_csv.loc[topic])
    means_pairs.append((topic, round(mean, 3) )) # store values to print later
    
topics = doc_csv.index.levels[0]
X = doc_csv.loc[topics[0]]
Y = doc_csv.loc[topics[1]]
mean = sum(sum(cosine_similarity(X, Y) )) / (len(X) * len(Y))
means_pairs.append(("all_topics", round(mean, 3) ))

if not args.markdown:
    for i in range(2):
        print("The mean of the cosine similarity of every pair of different vectors of "
                "the topic '%s' is %s" % (means_pairs[i][0], means_pairs[i][1]))

    print("The mean of the cosine similarity of every pair of "
          "different vectors of different topics is %s" % means_pairs[2][1])

else: # Return a table in markdown format
    print("| File | Options | cos_sim_1 | cos_sim_2 | cos_sim_12 |", "\n|",
            "--- | :---: | ---: | ---: | ---: |", "\n|",
            vectorfile.split("_")[1], " | ",
            vectorfile.split("_")[2][:-4], " | ",
            means_pairs[0][1], " | ",
            means_pairs[1][1], " | ",
            means_pairs[2][1], " | ", "\n")
