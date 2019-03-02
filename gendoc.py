import os, sys, re
import glob
import argparse
import numpy as np
import pandas as pd

from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfTransformer


parser = argparse.ArgumentParser(description="Generate term-document matrix.")
parser.add_argument("-T", "--tfidf", action="store_true",
                    help="Apply tf-idf to the matrix.")
parser.add_argument("-S", "--svd", metavar="N", dest="svddims", type=int,
                    default=None,
                    help="Use TruncatedSVD to truncate to N dimensions")
parser.add_argument("-B", "--base-vocab", metavar="M", dest="basedims",
                    type=int, default=None,
                    help="Use the top M dims from the raw counts before further processing")
parser.add_argument("foldername", type=str,
                    help="The base folder name containing the two topic subfolders.")
parser.add_argument("outputfile", type=str,
                    help="The name of the output file for the matrix data.")

args = parser.parse_args()

print("Loading data from directory {}.".format(args.foldername))

if not args.basedims:
    print("Using full vocabulary.")
else:
    print("Using only top {} terms by raw count.".format(args.basedims))

if args.tfidf:
    print("Applying tf-idf to raw counts.")

if args.svddims:
    print("Truncating matrix to {} dimensions via singular value decomposition.".format(args.svddims))

print("Writing matrix to {}.".format(args.outputfile))

# extract subfolders and files names
foldername = args.foldername
subfolds = os.listdir(foldername)
file_list = [(subf, filename) for subf in subfolds for filename in os.listdir(foldername+subf)]

# read all files at once and extract vocabulary (with counts)
#myregex = r"[\d\.\,\:\;\!\*%&\?€#@£$∞§\|\[\]\(\){}\-\>\<]*"
myregex = r"[^a-zA-Z\s]+"
vocab = {}
for subf, filename in file_list:
    with open(foldername + "/" + subf + "/" + filename, "r", encoding = "utf-8") as f:
        read_file = re.sub(myregex, "", f.read()).lower()
        for word in read_file.split():
                vocab[word] = vocab.get(word, 0) +1

# sort vocab by frequency
vocab = [(w, vocab[w]) for w in sorted(vocab, key=vocab.get, reverse=True)]
vocab_list = [pair[0] for pair in vocab]
# filter vocab if specified
if args.basedims:
    vocab_list = vocab_list[:args.basedims]

# read again the files and store a document vector for each
vectors = []
for subf, filename in file_list:
    vector = {word:0 for word in vocab_list}
    with open(foldername + "/" + subf + "/" + filename, "r", encoding = "utf-8") as f:
        read_file = re.sub(myregex, "", f.read()).lower()
        for word in read_file.split():
            if word in vector.keys():
                vector[word] += 1
        # clear the vector to be, well, a vector
        v = list(vector.values())
        vectors.append(v)

# create a data frame, with the apropiate (multi)index
doc_df = pd.DataFrame(vectors)
doc_df.columns = vocab_list
topic_vec = [name[0] for name in file_list]
article_vec = [name[1] for name in file_list]
multindex = pd.MultiIndex.from_arrays([topic_vec, article_vec], names=('topic', 'document'))
doc_df.index = multindex

# taking care of duplicates ##############
# repeated BY NAME are: but this makes no sense because the names are the same in both subfolders
# doc_df["document2"] = doc_df.index.get_level_values("document")
# repeated = doc_df[doc_df.duplicated(subset= "document2")]
# if len(repeated) > 0:
#     print("The following %s repeated documents have been removed from the data set:" %len(repeated))
#     for item in repeated.index.get_level_values(1):
#         print(item)
#     doc_df = doc_df.drop_duplicates(subset = "document2")
#     doc_df = doc_df.drop("document2", axis = 1)
# repeated BY VALUE are:
repeated = doc_df[doc_df.duplicated()]
if len(repeated) > 0:
    print("The following %s repeated documents have been removed from the data set:" %len(repeated))
    print(repeated.index.get_level_values(1).values)
    doc_df = doc_df.drop_duplicates()
#doc_df.duplicated()
#doc_df = doc_df.drop_duplicates()

# tf-idf #######################################
#if args.tfidf:
    #X = doc_df.values
    #tfidf_transformer = TfidfTransformer()
    #X_tfidf = tfidf_transformer.fit_transform(X)
    #X_tfidf.shape
    #doc_tfidf = pd.DataFrame(X_tfidf)
    #doc_df = pd.DataFrame(X_tfidf)

# SVD #######################################
# if args.svd:
#     svd = TruncatedSVD(n_components=args.svddims, n_iter=7, random_state=42)
#     svd.fit(X)  
#     TruncatedSVD(algorithm='randomized', n_components=5, n_iter=7,
#         random_state=42, tol=0.0)


################ finally, ##############
# create an output file
doc_df.to_csv(path_or_buf = args.outputfile, header = True, index = True)
