# LT2212 V19 Assignment 2

From Asad Sayeed's statistical NLP course at the University of Gothenburg.

My name: Elena Rodriguez 

## Additional instructions
+ Finding duplicates (in `gendoc.py`): I've added an extra argument, `-D`, to specify how to look for duplicated document vectors, either by value ("v") or by name ("n") (or ignore duplicates if not specified). The duplicates are printed out and removed from the dataframe. 
I've set it to look for duplicates by value, that is, if two documents have the same number of occurrences of every word they're discarted as duplicates. Which makes sense up to a point: if the vocabulary is cut down it might be the case that some documents coincide in the number of those most frequent words.
On the other hand, dismissing documents that share the same name might not be a good idea, if for instance the files are named as an enumeration "file1, file2,..". This is the case for the data we were given.

+ There is also an extra argument for `simdoc.py`, `-M` to print the results in markdown format. (This is simply to help me copy-paste the results as a table)

+ There are two bash scripts that take care of running gendoc and simdoc 8 times, with the required specifications. (Again this is most helpful to me for completing part 3). 

## File naming convention

I named them "output_" 01 to 08 corresponding to the subsections in the instructions, followed by the options specified for that file, T B and/or S

## Results and discussion

Overall, the mean values are somewhat consistent and the cosine similarity is higher when comparing vectors from the same topic (subfolder), which again is consistent and points out that there is, at least some, correlation between documents in the same topic.

### Vocabulary restriction.

I added the option for getting a restriction on the vocabulary of the 20%, rather than a fixed number, so it is independent of the input documents. I chose this cut in light of the Pareto Principle, which assumes that by getting the 20% most frequent words we are looking at roughly the 80% of the occurrences, which seems as a computationally reasonable tradeoff. 

### Result table
The following table contains the results from running `simdoc-py` over the output files 1-8. The "options" column specifies the arguments that were used; "cos_sim" 1 and 2 are simply the cosine similarities within topics (subfolders) 1 and 2; consequentely the last colum corresponds to the crossed cosine similarity.
| File | Options | cos_sim_1 | cos_sim_2 | cos_sim_12 | 
| --- | :---: | ---: | ---: | ---: | 
| 01  |    |  0.461  |  0.454  |  0.332  |
| 02  |  Bp  |  0.576  |  0.572  |  0.438  |
| 03  |  T  |  0.114  |  0.103  |  0.076  |
| 04  |  BpT  |  0.368  |  0.374  |  0.231  |
| 05  |  S100  |  0.577  |  0.568  |  0.442  |
| 06  |  S1000  |  0.461  |  0.454  |  0.332  |
| 07  |  TS100  |  0.304  |  0.327  |  0.18  |
| 08  |  TS1000  |  0.114  |  0.103  |  0.076  |  
> The option "Bp" means that `gendoc.py` was called with the argument -B with the option of getting the top 20% rather than a fixed number. For this data is around 205 words.



### The hypothesis in your own words

### Discussion of trends in results in light of the hypothesis

## Bonus answers
