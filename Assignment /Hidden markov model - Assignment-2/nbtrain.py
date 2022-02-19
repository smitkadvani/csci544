import os
import sys
import glob,json
from collections import defaultdict
model_training = dict()
model_training['deceptive'] = dict()
model_training['truthful'] = dict()
model_training['positive'] = dict()
model_training['negative'] = dict()


tag_dict={}
def read_file_recursively(root_dir):
    for filename in glob.iglob(root_dir + '/' + '**/*isdt_train_tagged.txt', recursive=True):  
        print(filename)     
        test_file_content = read_text_file(filename)
        for word in test_file_content.split("\n"):
            parseSentence(word)

            
def read_text_file(file_path):
    file_content = ""
    with open(file_path, 'r') as f:
        file_content += f.read()
    return file_content


def parseSentence(sentence):
    for tagged_word in sentence.split(" "):
        if "//" in tagged_word:
            continue
        tag,word = tagged_word[::-1].split("/",1)
        word,tag = word[::-1],tag[::-1]
        if tag not in tag_dict:
            tag_dict[tag]=0
        else:
            tag_dict[tag]+=1
           


if __name__ == "__main__":
    #path = sys.argv[1]
    path = './hmm-training-data'
    read_file_recursively(path)
    print(tag_dict) 
    