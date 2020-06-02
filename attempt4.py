import collections
import re
import pymorphy2
morph_an = pymorphy2.MorphAnalyzer()

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
            ant_pair[0] = ant_pair[0].lower()
            ant_pairs.append(ant_pair)
    return ant_pairs       

def speech_part(word, ant_pairs, lem_dict):
    morph_an = pymorphy2.MorphAnalyzer()
    for ant_pair in ant_pairs:
        if lem_dict[word].lower() == ant_pair[0]:
            word_parse = morph_an.parse(word)[0]
            sp_part = word_parse.tag.POS
            return(sp_part)

def adjective(token, lem_dict, ant_pairs):
    morph_an = pymorphy2.MorphAnalyzer()
    w = morph_an.parse(token)[0]
    gen_ = w.tag.gender
    num_ = w.tag.number
    pos_ = w.tag.POS
    if pos_ == 'ADJF':
        case_ = w.tag.case
    for ant_pair in ant_pairs:
        if lem_dict[token].lower() == ant_pair[0]:
            a = morph_an.parse(ant_pair[1])[0].inflect({num_, pos_})
            if a:
                if w.tag.POS == 'ADJF':
                    a = a.inflect({case_})
                if gen_:
                    a = a.inflect({gen_}).word
                else:
                    a = a.word
                return a

def pro_noun(token, lem_dict, ant_pairs):
    morph_an = pymorphy2.MorphAnalyzer()
    w = morph_an.parse(token)[0]
    case_ = w.tag.case
    if w.tag.POS == 'NOUN':
        num_ = w.tag.number
    for ant_pair in ant_pairs:
        if lem_dict[token].lower() == ant_pair[0]:
            if w.tag.POS == 'NOUN':
                a = morph_an.parse(ant_pair[1])[0].inflect({num_, case_}).word
            if w.tag.POS == 'NPRO':
                a = morph_an.parse(ant_pair[1])[0].inflect({case_}).word
            return a

def verb(token, lem_dict, ant_pairs):
    morph_an = pymorphy2.MorphAnalyzer()
    w = morph_an.parse(token)[0]
    mood_ = w.tag.mood
    for ant_pair in ant_pairs:
        if lem_dict[token].lower() == ant_pair[0]:
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

def comparative(token, lem_dict, ant_pairs):
    morph_an = pymorphy2.MorphAnalyzer()
    w = morph_an.parse(token)[0]
    pos_ = w.tag.POS
    for ant_pair in ant_pairs:
        if lem_dict[token].lower() == ant_pair[0]:
            a = morph_an.parse(ant_pair[1])[0].inflect({pos_}).word
            return a


def main():
    lines_ = cleaning('_слова.txt')
    lem_lines_ = opening('output_леммы.txt')
    ant_pairs_ = antonyms('_пары.txt')   #список из списков [слово, антоним]
    lem_dict_ = dictionary(lines_, lem_lines_)  #словарь [слово]: нач. форма 
    word_list_ = list(lem_dict_)
    ant_list_ = []
    for word_ in word_list_:
        sp_part_ = speech_part(word_, ant_pairs_, lem_dict_)
        if sp_part_ == 'ADJF' or sp_part_ == 'ADJS':
            ant_changed_ = adjective(word_, lem_dict_, ant_pairs_)            
        elif sp_part_ == 'NOUN' or sp_part_ == 'NPRO':
            ant_changed_ = pro_noun(word_, lem_dict_, ant_pairs_)
        elif sp_part_ == 'VERB':
            ant_changed_ = verb(word_, lem_dict_, ant_pairs_)
        elif sp_part_ == 'COMP':
            ant_changed_ = comparative(word_, lem_dict_, ant_pairs_)
        #elif sp_part_ == 'NPRO':
            #ant_changed_ = pronoun(word_, lem_dict_, ant_pairs_)
        elif sp_part_ == 'ADVB':
            for ant_pair_ in ant_pairs_:
                if lem_dict_[word_].lower() == ant_pair_[0]:
                    ant_changed_ = ant_pair_[1]
        else: ant_changed_ = word_
        ant_list_.append(ant_changed_)  #список изменённых антонимов
    word_ant_dict_ = dict(zip(word_list_, ant_list_)) #слово: антоним (косв. ф.)
    with open('new_file.txt', 'w', encoding = 'utf-8') as file2_:
        for line_ in lines_:
            words_ = line_.split()
            for i in range(len(words_)):
                if words_[i] in word_ant_dict_:
                    words_[i] = word_ant_dict_[words_[i]]
            print(words_)
            file2_.write(' '.join(words_) + '\n')
           
if __name__ == '__main__':
    main()
