# Contoh POSTagger sederhana dengan pendekatan statistika (metode decision tree)
# Ade Romadhony - Fakultas Informatika Universitas Telkom
# sumber: https://nlpforhackers.io/training-pos-tagger/

def read_dataset(fname):
    sentences = []
    tags = []
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    while idx_line < len(content):
        sent = []
        tag = []
        print('idx_line =')
        print(idx_line)
        while not content[idx_line].startswith('</kalimat'):
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                sent.append(content_part[0])
                tag.append(content_part[1])
            idx_line = idx_line + 1
        sentences.append(sent)
        tags.append(tag)
        idx_line = idx_line+2        
    return sentences, tags

def read_test_file(filename):
    
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    
    Sentences = []
    
    idx_line = 0
    kalimat = []
    while idx_line < len(content):
        while not content[idx_line].startswith('</kalimat'):
            if  content[idx_line].startswith('<kalimat'):
                kalimat = []
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                kalimat.append(content_part)
            idx_line = idx_line + 1
        Sentences.append(kalimat)
            
        idx_line = idx_line+1
    
    return Sentences

def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index],
        'prefix-1': sentence[index][0],
        'prefix-2': sentence[index][:2],
        'prefix-3': sentence[index][:3],
        'suffix-1': sentence[index][-1],
        'suffix-2': sentence[index][-2:],
        'suffix-3': sentence[index][-3:],
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
    }


 
def transform_to_dataset(sentences, tags):
    X, y = [], []
 
    for sentence_idx in range(len(sentences)):
        for index in range(len(sentences[sentence_idx])):
            X.append(features(sentences[sentence_idx], index))
            y.append(tags[sentence_idx][index])
 
    return X, y
 

 
sentences,tags = read_dataset('data_train.txt')

test_sentences = read_test_file('data_test.txt')
Test_Sentences = []
Test_Tags = []
for i, s in enumerate(test_sentences):
    Test_Sentences.append([x[0].lower() for x in s])
    Test_Tags.append([x[1] for x in s])
# print(sentences[0])
# print(tags[0])

# Split the dataset for training and testing
# cutoff = int(.75 * len(sentences))
training_sentences = sentences
test_sentences = Test_Sentences
training_tags = tags
test_tags = Test_Tags
 
#print(len(training_sentences))   
#print(len(test_sentences))         

X, y = transform_to_dataset(training_sentences, training_tags)
print('data training ke-0 =')
print(X[0])
print('label training ke-0 =')
print(y[0])

from sklearn import tree
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
 
clf = Pipeline([
    ('vectorizer', DictVectorizer(sparse=False)),
    ('classifier', tree.DecisionTreeClassifier(criterion='entropy'))
])
clf.fit(X, y)   
 
print('Training completed')

X_test, y_test = transform_to_dataset(test_sentences, test_tags)
 
print("Accuracy:")
print(clf.score(X_test, y_test))

# Test model yang sudah dilatih dengan kalimat masukan bebas
from nltk import word_tokenize

def pos_tag(sentence):
    tags = clf.predict([features(sentence, index) for index in range(len(sentence))])
    #return zip(sentence, tags)
    return tags
 
print(pos_tag(word_tokenize('kera makan pisang')))
 
