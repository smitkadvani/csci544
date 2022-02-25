from collections import defaultdict
from math import log
import sys, string, json, os

		
def viterbi(sent, mymod, prob_ttt, prob_wt, prob_tag, end_w):
	smooth = -8
	
	p_tag = 'START_TAG'

	pi = prob_ttt[p_tag]	
	words = sent.split(' ')
	w = words[0]
	
	vit_param = [defaultdict(int)]
	back_p = [defaultdict(int)]
	
	for curr_tag in prob_wt[w] if w in prob_wt else prob_ttt: 
		if curr_tag in pi:
			vit_param[0][curr_tag] += log(pi[curr_tag])
		else:
			vit_param[0][curr_tag] += smooth
		
		if w in prob_wt:
			vit_param[0][curr_tag] += log(prob_wt[w][curr_tag])
		else:
			vit_param[0][curr_tag] += log(prob_tag[curr_tag])

		back_p[0][curr_tag] = p_tag


	for i in range(1, len(words)):
		vit_param.append(defaultdict(int))
		w = words[i]
		back_p.append(defaultdict(int))
		for curr_tag in prob_wt[w] if w in prob_wt else prob_ttt:
			vit_param[i][curr_tag] = -float('inf')
			for p_tag in vit_param[i-1]:
				prob = vit_param[i-1][p_tag]

				if (p_tag in prob_ttt and curr_tag in prob_ttt[p_tag]):
					prob += log(prob_ttt[p_tag][curr_tag])
				else: 
					prob += smooth
				if w in prob_wt:
					prob += log(prob_wt[w][curr_tag])
				else: 
					prob += log(prob_tag[curr_tag])
				if vit_param[i][curr_tag] < prob:
					vit_param[i][curr_tag] = prob
					back_p[i][curr_tag] = p_tag

	end_prob = -float('inf')
	for last_tag in vit_param[-1]:
		final_state_transition = vit_param[-1][last_tag] + (log(end_w[w]) if w in end_w else smooth) + log(prob_wt[w][last_tag]) if w in prob_wt else log(prob_tag[last_tag])
		if end_prob < final_state_transition:
			end_prob = final_state_transition
			final_tag = last_tag

	state = final_tag
	ans = []
	for i in range(len(words)-1, -1, -1):
		ans.append(state)
		state = back_p[i][state]

	return ans[::-1]


def dec_pos(path, mymod, prob_ttt, prob_wt, prob_tag, end_w):
	with open(path,  encoding='utf-8') as f, open('hmmoutput.txt', 'w', encoding='utf-8') as out:
		for sent in f.read().split('\n'):
			
			line = ' '.join([f'{w}/{t}' for w, t in zip(sent.split(' '), viterbi(sent, mymod, prob_ttt, prob_wt, prob_tag, end_w)) if w and t]).rstrip()

			if line:
				out.write(line + '\n')

with open('hmmmodel.txt') as mod:
	mymod = json.load(mod)
	prob_wt = mymod['Prob_word_tag']
	prob_tag = mymod['Prob_tag']
	end_w = mymod['End_of_sentence']
	prob_ttt = mymod['Prob_tag_to_tag']
	
cmd_para = sys.argv[1]
dec_pos(cmd_para, mymod, prob_ttt, prob_wt, prob_tag, end_w)   