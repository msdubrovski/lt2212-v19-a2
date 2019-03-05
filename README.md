# LT2212 V19 Assignment 2

From Asad Sayeed's statistical NLP course at the University of Gothenburg.

My name: *Elena Rodriguez* 

## Additional instructions
+ Finding duplicates (in `gendoc.py`): I've added an extra argument, `-D`, to specify how to deal with duplicated document vectors. 
My code looks for duplicated document vectors by value, that is, if two documents have the same number of occurrences of every word they're discarted as duplicates. Which makes sense up to a point: if the vocabulary is cut down it might be the case that some documents coincide in the number of the most frequent words.
On the other hand, dismissing documents that share the same name might no be a good idea, if for instance the files are named as an enumeration "file1, file2,..". This is the case for the data we were given.
 with choices "v" for values, and "n" for names. Not specifying this option will ignore duplicates.

+ There is also an extra argument for `simdoc.py`

+ There are two bash scripts that take care of running gendoc and simdoc 8 times. 

## File naming convention

I named them "output_" 1 to 8 corresponding to the subsections in the instructions. (**maybe I want another naming convencion hey!**)

## Results and discussion

From Part 1&2: The mean values are somewhat consistent and the cosine similarity is higher when comparing vectors from the same topic (subfolder), which again is consistent and points out that there is, at least some, relation between documents in the same topic.

### Vocabulary restriction.

(Write what you chose for the vocabulary restriction for output file
(2), you can give a brief impressionistic justification for why in one
sentence or less.)

### Result table
This is a sample table cos I havent decided on the -B restriction yet.

| File | cos_sim_1 | cos_sim_2 | cos_sim_12 |
| --- | ---: | ---: | ---: |
| try1  |  0.939  |  0.833  |  0.702  |

### The hypothesis in your own words

### Discussion of trends in results in light of the hypothesis

## Bonus answers
