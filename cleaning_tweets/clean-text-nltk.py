file_name = 'metamorphosis-clean.txt'
file = open(file_name, 'r')
text = file.read()
file.close()

from nltk import sent_tokenize
sentences = sent_tokenize(text)
print(sentences[0])