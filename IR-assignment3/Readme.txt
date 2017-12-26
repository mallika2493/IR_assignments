This is the readme file for IR assignment 3

Language: Python
Version: 2.7.10

Please extract and install from beautifulsoup4-4.5.0.tar.gz package in order to run the scripts. It is given as part of the assignment zip folder

Steps to run:

Task 1
parse_source_pages.py reads through the raw html docs and does the job of parsing(removes punctuations where required and performs case folding)
parsed_source_pages folder contains the parsed document files


Task 2
Run command: python inverted_indexer.py 
This python file iterates through the corpus parsed pages and generates the unigram,bigram and trigram files for term frequency and document frequency

Below are the 6 files which contain the term frequency and document frequency:
folder unigram contains below files
1. unigram_tf.csv : contains the term frequency for each unigram(n=1) in the folder name unigram. The file contains data in the format below
[column1:term(unigram) column2:frequency]

2. unigram/unigram_df.csv : contains the document frequency for each unigram(n=1) in the folder name unigram. The file contains data in the format below
[column1:term column2:[DOCID1 DOCID2 ..] column3: document frequency]

folder bigram contains below files
3. bigram_tf.csv : contains the term frequency for each bigram(n=2) in the folder name bigram. The file contains data in the format [column1:term(bigram) column2:frequency]

4. bigram_df.csv : contains the document frequency for each bigram(n=2) in the folder name bigram. The file contains data in the format [column1:term(bigram) column2:[DOCID1 DOCID2 ..] column3: document frequency]

folder trigram contains below files
5. trigram_tf.csv : contains the term frequency for each trigram(n=3) in the folder name trigram. The file contains data in the format [column1:term(trigram) column2:frequency]

6. trigram_df.csv : contains the document frequency for each trigram(n=3) in the folder name trigram. The file contains data in the format [column1:term(trigram) column2:[DOCID1 DOCID2 ..] column3: document frequency] 
 
file_mapping.csv contains the mapping of doc id to the doc name

Task3
task3.docx contains the stop words and the explanation for task3

Bonus
zipian_curve.png contains the zipians curve plotting for n=1,2,3
