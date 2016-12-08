import requests
import sys
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import re
import json
import optparse

search_tree=dict()
patterns = [
        r"[Ss](\d+)[Ee](\d+)", 
        r"(\d+)[xX](\d+)",
        r"[Ss][Ee][Aa][Ss][Oo][Nn][%][2][0](\d+)"
          
    ]
parser = optparse.OptionParser('usage: %prog [options]')
parser.add_option("--update", "-u", dest="uflag",action="store_true", help="Update Data")
parser.add_option("--search", "-s", dest="keyword",action="store", help="Keywords")
#parser.add_option("--link", "-l", dest="ulink",action="store", help="New Database For Search")
parser.add_option("--name", "-n", dest="uname",action="store", help="Name of Database")

(options, args) = parser.parse_args()
def indexing(url,search_tree):
	print url
	if(url[-1] == '/'):
		html_page = urllib2.urlopen(url)
		soup = BeautifulSoup(html_page)
		i=0;
		for link in soup.findAll('a'):
			url= link.get('href')
			i=i+1
			
			if(i==1):
				start=url
				continue
			print start
			if("node-ecstatic" in url):
				break
			string=url[len(start)-3:]
			
			if(string[-1]=='/'):
				string=string[:-1]
			search_tree[string]=dict()
			indexing(str(base+url),search_tree[string])	
	else:
		search_tree["Link"]=url  
		sys.stdout.write('.')
		sys.stdout.flush()
def ksearch(level,words,flag):
	# print level.keys()
	# print words
	if "Link" in level.keys():
		if not words:
			print level["Link"]
		return 
	used=[]
	for j in level.keys():
		for i in words:

			reg=re.search(i,j,re.IGNORECASE)
			if reg:
				file=j
				used.append(j)
				temp=list(words)
				temp.remove(i)
				ksearch(level[file],temp,True)
				
	if flag:
		for j in level.keys():
			if j not in used:
				ksearch(level[j],words,True)
	else:
		for j in level.keys():
			if "Link" not in level[j].keys() and j not in used:
				ksearch(level[j],words,False)

			    
#Enter Link Here
url ="http://localhost:8081/" 
base="http://localhost:8081"
#Enter Link Here


if(options.uflag):
	
	
	indexing(url,search_tree)
	json.dump(search_tree, open(uname+'.dat', 'w'))
	sys.exit(2)
if(options.keyword is not None):
	keys=options.keyword.split(" ")
	with open(uname+'.dat') as data_file:    
		data = json.load(data_file)
		ksearch(data,keys,False)

#print search_tree



