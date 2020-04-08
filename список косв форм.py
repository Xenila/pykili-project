import collections
import re
word_list = []
with open ('пословицы2.txt', encoding = 'utf-8') as file:
    lines = file.readlines()
    for line in lines:
        words = line.split()
        for word in words:
            if not (word == '–' or word == '—'):
                word_list.append(word)
    word_dict = collections.Counter(word_list)
    final_words = list(word_dict)
    pat = 'ё'
    pat2 = '[^А-Яа-я]'
    for word in final_words:
        word = re.sub(pat, 'е', word)
        word = re.sub(pat2, '', word)
        word = word.lower()
        with open ('косвенные формы.txt', 'a', encoding = 'utf-8') as file2:
            file2.write(word + '\n')
