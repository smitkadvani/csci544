import json 
#model_parameter = 
#{'tags_list':tags_list,'word_list':total_word,
#'transition_table':tranmision_prob,
#'emission_table':emission_prob}
Tunning_parameter = -7.0
def readModeData():
    file_path = './hmmmodel.txt'
    with open(file_path) as json_file:
        model_data = json.load(json_file)
    return model_data

def parseSentence(sentence): 
    sentence = sentence.split(" ")
    viterbi_mat = []
    backpointer = []
    for __ in sentence:
        viterbi_mat.append(dict()) 
        backpointer.append(dict())
    prev = "BEG"
    initial_word  = sentence[0]
    for index_of, state in enumerate(tags_list):
        tagTotag = float(transition_table_tagTotag[prev][state])
        if initial_word in word_list:
            wordTotag = float(emission_table_wordTotag[state][initial_word])
        else:
            wordTotag = Tunning_parameter
        viterbi_mat[0][state] = tagTotag + wordTotag
    
    for word_index, word in enumerate(sentence):
        if word_index == 0:
            continue
        temporary_value = float('-inf')
        probable_tag = defaultTag
        for index_of_tag, state in enumerate(tags_list):
            for prev_state_, value in (viterbi_mat[word_index-1].items()):
                tagTotag = float(transition_table_tagTotag[prev_state_][state])
                if word in word_list:
                    wordTotag = float(emission_table_wordTotag[state][word])
                else:
                    wordTotag = Tunning_parameter
                if value + tagTotag + wordTotag > temporary_value:
                    temporary_value = value+tagTotag+wordTotag
                    probable_tag = prev_state_     
            viterbi_mat[word_index][state] = temporary_value
            backpointer[word_index][state] = probable_tag
        
    bestpathprob = [float('-inf') for _ in range(len(sentence)+1)]
    bestpathtag = [0 for _ in range(len(sentence)+1)]
    word_index = len(sentence)-1
    while word_index > 0:
        max_prob = float('-inf')
        for tag, tag_value in viterbi_mat[word_index].items():
            if tag_value > max_prob:
                max_prob = tag_value
                bestpathtag[word_index] = backpointer[word_index][tag]
        word_index -= 1
               
    
    for index, word in enumerate(sentence):
        sentence[index] = sentence[index] + "/" + tags_list[bestpathtag[index]]
    return " ".join(sentence)

def read_text_file(file_path):
    file_content = ""
    with open(file_path, 'r') as f:
        file_content += f.read()
    return file_content
'''

model_parameter = {'tags_list':tags_list,'word_list':total_word,'transition_table':transitionMatrix,'emission_table':emissionMatrix,'tag_dict':tag_dict}
    
'''
model_data = readModeData()
tags_list = model_data['tags_list']
word_list = model_data['word_list']
transition_table_tagTotag = model_data['transition_table']
emission_table_wordTotag = model_data['emission_table']
tag_dict = model_data['tag_dict']
defaultTag = list(tag_dict.items())[0][0]
root_dir = "./hmm-training-data/it_isdt_dev_raw.txt"
file_data = read_text_file(root_dir)
file_ = open('hmmoutput.txt','w')
for sentence in file_data.split('\n'):
    output = parseSentence(sentence)
    file_.write(output+"\n")
    print(output)
