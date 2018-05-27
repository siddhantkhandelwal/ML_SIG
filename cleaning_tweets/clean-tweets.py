import sys
import re
import os

filein_name = sys.argv[1]

output_dir_name = "cleaning-stages"
if not os.path.exists(output_dir_name):
    os.makedirs(output_dir_name)

output_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_dir_name)

class clean_tweets:
    
    text = ''
    
    def __init__(self, text):
        self.text = text
        self_text_temp = []
        print("\n\nThe first 100 characters of the input file: \n%s" % self.text[:100])
        # print("\n\nNow Lower-casing text")
        # self.text = self.text.lower()        
        self.remove_sentiments()
        
    def remove_sentiments(self):
        print('Removing Sentiments.')
        file_temp = open(os.path.join(output_dir_path, 'sentiments-removed-'+ filein_name), 'w+')
        for line in self.text.splitlines():
            line_temp_out = line
            pattern =  re.compile(r':: \w+')
            line_temp_out = re.sub(pattern, '', line_temp_out)
            file_temp.write(line_temp_out + '\n')
        file_temp.seek(0)
        self.text = file_temp.read()
        
    def remove_at_mentions(self):
        print("Removing '@' from @mentions.")
        file_temp = open(os.path.join(output_dir_path, 'atmentions-removed-'+ filein_name), 'w+')
        for line in self.text.splitlines():
            line_temp_out = line
            pattern =  re.compile(r'@\w+')
            line_temp_out = re.sub(pattern, '**NAME**', line_temp_out)
            file_temp.write(line_temp_out + '\n')
        file_temp.seek(0)
        self.text = file_temp.read()
    
    def remove_hash_tags(self):
        print("Removing '#' from hashtags. ")
        file_temp = open(os.path.join(output_dir_path, 'hashtags-removed-'+ filein_name), 'w+')
        for line in self.text.splitlines():
            line_temp_out = line
            pattern =  re.compile(r'#')
            line_temp_out = re.sub(pattern, '', line_temp_out)
            file_temp.write(line_temp_out + '\n')
        file_temp.seek(0)
        self.text = file_temp.read()

    def remove_emoji_smileys(self):
        print("Removing Unicode Emojis & Smileys.")
        file_temp = open(os.path.join(output_dir_path, 'emojis-smileys-removed-'+ filein_name), 'w+')
        for line in self.text.splitlines():
            line_temp_out = line
            #Regex Pattern taken from: https://gist.github.com/admackin/0b677738a4b5648d307c
            pattern_emojis =  re.compile(r'[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]', re.VERBOSE)
            #Regex Pattern taken from: https://github.com/s/preprocessor/blob/master/preprocessor/defines.py
            pattern_smileys = re.compile(r"(?:X|:|;|=)(?:-)?(?:\)|\(|O|D|P|S){1,}", re.IGNORECASE)
            line_temp_out = re.sub(pattern_emojis, '', line_temp_out)
            line_temp_out = re.sub(pattern_smileys, '', line_temp_out)
            file_temp.write(line_temp_out + '\n')
        file_temp.seek(0)
        self.text = file_temp.read()
    
    def remove_reserved_words(self):
        print("Removing Reserved Words - RT and FAV.")
        file_temp = open(os.path.join(output_dir_path, 'reserved-words-removed-'+ filein_name), 'w+')
        for line in self.text.splitlines():
            line_temp_out = line
            pattern =  re.compile(r' rt|fav ')
            line_temp_out = re.sub(pattern, '', line_temp_out)
            file_temp.write(line_temp_out + '\n')
        file_temp.seek(0)
        self.text = file_temp.read()



filein_name = sys.argv[1]
if len(sys.argv) == 2:
    fileout_name = "clean-" + filein_name
else:
    fileout_name = sys.argv[2]
filein = open(filein_name, 'r')
fileout = open(fileout_name, 'w')
filein_text = filein.read()

ct = clean_tweets(filein_text)
ct.remove_at_mentions()
ct.remove_hash_tags()
ct.remove_emoji_smileys()
ct.remove_reserved_words()