from collections import defaultdict,OrderedDict,Counter
from math import log,sqrt
import os
import csv

dict_df = OrderedDict()

dest_folder="results/"
file="cosine_similiarity_"
cosine_simularity=OrderedDict()

path="../parsed_pages/"
def get_filenames():
    return os.listdir(path)
filenames=get_filenames()
queries=["global warming potential","green power renewable energy","solar energy california","light bulb bulbs alternative alternatives"]
system_name="COSINE_SIM"

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

def counters_all_docs():
    counter_docs=OrderedDict()
    for filename in filenames:
        fd = open(path + filename, "r")
        fileCon = fd.read()
        fd.close()
        counter_docs[filename] = Counter(fileCon.strip().split())
        #tf_idfs[filename]=compute_tfidf_in_doc(counter_docs[filename])
    return counter_docs

all_counters=counters_all_docs()

# returns the document ID list
def get_doc_list(value_list):
    doc_list=list()
    for value in value_list:
        doc_list.append(value.docId)
    return doc_list



def store_tfidfs(unigram):
    tf_idf=OrderedDict()
    for key in unigram:
            val=unigram[key]
            len_val=len(val)
            #dict_df[key] = len_val
            if len_val == 0:
                print len_val
                tf_idf[key] = 0
            else:
                tf_idf[key] = log(float(1000)/len_val)
    return tf_idf



def build_inverted_indexer():
    filenames = get_filenames()
    unigram = OrderedDict()
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
    return unigram

# creates the directory if not already present
def create_path(path):
     if not os.path.exists(path):
       os.makedirs(path)

#query_id Q0 doc_id rank CosineSim_score system_name
def write_simalirity_matrix(query_id,sorted_consine_simularity):
    create_path(dest_folder)
    with open(dest_folder+file+str(query_id)+".csv", 'wb') as csv_file:
        writer_tf = csv.writer(csv_file)
        limit=0
        for tuple in sorted_consine_simularity:
            if limit >= 100:
                break
            limit+=1
            print "DOCID:"+str(tuple[0])+"|"+str(tuple[1])
            writer_tf.writerow([query_id,"Q0",tuple[0], tuple[1],system_name])

def calculate_query_magnitude(query_tf):
    sum=0.0
    for term in query_tf:
        sum+=pow(query_tf[term],2)
    return sum


def calculate_doc_magnitude(filename,dict_tfidf):
    doc_mag = 0
    counters=all_counters[filename]
    for term in counters:
        if term in dict_tfidf:
            doc_mag += pow(counters[term]*dict_tfidf[term], 2)
    return doc_mag

def compute_cosine_similarity(query_id,query,dict_tfidf):
    query_tf=Counter(query.split())
    query_magnitude = calculate_query_magnitude(query_tf)
    for filename in filenames:
        similarity_numerator = 0
        doc_magnitude = calculate_doc_magnitude(filename,dict_tfidf)
        flag=0
        counters = all_counters[filename]
        i = 0
        for term in query_tf:
            if term not in counters:
                i = i + 1
                if i==len(query_tf):
                    cosine_simularity[filename] = 0
                    flag=1
                continue
            else:
                query_tfidf = query_tf[term]
                doc_tfidf=dict_tfidf[term]
                similarity_numerator+=query_tfidf*counters[term]*doc_tfidf
        if flag == 0:
            magnitude_sum=sqrt(query_magnitude)*sqrt(doc_magnitude)
            similarity=float(similarity_numerator)/magnitude_sum
            cosine_simularity[filename]=similarity
    write_simalirity_matrix(query_id,sorted(cosine_simularity.items(),key=lambda t:t[1],reverse=True))




def main():
    unigram=build_inverted_indexer()
    dict_tfidf = store_tfidfs(unigram)
    query_id=0
    for query in queries:
        query_id+=1
        compute_cosine_similarity(query_id,query,dict_tfidf)

if __name__ == "__main__":main()
