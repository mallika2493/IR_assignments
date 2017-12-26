from collections import Counter
from collections import OrderedDict
import os
import csv
from math import log

path="parsed_pages/"
unigram_file_tf="unigram/unigram_tf.csv"
unigram_file_df="unigram/unigram_df.csv"
bigram_file_tf="bigram/bigram_tf.csv"
bigram_file_df="bigram/bigram_df.csv"
trigram_file_tf="trigram/trigram_tf.csv"
trigram_file_df="trigram/trigram_df.csv"
map_file="file_mapping.csv"
inverted_index = OrderedDict()

#IndexInfo Class stores Doc ID and count
class IndexInfo(object):
    docId = ""
    tf = 0
    def __init__(self,doc_id,count):
        self.docId=doc_id
        self.tf=count

def make_IndexInfo(doc_id,count):
    index_info = IndexInfo(doc_id,count)
    return index_info

# retrieves all the filenames in the path
def get_filenames():
    filenames= os.listdir(path)
    return filenames

# calculates the term frequency from the value list
def calculate_termf(value_list):
    count=0
    for value in value_list:
        count+=value.tf
    return count

# returns the document ID list
def get_doc_list(value_list):
    doc_list=list()
    for value in value_list:
        doc_list.append(value.docId)
    return doc_list

# creates the directory if not already present
def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_mapping(dict):
    with open(map_file, 'wb') as csv_file:
        writer_tf = csv.writer(csv_file)
        for key,value in dict.items():
                writer_tf.writerow([key, value])
        csv_file.close()


# writes dictionary into a file
def write_into_file(dict,file,flag):
    create_path(file.split("/")[0])
    with open(file, 'wb') as csv_file:
        writer_tf = csv.writer(csv_file)
        for tuple in dict:
            if flag == 0:
                writer_tf.writerow([tuple[0], tuple[1]])
            else:
                writer_tf.writerow([tuple[0], ' '.join(str(doc_id)for doc_id in tuple[1][0]),tuple[1][1]])
        csv_file.close()

# creates dictinary of term frequency, document frequency and dictionary that stores tf*idf values of unigrams
def write_index_info(dict,file_tf,file_df,flag):
    dict_tf = OrderedDict()
    dict_df = OrderedDict()
    dict_tfidf = OrderedDict()
    for key in dict:
            val=dict[key]
            len_val=len(val)
            dict_tf[key] = calculate_termf(val)
            dict_df[key] = [get_doc_list(dict[key]),len_val]
            if len_val == 0:
                print len_val
                dict_tfidf[key] = 0
            else:
                dict_tfidf[key] = dict_tf[key]*log(float(1)/len_val)
    write_into_file(sorted(dict_tf.items(),key=lambda t:t[1],reverse=True), file_tf,0)
    write_into_file(sorted(dict_df.items(),key=lambda  x:x[0]), file_df,1)
    if flag == 1:
        write_into_file(sorted(dict_tfidf.items(),key=lambda t:t[1]),"new_unigram/stop_words.csv",0)

#generates list of ngrams
def find_ngrams(file_con,n):
  return zip(*[file_con.replace("\n", " ").split()[i:] for i in range(n)])

#builds the index dictionary([term,[[docId1,tf1],[docId2,tf2],...]) for unigrams,bigrams and trigrams
def build_inverted_indexer():
    filenames = get_filenames()
    unigram = OrderedDict()
    bigram = OrderedDict()
    trigram = OrderedDict()
    file_map=OrderedDict()
    doc_num=0
    for filename in filenames:
        doc_num+=1
        fd=open(path+filename,"r")
        fileCon = fd.read()
        fd.close()
        counters = Counter(fileCon.strip().split())
        file_map[doc_num]=filename
        #build unigram dictionary
        for each_word in counters:
            unigram.setdefault(each_word,[]).append(make_IndexInfo(doc_num, counters[each_word]))

        #build bigram dictionary
        bigram_list_counter=Counter(find_ngrams(fileCon,2))
        for each_word in bigram_list_counter:
            bigram.setdefault(' '.join(each_word), []).append(make_IndexInfo(doc_num, bigram_list_counter[each_word]))

        #build trigram dictionary
        trigram_list_counter = Counter(find_ngrams(fileCon, 3))
        for each_word in trigram_list_counter:
            trigram.setdefault(' '.join(each_word), []).append(make_IndexInfo(doc_num, trigram_list_counter[each_word]))

    write_mapping(file_map)
    write_index_info(unigram, unigram_file_tf, unigram_file_df,1)
    write_index_info(bigram, bigram_file_tf, bigram_file_df,0)
    write_index_info(trigram, trigram_file_tf, trigram_file_df,0)


def main():
    build_inverted_indexer()

if __name__ == "__main__":main()
