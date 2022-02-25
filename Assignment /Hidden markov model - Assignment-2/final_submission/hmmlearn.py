import sys, json, os
from collections import defaultdict
from math import log
hyper_tunning = 3
def trainmodel(dir):
	prob_tag = defaultdict(int)
	end_w = defaultdict(int)
	prob_ttt = defaultdict(lambda : defaultdict(int))
	prob_w = defaultdict(lambda : defaultdict(int))
	
	with open(dir,  encoding='utf8') as file_content, open('hmmmodel.txt', 'w') as output_write:
		lines = file_content.read().split('\n')
		t_tags = 0
		
		for line in lines:
			prev_tag = 'START_TAG'
			prob_tag[prev_tag]+=1
			t_tags+=1

			for word, tag in map(lambda x: (x[:x.rfind('/')], x[x.rfind('/')+1:]), line.rstrip().split(' ') + ['END/END']):
				prob_tag[tag] = prob_tag[tag] + 1
				t_tags = t_tags + 1
				prob_ttt[prev_tag][tag] = prob_ttt[prev_tag][tag] + 1
				prob_w[word][tag]+=1
				prev_tag = tag
			end_w[word]+=1
		for word in end_w:
			end_w[word]/=prob_tag['START_TAG']
			
		for prev_tag in prob_ttt:
			for curr_tag in prob_ttt:
				nume = (prob_ttt[prev_tag][curr_tag] + hyper_tunning)
				deno = (prob_tag[prev_tag] + len(prob_ttt))
				prob_ttt[prev_tag][curr_tag] =  nume/deno 

		for tag in prob_tag:
			prob_tag[tag]= prob_tag[tag]/t_tags
			
		json.dump({'Prob_tag_to_tag':prob_ttt, 
		'Prob_word_tag':prob_w, 
		'Prob_tag':prob_tag, 
		'End_of_sentence':end_w}, 
		output_write, 
		indent=2)
cmd_param = sys.argv[1]
trainmodel(cmd_param)