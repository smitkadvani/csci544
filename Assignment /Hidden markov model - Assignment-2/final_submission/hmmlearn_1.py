import sys, json, os
from collections import defaultdict
from math import log


def train(path):

	ptt = defaultdict(lambda : defaultdict(int))
	pwt = defaultdict(lambda : defaultdict(int))
	pt = defaultdict(int)
	ends = defaultdict(int)
	with open(path,  encoding='utf8') as f, open('hmmmodel.txt', 'w') as out:
		sents = f.read().split('\n')
		total_tags = 0
		for sent in sents:
			prev_tag = 'START_TAG'
			pt[prev_tag]+=1
			total_tags+=1

			for word, tag in map(lambda x: (x[:x.rfind('/')], x[x.rfind('/')+1:]), sent.rstrip().split(' ') + ['END/END']):
				pt[tag]+=1
				total_tags+=1
				ptt[prev_tag][tag]+=1
				pwt[word][tag]+=1
				prev_tag = tag

			ends[word]+=1

		for word in ends:
			ends[word]/=pt['START_TAG']

		for prev_tag in ptt:
			for curr_tag in ptt:
				ptt[prev_tag][curr_tag] = (ptt[prev_tag][curr_tag] + 1) / (pt[prev_tag] + len(ptt))

		for tag in pt:
			pt[tag]/=total_tags
			
		json.dump({'PTT':ptt, 'PWT':pwt, 'PT':pt, 'ENDS':ends}, out, indent=2)



train(sys.argv[1])