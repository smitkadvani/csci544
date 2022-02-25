from collections import defaultdict
from math import log
import sys, string, json, os

class HMM:
	def __init__(self):		
		with open('hmmmodel.txt') as mod:
			model = json.load(mod)
			self.ptt = model['PTT']
			self.pwt = model['PWT']
			self.pt = model['PT']
			self.ends = model['ENDS']

	def viterbi(self, sent):
		LAPLACE = -8
		viterbi = [defaultdict(int)]
		backpointer = [defaultdict(int)]

		prev_tag = 'START_TAG'

		pi = self.ptt[prev_tag]

		words = sent.split(' ')

		w = words[0]

		for curr_tag in self.pwt[w] if w in self.pwt else self.ptt:
			viterbi[0][curr_tag] += log(pi[curr_tag]) if curr_tag in pi else LAPLACE
			viterbi[0][curr_tag] += log(self.pwt[w][curr_tag]) if w in self.pwt else log(self.pt[curr_tag])
			backpointer[0][curr_tag] = prev_tag


		for i in range(1, len(words)):
			w = words[i]
			viterbi.append(defaultdict(int))
			backpointer.append(defaultdict(int))

			for curr_tag in self.pwt[w] if w in self.pwt else self.ptt:
				viterbi[i][curr_tag] = -float('inf')

				for prev_tag in viterbi[i-1]:
					prob = viterbi[i-1][prev_tag]
					prob += log(self.ptt[prev_tag][curr_tag]) if (prev_tag in self.ptt and curr_tag in self.ptt[prev_tag]) else LAPLACE
					prob += log(self.pwt[w][curr_tag]) if w in self.pwt else log(self.pt[curr_tag])

					if viterbi[i][curr_tag] < prob:
						viterbi[i][curr_tag] = prob
						backpointer[i][curr_tag] = prev_tag

		end_prob = -float('inf')
		for last_tag in viterbi[-1]:
			final_state_transition = viterbi[-1][last_tag] + (log(self.ends[w]) if w in self.ends else LAPLACE) + log(self.pwt[w][last_tag]) if w in self.pwt else log(self.pt[last_tag])
			if end_prob < final_state_transition:
				end_prob = final_state_transition
				final_tag = last_tag

		state = final_tag
		ans = []
		for i in range(len(words)-1, -1, -1):
			ans.append(state)
			state = backpointer[i][state]

		return ans[::-1]


	def decode(self, path):
		with open(path,  encoding='utf-8') as f, open('hmmoutput.txt', 'w', encoding='utf-8') as out:
			for sent in f.read().split('\n'):
				
				line = ' '.join([f'{w}/{t}' for w, t in zip(sent.split(' '), self.viterbi(sent)) if w and t]).rstrip()

				if line:
					out.write(line + '\n')


if __name__=='__main__':
	HMM().decode(sys.argv[1])   