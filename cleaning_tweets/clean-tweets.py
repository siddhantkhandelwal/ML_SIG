'''
Cleans Tweets/Texts for ML applications.
Loads the text into memory and runs the following preprocessing tasks on the text:

    removes sentiments: e.g. '::joy, ::anger'
    replaces @ mentions with **NAME**, finds occurences of the text of @ mention everywhere in the file, and replaces them with **NAME**
    removes # tags
    removes emojis, smileys, special characters
    removes reserved words, extra spaces
    spell_check using hunspell

Stores the present state of the text at every stage in "cleaning-stages" directory in the current directory.
The final cleaned text is saved as "clean-" + filename in the working directory   
'''

import sys
import re
import os
import hunspell

filein_name = sys.argv[1]

output_dir_name = "cleaning-stages"
if not os.path.exists(output_dir_name):
    os.makedirs(output_dir_name)
output_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_dir_name)

class clean_tweets:
    
    text = ''
    temp_text = ''
    handles_list = []
    
    def __init__(self, text):
        self.text = text
        print("\n\nThe first 100 characters of the input file: \n%s" % self.text[:100])
        # print("\n\nNow Lower-casing text")
        # self.text = self.text.lower()        
    
    def pattern_substitute(self, stageout_name, pattern):
        file_temp = open(os.path.join(output_dir_path, stageout_name+filein_name), 'w+')
        for line in self.text.splitlines():
            line_temp_out = line
            line_temp_out = re.sub(pattern, '', line_temp_out)
            file_temp.write(line_temp_out + '\n')
        file_temp.seek(0)
        self.text = file_temp.read()
        
    def remove_sentiments(self):
        print('Removing Sentiments.')
        pattern =  re.compile(r':: \w+')
        self.pattern_substitute('sentiments-removed-', pattern)
        
    def remove_at_mentions(self):
        print("Removing '@' from @mentions.")
        file_temp = open(os.path.join(output_dir_path, 'atmentions-removed-'+ filein_name), 'w+')
        for line in self.text.splitlines():
            line_temp_out = line
            pattern =  re.compile(r'@\w+')
            matches = re.findall(pattern, line_temp_out)
            for match in matches:
                self.handles_list.append(match[1:])
            line_temp_out = re.sub(pattern, '**NAME**', line_temp_out)
            file_temp.write(line_temp_out + '\n')
        file_temp.seek(0)
        self.text = file_temp.read()
    
    def remove_hash_tags(self):
        print("Removing '#' from hashtags. ")
        pattern =  re.compile(r'#')
        self.pattern_substitute('hashtags-removed-', pattern)
        
    def remove_emoji_smileys_special(self):
        print("Removing Unicode Emojis, Smileys and Special characters.")
        file_temp = open(os.path.join(output_dir_path, 'emojis-smileys-specials-removed-'+ filein_name), 'w+')
        for line in self.text.splitlines():
            line_temp_out = line
            #Regex Pattern taken from: https://gist.github.com/admackin/0b677738a4b5648d307c
            pattern_emojis =  re.compile(r'[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]', re.VERBOSE)
            #Regex Pattern taken from: https://github.com/s/preprocessor/blob/master/preprocessor/defines.py
            pattern_smileys = re.compile(r"(?:X|:|;|=)(?:-)?(?:\)|\(|\[|\]|O|D|P|S){1,}", re.IGNORECASE)
            pattern_specials = re.compile(r"[\\/\{\}\(\)]")
            pattern_new_words = re.compile(r"([a-z0-9])([A-Z])")
            line_temp_out = re.sub(pattern_emojis, '', line_temp_out)
            line_temp_out = re.sub(pattern_smileys, '', line_temp_out)
            line_temp_out = re.sub(pattern_specials, '', line_temp_out)
            line_temp_out.strip()
            line_temp_out = re.sub(pattern_new_words, r'\1 \2', line_temp_out)
            file_temp.write(line_temp_out + '\n')
        file_temp.seek(0)
        self.text = file_temp.read()
    
    def remove_reserved_words(self):
        print("Removing Reserved Words - RT and FAV, and basic formatting.")
        file_temp = open(os.path.join(output_dir_path, 'reserved-words-removed-'+ filein_name), 'w+')
        for line in self.text.splitlines():
            line_temp_out = line
            pattern_reserved =  re.compile(r' rt|fav ', re.IGNORECASE)
            pattern_extra_spaces = re.compile(r' +')
            line_temp_out = re.sub(pattern_reserved, '', line_temp_out)
            line_temp_out = re.sub(pattern_extra_spaces, ' ', line_temp_out)
            for handle in self.handles_list:
                if handle in line_temp_out:
                    line_temp_out = str.replace(line_temp_out, handle, '**NAME**')
            file_temp.write(line_temp_out + '\n')
        file_temp.seek(0)
        self.text = file_temp.read()

    def spell_check(self):
        print("Running Spell-Check.")
        file_temp = open(os.path.join(output_dir_path, 'spell-check-'+ filein_name), 'w+')
        spellchecker = hunspell.HunSpell('/usr/share/hunspell/en_US.dic',
                                 '/usr/share/hunspell/en_US.aff')
        lines = self.text.splitlines()
        for line in lines:
            words = line.split()
            index = 0
            for word in words:
                #print("BSPCHK - " + word)
                if not word.startswith('**') and not spellchecker.spell(word):
                    suggestions = spellchecker.suggest(word)
                    if len(suggestions)>0:
                        #print(suggestions[0])
                        autocorrected = suggestions[0]
                        word = autocorrected
                #print("ASPCHK - " + word)
                words[index] = word
                index = index + 1
            line_temp_out = ' '.join(words)
            file_temp.write(line_temp_out + '\n')
        file_temp.seek(0)
        self.text = file_temp.read()

if len(sys.argv) == 2:
    fileout_name = "clean-" + filein_name
else:
    fileout_name = sys.argv[2]
filein = open(filein_name, 'r')
fileout = open(fileout_name, 'w')
filein_text = filein.read()

ct = clean_tweets(filein_text)
ct.remove_sentiments()
ct.remove_at_mentions()
ct.remove_hash_tags()
ct.remove_emoji_smileys_special()
ct.remove_reserved_words()
ct.spell_check()

fileout.write(ct.text)

filein.close()
fileout.close()

print("Done..")
