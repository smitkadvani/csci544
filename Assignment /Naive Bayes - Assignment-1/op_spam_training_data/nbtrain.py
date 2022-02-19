import os
import sys
import glob,json
stop_word = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "arent", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "cant", "cannot", "could", "couldnt", "did", "didnt", "do", "does", "doesnt", "doing", "dont", "down", "during", "each", "few", "for", "from", "further", "had", "hadnt", "has", "hasnt", "have", "havent", "having", "he", "hed", "hell", "hes", "her", "here", "heres", "hers", "herself", "him", "himself", "his", "how", "hows", "i", "id", "ill", "im", "ive", "if", "in", "into", "is", "isnt", "it", "its", "its", "itself", "lets", "me", "more", "most", "mustnt", "my", "myself", "no", "nor", "not", "of", "off",
             "on", "once", "only", "or", "other", "ought", "our", "ours",	"ourselves", "out", "over", "own", "same", "shant", "she", "shed", "shell", "shes", "should", "shouldnt", "so", "some", "such", "than", "that", "thats", "the", "their", "theirs", "them", "themselves", "then", "there", "theres", "these", "they", "theyd", "theyll", "theyre", "theyve", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasnt", "we", "wed", "well", "were", "weve", "were", "werent", "what", "whats", "when", "whens", "where", "wheres", "which", "while", "who", "whos", "whom", "why", "whys", "with", "wont", "would", "wouldnt", "you", "youd", "youll", "youre", "youve", "your", "yours", "yourself", "yourselves"]

model_training = dict()
model_training['deceptive'] = dict()
model_training['truthful'] = dict()
model_training['positive'] = dict()
model_training['negative'] = dict()

Vocab = set()
Prior = {'truthful': 0, 'deceptive': 0,'positive': 0, 'negative': 0}
Prior_P = {'truthful': 0, 'deceptive': 0,
         'positive': 0, 'negative': 0}
word_per_class = {'truthful': 0, 'deceptive': 0,'positive': 0, 'negative': 0}

def read_file_recursively(root_dir):
    invalid_file = True
    total  = 0
    for filename in glob.iglob(root_dir + '/' + '**/*.txt', recursive=True):
        if 'fold2' in filename or 'fold3' in filename or 'fold4' in filename :
            invalid_file = False
            if 'README.txt' in filename:
                continue
            if 'positive' in filename:
                current_class_2  = 'positive'
            if 'negative' in filename:
                current_class_2 = 'negative'
            if 'deceptive' in filename:
                current_class_1 = 'deceptive'
            if 'truthful' in filename:
                current_class_1 = 'truthful'
            if not invalid_file:
                Prior[current_class_1] += 1
                Prior[current_class_2] += 1

                test_file_content = read_text_file(filename)
                total+=1
                for word in test_file_content.split(" "):
                    if word.isalpha():
                        if word.lower() not in stop_word:
                            Vocab.add(word.lower())
                            word_per_class[current_class_1]+=1
                            word_per_class[current_class_2]+=1
                            if word.lower() not in model_training[current_class_1]:
                                model_training[current_class_1][word.lower()] = 1
                            else:
                                model_training[current_class_1][word.lower()] += 1
                            if word.lower() not in model_training[current_class_2]:
                                model_training[current_class_2][word.lower()] = 1
                            else: 
                                model_training[current_class_2][word.lower()] += 1
    #total = Prior['deceptive'] + Prior['truthful'] + Prior['positive'] + Prior['negative']
    for class_ in Prior:
        Prior_P[class_] /= total


def read_text_file(file_path):
    file_content = ""
    with open(file_path, 'r') as f:
        file_content += f.read()
    # Removing punction while reading file
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in file_content:
        if ele == '\n':
            file_content = file_content.replace(ele, "")
        if ele in punc:
            file_content = file_content.replace(ele, "")
    return file_content


if __name__ == "__main__":
    path = sys.argv[1]
    read_file_recursively(path)
    model={'prior':Prior_P, 'vocab':len(Vocab), 'model_p':model_training,'class_count':word_per_class}
    with open('nbmodel.txt', 'w') as outfile:
        json.dump(model, outfile)