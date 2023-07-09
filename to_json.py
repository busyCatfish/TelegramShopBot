import json

mas_of_words = []

with open('words.txt', encoding='utf-8') as f:
    for i in f:
        word = i.lower().split('\n')[0]
        if word!= '':
            mas_of_words.append(word)
with open('words.json','w',encoding='utf-8') as f:
    json.dump(mas_of_words,f)