#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 18:37:50 2022

@author: smitkadvani
"""


import os,math,json,glob,sys


stop_word = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "arent", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by","btw" "cant", "cannot", "could", "couldnt", "did", "didnt", "do", "does", "doesnt", "done","doing", "dont", "down", "during", "each", "even","few", "for", "from", "further", "had", "hadnt", "has", "hasnt", "have", "havent", "having", "he", "hed", "hell", "hes", "her", "here", "heres", "hers", "herself", "him", "himself", "his", "how", "hows", "i", "id", "ill", "im", "ive", "if", "in", "into", "is", "isnt", "it", "its", "its", "itself", "lets", "me", "more", "most", "mustnt", "my", "myself", "no", "nor", "not", "of", "off",
             "on", "once", "only", "or", "other", "ought", "our", "ours",	"ourselves", "out", "over", "own", "same", "shant", "she", "shed", "shell", "shes", "should", "shouldnt", "so", "some", "such", "than", "that", "thats", "the", "their", "theirs", "them", "themselves", "then", "there", "theres", "these", "they", "theyd", "theyll", "theyre", "theyve", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasnt", "we", "wed", "well", "were", "weve", "were", "werent", "what", "whats", "when", "whens", "where", "wheres", "which", "while", "who", "whos", "whom", "why", "whys", "with", "wont", "would", "wouldnt", "you", "youd", "youll", "youre", "youve", "your", "yours", "yourself", "yourselves"]
development_data = []

def read_file_recursively(model_parameter):
    true_count = 0
    total_count = 0
    print("Smit")
    outputfile = open("./nboutput.txt", "w+")
    
    for filename in glob.iglob(sys.argv[1] + '/' +'**/*.txt', recursive=True):
        if 'README.txt' in filename :
            continue
        test_file_content = read_text_file(filename)
        class_tags = classify(test_file_content,model_parameter) 
        final = class_tags[1] +  " " +  class_tags[0] + " " + filename
        outputfile.write(final+str("\n"))
    outputfile.close()

def read_text_file(file_path):
    file_content = ""
    with open(file_path, 'r') as f:
        file_content += f.read()
    # Removing punction while reading file
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in file_content:
        if ele == '\n':file_content = file_content.replace(ele, "")
        if ele in punc:file_content = file_content.replace(ele, "")
    return file_content

def readModel():
    file_path = './nbmodel.txt'
    with open(file_path) as json_file:
        model_data = json.load(json_file)
    return model_data

def classify(test_data,model_parameter):
    test_data = test_data.split(" ")

    total_final_prob = {}
    class_list = ['deceptive', 'truthful',
                  'positive', 'negative']
    total,vocal_len=0,int(model_parameter['vocab'])
    
    for class_ in class_list:
        temp = 0
        for word in test_data:
            word = word.lower()
            if word not in stop_word:
                temp += math.log((model_parameter['model_p'][class_][word] if word in model_parameter['model_p'][class_] else 0 +1)/(int(model_parameter['class_count'][class_])+vocal_len))
        total_final_prob[class_] = temp

    class_1 = 'positive' if total_final_prob['positive'] < total_final_prob['negative'] else 'negative'
    class_2 = 'truthful' if total_final_prob['truthful'] < total_final_prob['deceptive'] else 'deceptive'
    return [class_2,class_1]

if __name__ == "__main__":
    model_parameter = readModel()
    read_file_recursively(model_parameter)