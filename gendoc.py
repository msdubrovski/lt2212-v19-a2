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
                    default=None, type=str,
                    help="Use the top M dims from the raw counts before further processing. "
                        "if set to 'p' the top 20percent is taken.")
parser.add_argument("foldername", type=str,
                    help="The base folder name containing the two topic subfolders.")
parser.add_argument("outputfile", type=str,
                    help="The name of the output file for the matrix data.")
parser.add_argument("-D", "--duplicates", type=str, choices=["v", "n"],
                    help="how to look for duplicates, by 'value' or by 'name', if not specified they're ignored")

args = parser.parse_args()

print("Loading data from directory {}.".format(args.foldername))


if not args.basedims:
    print("Using full vocabulary.")
else:
    try:
        basedims = int(args.basedims)
        print("Using only top {} terms by raw count.".format(basedims))
    except ValueError:
        basedims = False
        print("Using top 20%p frequent words.")

if args.tfidf:
    print("Applying tf-idf to raw counts.")

if args.svddims:
    if not args.tfidf:
        print("Warning: You should convert to TF-IDF to perform SVM.")
        print("Truncating matrix to {} dimensions via singular value decomposition.".format(args.svddims))
    elif args.basedims and args.basedims < args.svddims:
        exit("Error: The dimensions of the vocabulary can't be smaller than the target SVM.")
    else:
        print("Truncating matrix to {} dimensions via singular value decomposition.".format(args.svddims))

print("Writing matrix to {}.".format(args.outputfile))

# extract subfolders and file names
if not re.search("/$", args.foldername):
    foldername = args.foldername + "/"
else: # im adding a final "/" to the path in case i forget to write it right =D
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
    if basedims:
        vocab_list = vocab_list[:basedims]
    else:
        basedims = len(vocab_list)*2 // 100
        vocab_list = vocab_list[:basedims]

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
if args.duplicates:
    # repeated BY NAME are: but this makes no sense because the names are the same in both subfolders
    if args.duplicates == "n":
        doc_df["document2"] = doc_df.index.get_level_values("document")
        repeated = doc_df[doc_df.duplicated(subset= "document2")]
        if len(repeated) > 0:
            print("The following %s repeated documents have been removed from the data set:" %len(repeated))
            for item in repeated.index.get_level_values(1):
                print(item)
            doc_df = doc_df.drop_duplicates(subset = "document2")
            doc_df = doc_df.drop("document2", axis = 1)
            multindex = doc_df.index

    # repeated BY VALUE are:
    if args.duplicates == "v":
        repeated = doc_df[doc_df.duplicated()]
        if len(repeated) > 0:
            print("The following %s repeated documents have been removed from the data set:" %len(repeated))
            print(repeated.index.get_level_values(1).values)
            doc_df = doc_df.drop_duplicates()
            multindex = doc_df.index

# tf-idf #######################################
if args.tfidf:
    tfidf_transformer = TfidfTransformer()
    X_tfidf = tfidf_transformer.fit_transform(doc_df.values).toarray()
    #X_tfidf.shape
    doc_df = pd.DataFrame(X_tfidf)
    doc_df.index = multindex

# SVD #######################################
if args.svddims:
    svd = TruncatedSVD(n_components = args.svddims, algorithm="randomized",
                        n_iter=5, random_state=None, tol=0.0)
    X_svd = svd.fit_transform(doc_df.values)
    doc_df = pd.DataFrame(X_svd)
    # the columns change but rows should be the same, we glue the (updated) multindex to it:
    doc_df.index = multindex

################ finally, ##############
# create an output file
doc_df.to_csv(path_or_buf = args.outputfile, header = True, index = True)

print("These are the first lines written in '%s'" %args.outputfile)
print(doc_df.iloc[:10])
