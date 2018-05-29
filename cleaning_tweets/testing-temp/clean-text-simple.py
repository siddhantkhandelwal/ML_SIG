filename = "metamorphosis-clean.txt"
file = open(filename, 'r')
text = file.read()
file.close()

words = text.split()
words = [word.lower() for word in words]

import string
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in words]
print(stripped[:100])