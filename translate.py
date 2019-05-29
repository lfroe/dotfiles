#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import re
import os
import subprocess
import requests
import json
import re

pattern = re.compile("(getWord)(\W+)([\'|\"][\w|\(|\)|\s|\-]+[\'|\"]).*")
words = []
translations = []
missing = []

rootdir = '/Users/lukas/Documents/EXT/frontend/Source/public/app.babel/'
lang_file_dir = '/Users/lukas/Documents/EXT/extBackend/grails-app/conf/lang'

for root, subfolders, files in os.walk(rootdir):
    for file in files:
        with open (os.path.join(root,file)) as _fin:
            for i, line in enumerate(_fin):
                for match in re.finditer(pattern, line):
                    words.append(str(match.groups()[2].replace("'", '').replace('"', '').strip()))

words = set(words)

with open(os.path.join(lang_file_dir, 'de_Deutsch.json')) as de_file:
    for i, line in enumerate(de_file):
        translations.append(str(line.split(':')[0].replace('"', '').lstrip().rstrip()))
for word in words:
    try:
        index = translations.index(word)
    except:
        missing.append(word)

print('Congratulations! You are missing {} translations!'.format(len(missing)))


sourceLang = 'en'
targetLang = 'de'

punctuations = ['?', '!', '.']
translated_words = ''

for i in range(0, len(missing)):
    word = re.sub(r'[\!|\.|\?]', "", missing[i])
    print('translating word#{} - {}'.format(i+1, word))
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + sourceLang + "&tl=" + targetLang + "&dt=t&q=" + word
    result = requests.get(url)
    if result.status_code == 429:
        print('error: too many requests')
        break;
    translation = json.loads(result.text)[0][0][0]
    line = '"{}": "{}",\n'.format(word, translation)
    translated_words += line
       
os.system("echo '%s' | pbcopy" %translated_words)
