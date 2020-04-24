import collections
import re
import pymorphy2
word_list = []
with open ('пословицы_демо.txt', encoding = 'utf-8') as file:
    lines = file.readlines()
    #pat = 'ё'
    pat2 = '[^А-Яа-я]'
    for line in lines:
        words = line.split()
        for word in words:
            #word = word.lower()
            if not (word == '–' or word == '—'):
                #word = re.sub(pat, 'е', word)
                word = re.sub(pat2, '', word)
                word_list.append(word)

morph_an = pymorphy2.MorphAnalyzer()
morph_list = []
for word in word_list:
    f = morph_an.parse(word)[0]
    morphs = []
    morphs.append(word)
    morphs.append(f.tag)
    morphs.append(f.normal_form)
    morph_list.append(morphs)
#print(morph_list)

with open ('антонимы.txt', encoding = 'utf-8') as ants:
    lines = ants.readlines()
    ant_pairs = []
    for line in lines:
        ant_pair = line.split()
        ant_pairs.append(ant_pair)

word_ant_dict = {}
for morph in morph_list: #список из списков [слово, признаки, нач. форма]
    for ant_pair in ant_pairs: #список [слово, антоним]
        if morph[2].lower() == ant_pair[0].lower():
            #print(morph[0], morph[1], ant_pair[1])
            #ant = morph_an.parse(ant_pair[1])[0]
            #forms_list = ant.lexeme
            w = morph_an.parse(morph[0])[0]
            sp_part = w.tag.POS
            #print(sp_part)
            if sp_part == 'ADJF':
                gen_ = w.tag.gender
                num_ = w.tag.number
                case_ = w.tag.case
                #print(gen_, num_, case_)
                a = morph_an.parse(ant_pair[1])[0].inflect({num_, case_}).word
                #if gen_:
                    #a = morph_an.parse(a)[0].inflect({gen_}).word
                print(morph[0], a)
                word_ant_dict[morph[0]] = a
            if sp_part == 'NOUN':
                num_ = w.tag.number
                case_ = w.tag.case
                a = morph_an.parse(ant_pair[1])[0].inflect({num_, case_}).word
                print(morph[0], a)
                word_ant_dict[morph[0]] = a
            if sp_part == 'VERB':
                mood_ = w.tag.mood
                #print(mood_)
                if mood_ == 'indc':
                    tense_ = w.tag.tense
                    if tense_ == 'pres' or tense_ == 'futr':
                        num_ = w.tag.number
                        pers_ = w.tag.person
                        a = morph_an.parse(ant_pair[1])[0].inflect({num_, pers_}).word
                        print(morph[0], a)
                        word_ant_dict[morph[0]] = a
                if mood_ == 'impr':
                    num_ = w.tag.number
                    #pers_ = w.tag.person
                    invl_ = w.tag.involvement
                    a = morph_an.parse(ant_pair[1])[0].inflect({num_, invl_}).word
                    print(morph[0], a)
                    word_ant_dict[morph[0]] = a
            if sp_part == 'COMP':
                a = morph_an.parse(ant_pair[1])[0].inflect({'COMP'}).word
                print(morph[0], ant_pair[1])
                word_ant_dict[morph[0]] = a
            if sp_part == 'ADVB':
                print(morph[0], ant_pair[1])
                word_ant_dict[morph[0]] = ant_pair[1]
            break
print(word_ant_dict)
print(word_list)
for word in word_list:
    if word in word_ant_dict:
        print(word_ant_dict[word])
    else:
        print(word)
