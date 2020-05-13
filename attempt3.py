import collections
import re
import pymorphy2

def cleaning(filename):
    with open (filename, encoding = 'utf-8') as file:
        lines = file.readlines()
        for line in lines:
            pat = '[^А-Яа-я\s]'
            pat2 = 'ё'
            line = re.sub(pat, '', line)
            line = re.sub(pat, 'е', line)
        return(lines)
                
def opening(filename):
    with open (filename, encoding = 'utf-8') as file:
         lem_lines = file.readlines() 
         for lem_line in lem_lines:
             pat = '[^А-Яа-я\s]'
             pat2 = 'ё'
             lem_line = re.sub(pat, '', lem_line)
             lem_line = re.sub(pat, 'е', lem_line)
    return(lem_lines)     

def dictionary(lines, lem_lines):
    word_list = []
    for line in lines:
        words = line.split()
        for word in words:
            word_list.append(word)
    lem_list = []
    for lem_line in lem_lines:
        lemmas = lem_line.split()
        for lemma in lemmas:
            lem_list.append(lemma)
    lem_dict = dict(zip(word_list, lem_list))
    return lem_dict

def antonyms(filename):
    with open (filename, encoding = 'utf-8') as file:
        lines = file.readlines()
        ant_pairs = []
        for line in lines:
            ant_pair = line.split()
            ant_pairs.append(ant_pair)
    return ant_pairs       

def speech_part(word, ant_pairs, lem_dict):
    morph_an = pymorphy2.MorphAnalyzer()
    for ant_pair in ant_pairs:
        if lem_dict[word].lower() == ant_pair[0].lower():
            word_parse = morph_an.parse(word)[0]
            sp_part = word_parse.tag.POS
            return(sp_part)

def ajective(token, lem_dict, ant_pairs):
    morph_an = pymorphy2.MorphAnalyzer()
    w = morph_an.parse(token)[0]
    gen_ = w.tag.gender
    num_ = w.tag.number
    case_ = w.tag.case
    for ant_pair in ant_pairs:
        if lem_dict[token] == ant_pair[0]:
            a = morph_an.parse(ant_pair[1])[0].inflect({num_, case_}).word
            if gen_:
                a = morph_an.parse(a)[0].inflect({gen_}).word
            return a

def noun(token, lem_dict, ant_pairs):
    morph_an = pymorphy2.MorphAnalyzer()
    w = morph_an.parse(token)[0]
    num_ = w.tag.number
    case_ = w.tag.case
    for ant_pair in ant_pairs:
        if lem_dict[token] == ant_pair[0]:
            a = morph_an.parse(ant_pair[1])[0].inflect({num_, case_}).word
            return a

def verb(token, lem_dict, ant_pairs):
    morph_an = pymorphy2.MorphAnalyzer()
    w = morph_an.parse(token)[0]
    mood_ = w.tag.mood
    for ant_pair in ant_pairs:
        if lem_dict[token] == ant_pair[0]:
            if mood_ == 'indc':
                tense_ = w.tag.tense
                if tense_ == 'pres' or tense_ == 'futr':
                    num_ = w.tag.number
                    pers_ = w.tag.person
                    if pers_:
                        a = morph_an.parse(ant_pair[1])[0].inflect({num_, pers_}).word
                    else:
                        a = morph_an.parse(ant_pair[1])[0].inflect({num_}).word
                    return a
                if tense_ == 'past':
                    gen_ = w.tag.gender
                    num_ = w.tag.number
                    a = morph_an.parse(ant_pair[1])[0].inflect({num_}).word
                    if gen_:
                        a = morph_an.parse(a)[0].inflect({gen_}).word
                    return a
            if mood_ == 'impr':
                num_ = w.tag.number
                invl_ = w.tag.involvement
                a = morph_an.parse(ant_pair[1])[0].inflect({num_, invl_}).word
                return a
'''
def comparative(token, lem_dict, ant_pairs):
    morph_an = pymorphy2.MorphAnalyzer()
    w = morph_an.parse(token)[0]
    for ant_pair in ant_pairs:
        if lem_dict[token] == ant_pair[0]:
            a = morph_an.parse(ant_pair[1])[0].inflect({'COMP'}).word
            return a

def replacing(dic, lines):
    with open('new_file.txt', 'w', encoding = 'utf-8') as file:
        for line in lines:
            words = line.split()
            for i in range(len(words)):
                if words[i] in dic:
                    words[i] = dic[words[i]]
            file.write(' '.join(words) + '\n')        
            lines2 = file.readlines()
            return(lines2)
'''
def main():
    lines_ = cleaning('_слова.txt')
    lem_lines_ = opening('_леммы.txt')
    ant_pairs_ = antonyms('_пары.txt')
    lem_dict_ = dictionary(lines_, lem_lines_)  #словарь [слово]: нач. форма
    ant_pairs_ = antonyms('_пары.txt')   #список из списков [слово, антоним]
    word_list_ = list(lem_dict_)
    ant_list_ = []
    for word_ in word_list_:
        sp_part_ = speech_part(word_, ant_pairs_, lem_dict_)
        if sp_part_ == 'ADJF':
            ant_changed_ = ajective(word_, lem_dict_, ant_pairs_)
        elif sp_part_ == 'NOUN':
            ant_changed_ = noun(word_, lem_dict_, ant_pairs_)
        elif sp_part_ == 'VERB':
            ant_changed_ = verb(word_, lem_dict_, ant_pairs_)
        #elif sp_part_ == 'COMP':
            #ant_changed_ = comparative(word_, lem_dict_, ant_pairs_)
        else:
            for ant_pair_ in ant_pairs_:
                if lem_dict_[word_] == ant_pair_[0]:
                    ant_changed_ = ant_pair_[1]
        ant_list_.append(ant_changed_)
    #print(ant_list_)    #список изменённых антонимов
    word_ant_dict_ = dict(zip(word_list_, ant_list_))
    with open('new_file.txt', 'w', encoding = 'utf-8') as file2_:
        for line_ in lines_:
            words_ = line_.split()
            for i in range(len(words_)):
                if words_[i] in word_ant_dict_:
                    words_[i] = word_ant_dict_[words_[i]]
            file2_.write(' '.join(words_) + '\n')
            
    
if __name__ == '__main__':
    main()
