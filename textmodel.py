# Text Model

import math

def clean_text(txt):
    """ takes a string of text txt as a parameter and returns a list containing the words in txt after it has been “cleaned”
    """
    txt = txt.replace('.', '').replace(',', '').replace('?', '').replace('!', '') \
          .replace(';', '').replace(':', '').replace('"', '').lower().split()
    return txt

def stem(s):
    """ accepts a string  s as a parameter. Then return the stem of s
    """
    if s[-1:] == 's':
        if len(s) < 4:
            stem = s
        elif s[-2] == 'e':
            stem = s[:-2]
        else:
            stem = s[:-1]
    elif s[-4:] == 'able' or s[-4:] == 'ible':
        if len(s) < 5:
            stem = s
        else:
            stem = s[:-4]
    elif s[-2:] == 'en':
        stem = s[:-2]
    elif s[-2:] == 'er':
        stem = s[:-2]
    elif s[-3:] == 'ful':
        stem = s[:-3]
    elif s[-3:] == 'ion':
        stem = s[:-3]
    elif s[-4:] == 'less'or s[-4:] == 'ness':
        stem = s[:-4]
    elif s[-3:] == 'ing':
        stem = s[:-3]
    else:
        stem = s
    return stem

def compare_dictionaries(d1, d2):
    """ compute and return their log similarity score of d1 and d2
    """
    score = 0
    total = 0
    for i in d1:
        total += d1[i]
    
    for word in d2:
        if word in d1:
            score += d2[word] * math.log(d1[word] / total)
        else:
            score += d2[word] * math.log(0.5 / total)
    return score


def run_tests():
    """ Test """
    source2 = TextModel('shakespeare')
    source2.add_file('shaks12.txt')
    
    source1 = TextModel('rowling')
    source1.add_file('rolling.txt')

    
    new1 = TextModel('fitzerald')
    new1.add_file('fitzerald.txt')
    new1.classify(source1, source2)
    
    new2 = TextModel('orwell')
    new2.add_file('george_orwell.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('wr112')
    new3.add_file('wr112.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('wr120')
    new4.add_file('wr120.txt')
    new4.classify(source1, source2)
    
class TextModel:
    """ blueprint for objects that model a body of text
    """

    def __init__(self, model_name):
        """ constructs a new TextModel object
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punc_freq = {}
        
    def __repr__(self):
        """ Return a string representation of the TextModel.
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of punctuation frequencies: ' + str(len(self.punc_freq)) + '\n'
        return s
    
    def add_string(self, s):
        """ Analyzes the string txt and adds its pieces
            to all of the dictionaries in this text model.
        """
        length = 0
        for i in range(len(s)):
            if s[i] == '.':
                sentence = s[:i]
                previous = length
                length = len(sentence.split(' '))
                if (length - previous) not in self.sentence_lengths:
                    self.sentence_lengths[length - previous] = 1
                else:
                    self.sentence_lengths[length - previous] += 1
                    
        for char in s:
            if char in '!"#$%&' or char in "'()*+, -./:;<=>?@[\]^_`{|}~":
                if char not in self.punc_freq:
                    self.punc_freq[char] = 1
                else:
                    self.punc_freq[char] += 1
                     
        word_list = clean_text(s)
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1

        # Add code to update other feature dictionaries.
        for w in word_list:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else: 
                self.word_lengths[len(w)] += 1
       
        for w in word_list:
            w = stem(w)
            if w not in self.stems:
                self.stems[w] = 1
            else:
                self.stems[w] +=1
        
        
    
        
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to the model
        """
        file = open(filename, 'r', encoding='utf8', errors='ignore')
        text = file.read()
        file.close()
        self.add_string(text)
        
    def save_model(self):
        """ saves the TextModel object self by writing its various feature dictionaries to files
        """
        file_words = open((self.name + '_' + 'words'), 'w')
        file_word_lengths = open((self.name + '_' + 'word_lengths'), 'w')
        file_stems = open((self.name + '_' + 'stems'), 'w')
        file_sentence_lengths = open((self.name + '_' + 'sentence_lengths'), 'w')
        file_punc_freq = open((self.name + '_' + 'punc_freq'), 'w')
        file_words.write(str(self.words))
        file_word_lengths.write(str(self.word_lengths))
        file_stems.write(str(self.stems)) 
        file_sentence_lengths.write(str(self.sentence_lengths)) 
        file_punc_freq.write(str(self.punc_freq)) 
        file_words.close()
        file_word_lengths.close()
        
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object from their files and assigns them to the attributes of the called TextModel
        """
        file_words = open((self.name + '_' + 'words'), 'r')
        file_word_lengths = open((self.name + '_' + 'word_lengths'), 'r')
        file_stems = open((self.name + '_' + 'stems'), 'r')
        file_sentence_lengths = open((self.name + '_' + 'sentence_lengths'), 'r')
        file_punc_freq = open((self.name + '_' + 'punc_freq'), 'r')
        words_text = file_words.read()
        word_lengths_text = file_word_lengths.read()
        stems_text = file_stems.read()
        sentence_text = file_sentence_lengths.read()
        punc_text = file_punc_freq.read() 
        file_words.close()
        file_word_lengths.close()
        file_stems.close()
        file_sentence_lengths.close()
        file_punc_freq.close()
        self.words = eval(words_text)
        self.word_lengths = eval(word_lengths_text)
        self.stems = eval(stems_text)
        self.sentence_lengths = eval(sentence_text)
        self.punc_freq = eval(punc_text)
        
    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores measuring the similarity of self and other
        """
        score_list = []
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punc_score = compare_dictionaries(other.punc_freq, self.punc_freq)
        score_list = [word_score] + [word_lengths_score] + [stems_score] + [sentence_lengths_score] + [punc_score]
        return score_list
        
        
    def classify(self, source1, source2):
        """ compares the called TextModel object (self) to two other “source” TextModel objects (source1 and source2) 
            and determines which of these other TextModels is the more likely source of the called TextModel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for ' + source1.name + ':' + str(scores1))
        print('scores for ' + source2.name + ':' + str(scores2))
        count_scores1 = 0
        count_scores2 = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                count_scores1 += 1
            elif scores2[i] > scores1[i]:
                count_scores2 += 1
            else:
                count_scores1 += 1
                count_scores2 += 1
        
        if count_scores1 > count_scores2:
            print(self.name + ' is more likely to have come from ' + source1.name)
        else:
            print(self.name + ' is more likely to have come from ' + source2.name)
        
        
        
        
        
        
        
    