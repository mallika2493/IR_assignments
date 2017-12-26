#assignment 2 task 2
import collections
from collections import OrderedDict
from math import pow, log
filename = "G1.txt"
#filename = "wt2g_inlinks.txt"
page_results="G1_pagerank_results.txt"
perplixity_file="G1_perplixity.txt"
sink_node_filename="sinknodes_G1.txt"
no_inlink_filename="no_inlinks_G1.txt"
#directed graph
dict_graph = OrderedDict()
#Page rank dictionary that stores the page ranks for each page
PR = OrderedDict()
#new page rank computation for each page
newPR = OrderedDict()
#stores the outlink count for each page
out_link_count=OrderedDict()
#keeps track of the count value of each link in the directed graph
counters=OrderedDict()
#list of perplixites for all iterations
perplexities=list()
#set of inlinks for a given page
M = set()
# set of sink nodes
sink_nodes = set()
# set of inlinks
pages_with_no_in_links = set()
#set of all pages
P = set()
#damping factor
d=float(0.85)
N=0

#this method does the following preproccessing
#i)stores the directed graph from the file into the dictionary
#ii)computes the outlink count for each link
#iii) stores the sink nodes
def preprocessing_data():
    with open(filename) as fd:
        file_con=fd.read()
        #stores the count value for each link from the file
        counters = collections.Counter(file_con.strip().split())
        fd.close()
    #reads each line from the file
    for x in file_con.strip().split("\n"):
        if x.count(" ") > 0:
            key,value = x.strip(" ").split(" ", 1)
            #print key+" "+value
            val=str(value).split(" ")
            P.add(key)
            #stores in dictionary
            dict_graph[key]=val
            for k in list(val):
                    P.add(k)
                    #updating the outlink count
                    if k in out_link_count:
                        out_link_count[k]+=1
                    else:
                        out_link_count[k]=1
        else:
            dict_graph[x]=list()
            #print x
            pages_with_no_in_links.add(x.strip(" "))
            key=x
            P.add(key)
        # storing sink nodes
        if counters[key] == 1:
            sink_nodes.add(key)
            out_link_count[key] = 0

#calculates perplixity for a given page rank
def calculate_perplexity(page_rank):
    perplixity=pow(2,calculate_shannon_entropy(page_rank))
    return perplixity

#calculates the shannon entropy for the page rank
def calculate_shannon_entropy(page_rank):
    shannon_entropy=0
    for i in page_rank:
        shannon_entropy+=page_rank[i]*log(page_rank[i],2)
        #print -1*shannon_entropy
    return -1*shannon_entropy

def write_page_ranks_to_file(PR):
    fil = open(page_results, "w")
    for key in PR:
        fil.write(key + " " + str(PR[key]))
        fil.write("\n")
    fil.close()

def write_perplixities_to_file():
    fil = open(perplixity_file, "w")
    for key in perplexities:
        #print str(key)
        fil.write(str(key))
        fil.write("\n")
    fil.close()

def write_sink_nodes_and_empty_linkcount_to_file():
    fil = open(sink_node_filename, "w")
    for key in sink_nodes:
        #print str(key)
        fil.write(str(key))
        fil.write("\n")
    fil.close()
    fil1 = open(no_inlink_filename, "w")
    for key1 in pages_with_no_in_links:
        #print str(key1)
        fil1.write(str(key1))
        fil1.write("\n")
    fil1.close()


def page_rank_algorithm():
    N = len(P)
    no_of_iterations = 1
    for p in P:
        PR[p] = float(1) / N
    new_perplexity=calculate_perplexity(PR)
    perplexities.append(new_perplexity)
    while no_of_iterations <=4:
            sinkPR=0
            for page_in_sink_nodes in sink_nodes:
                    sinkPR+=PR[page_in_sink_nodes]
            for p1 in P:
                newPR[p1] = (1 - d)/N
                newPR[p1] += (d*sinkPR)/N
                M=dict_graph[p1]
                if len(M):
                    for q in M:
                        L=out_link_count[q]
                        newPR[p1] += d*float(PR[q])/L
            for each_page in P:
                PR[each_page]=newPR[each_page]
            old_perplexity = new_perplexity
            new_perplexity = calculate_perplexity(PR)
            #print new_perplexity
            perplexities.append(new_perplexity)
            if abs(new_perplexity - old_perplexity) < 1:
                no_of_iterations += 1
            else:
                no_of_iterations = 1
    write_page_ranks_to_file(OrderedDict(sorted(PR.items(),key=lambda t:t[1],reverse=True)))
    write_perplixities_to_file()
    write_sink_nodes_and_empty_linkcount_to_file()


def main():
    preprocessing_data()
    page_rank_algorithm()

if __name__ == "__main__":main()
