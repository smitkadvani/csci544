import os
import sys
import glob,json, math
from collections import defaultdict
import numpy as np 
model_training_transition = dict()
total_word = []
lam = 1


def read_file_recursively(root_dir):
    for filename in glob.iglob(root_dir + '/' + '**/*isdt_train_tagged.txt', recursive=True):  
        test_file_content = read_text_file(filename)
        for sentence in test_file_content.split("\n"):
            parseSentence(sentence)
        tags_index = (list(tag_dict.keys()))
        tags_index.append("BEG")
        for tag in tags_index : 
            transitionMatrix[tag]={}
            transitionSum[tag] = 1
            for tag1 in tags_index:
                transitionMatrix[tag][tag1] = lam
        for tag in tags_index:
            emissionMatrix[tag] = {}
            emissionSum[tag] = 1
            for word in total_word:
                emissionMatrix[tag][word] = 1
        for sentence in test_file_content.split("\n"):
            parseSentenceEmission(sentence)
    return tags_index
     
def read_text_file(file_path):
    file_content = ""
    with open(file_path, 'r') as f:
        file_content += f.read()
    return file_content

def parseSentence(sentence):
    sentence = sentence.split(" ")
    for tagged_word in sentence:
        if "//" in tagged_word:
            continue
        tag,word = tagged_word[::-1].split("/",1)
        word,tag = word[::-1],tag[::-1]
        if word.isdigit() :
            word = "0"
        if word not in total_word:
            total_word.append(word)
        if tag not in tag_dict:
            tag_dict[tag]=1.0
        else:
            tag_dict[tag]+=1.0


def parseSentenceEmission(sentence):
    sentence = sentence.split(" ")
    prev_tag = "BEG"
    for tagged_word in sentence:
        if "//" in tagged_word:
            continue
        tag,word = tagged_word[::-1].split("/",1)
        word,tag = word[::-1],tag[::-1]
        if word.isdigit():
            word="0"
        transitionMatrix[prev_tag][tag] += 1.0
        transitionSum[prev_tag]+=1.0
        emissionMatrix[tag][word] += 1.0
        emissionSum[tag]+=1.0
        prev_tag = tag

if __name__ == "__main__":
    #path = sys.argv[1]
    tag_dict={}
    tags_index=[]
    transitionSum = {}
    emissionSum = {}
    transitionMatrix = dict()
    emissionMatrix = dict()
    BEG_OF_SENTENCE="__"
    path = './hmm-training-data'
    tags_index  = read_file_recursively(path)
    
    for tag in tags_index : 
        for tag1 in tags_index:
            transitionMatrix[tag][tag1] /= (transitionSum[tag])
            transitionMatrix[tag][tag1] = math.log(transitionMatrix[tag][tag1],2.7)
    for tag in tags_index:
        for word in total_word:
            emissionMatrix[tag][word] /= (emissionSum[tag])
            emissionMatrix[tag][word] = math.log(emissionMatrix[tag][word],2.7)
   

    tag_dict = dict(sorted(tag_dict.items(), key=lambda item: item[1]))
    model_parameter = {'tags_list':tags_index,'word_list':total_word,'transition_table':transitionMatrix,'emission_table':emissionMatrix,'tag_dict':tag_dict}
    with open('hmmmodel.txt', 'w') as outfile:
        json.dump(model_parameter,outfile)

