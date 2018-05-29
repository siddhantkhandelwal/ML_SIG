import sys
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re

class clean_tweets:
    
    text = ''
    tokens = []
    lower_tokens = []
    stop_words = []
    words = []
    stemmed_words = []
        
    
    def __init__(self, text):
        self.text = text
        print("The first 100 characters of the input file: %s" % self.text[:100])
        self.remove_sentiments()
        self.tokens = word_tokenize(text)
        self.lower_tokens = [token.lower() for token in self.tokens]
        self.stop_words = set(stopwords.words('english'))

    def remove_sentiments(self):
        file_temp = open('file_temp', 'w+')
        for line in self.text.splitlines():
            line_temp_out = line
            sentiment_pattern =  re.compile(r':: \w+')
            line_temp_out = re.sub(sentiment_pattern, '', line_temp_out)
            file_temp.write(line_temp_out + '\n')
        self.text = file_temp.read()

    def remove_non_alphabetics(self, stripped):
        self.words = [word for word in stripped if word.isalpha()]

    def remove_punctuation(self):
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in self.lower_tokens]
        self.remove_non_alphabetics(stripped)
    
    def filter_stop_words(self):
        self.words = [word for word in self.words if not word in self.stop_words]

    def stemming_words(self):
        porter = PorterStemmer()
        self.stemmed_words = [porter.stem(word) for word in self.words]


filein_name = sys.argv[1]
if len(sys.argv) == 2:
    fileout_name = "clean - " + filein_name
else:
    fileout_name = sys.argv[2]
filein = open(filein_name, 'r')
fileout = open(fileout_name, 'w')
filein_text = filein.read()

ct = clean_tweets(filein_text)
ct.remove_punctuation()
ct.filter_stop_words()
ct.stemming_words()