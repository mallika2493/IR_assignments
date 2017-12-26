import os
from bs4 import BeautifulSoup
import io
import re
from collections import OrderedDict

folder="pages/"
parsed_path="parsed_pages/"
def clean(string):
    str=re.sub(r'(\[.+?\])', '', string) #removes citation
    str=re.sub(r'\,(?=[^0-9])','',str).rstrip(",") # remove comma except within digits
    str=re.sub(r'\.(?=[^0-9])', '', str).rstrip(".") # remove dot except within digits
    str=re.sub(r"[^\w\s,.-]|_", ' ', str)  #remvoes all the punctuations except for - , comma and dot
    return str.lower()

def get_filenames():
    if not os.path.exists(parsed_path):
        os.makedirs(parsed_path)
    filenames= os.listdir(folder)
    return filenames

def process_data():
        filenames=get_filenames()
        i=0
        counter=OrderedDict()
        for filename in filenames:
            with open(folder+filename,"r") as fd:
                new_filename=re.sub(r'\_*\-*','',filename)
                counter[new_filename]=1
                if os.path.isfile(os.path.join(parsed_path,"%s.txt" % new_filename)):
                    counter[new_filename]=counter[new_filename]+1
                    file_path=parsed_path+new_filename+"_"+str(counter[new_filename])
                else:
                    file_path=parsed_path+new_filename
                fil = open(file_path+".txt", "w")
                i=i+1
                print str(i)+" "+file_path
                fileCon=fd.read()
                #print fileCon
                soup = BeautifulSoup(fileCon,"html.parser")
                page_title = soup.title.text
                page_content=page_title.lower()
                fil.write(page_content.encode('utf8')+"\n")
                body=soup.find("div", {"id" : "mw-content-text"}).findAll(['p', 'h2', 'h3'])
                for b in body:
                    if b.parent is not None and b.parent.has_attr("id") and b.parent['id'] == "mw-content-text":
                        fil.write(clean(b.text).encode('utf8')+'\n')
                fil.close()
                fd.close()

process_data()



