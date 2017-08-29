# coding: utf-8
from pymarkov import markov
import os, random, sys
import pickle
import string

from django.conf import settings

def load(filename):
    data = None
    fh = None
    try:
        fh = open(filename, "rb")
        data = pickle.load(fh)
    except (EnvironmentError, pickle.UnpicklingError) as err:
        print("{0}: file load error: {1}".format(filename, err))
    finally:
        if fh is not None:
            fh.close()
    return data

def rebuild_text(original_text):
    filepath = os.path.join(settings.BASE_DIR, 'basedict_l.dat')
    data = load(filepath)
    maxwordlen = 30
    punctuation = string.punctuation.replace('-','!')
    if sys.version_info[0] < 3:
        raw_text = original_text.encode('utf-8').translate(None, punctuation)
        raw_text = raw_text.decode('utf-8')
    else:
        punctuation_map = str.maketrans('', '', punctuation)
        raw_text = original_text.translate(punctuation_map)
    #print('your text:', raw_text)
    text_words = raw_text.split()
    length = random.randint(2, len(raw_text))
    out = markov.generate(data, length, 2, join_char="")
    #print('raw generated:', out)
    out = out.split()
    insert_place = 0
    for text_word in text_words:
        if text_word.isalpha() and random.randint(0,10) > 8:
            insert_place = random.randint(insert_place, len(out))
            out.insert(insert_place, text_word.lower())
        else:
            insert_place = random.randint(insert_place, len(out))
            out.insert(insert_place, text_word)
    i = 0
    j = 0
    signs = u'ьъ'
    
    for word in out:
        if word[0].isupper():
            j = 0
            endsign = random.choice(['.','.','.','.','?','!'])
            out[i-1] = out[i-1] + endsign
            out[i] = out[i][0] + out[i][1:].lower()
        else:
            out[i] = out[i].lower()
        if word[0].lower() in signs:
            out[i] = word[1:]
        if j > 1 and random.randint(0, 10) > 6:
            out[i-1] = out[i-1] + ','
        if len(word) > maxwordlen:
            if word[maxwordlen] in signs:
                insert_place = maxwordlen + 1
            else:
                insert_place = maxwordlen
            out[i] = word[:maxwordlen] + ' ' + word[insert_place:]
        i = i + 1
        j = j + 1
    out = " ".join(out)
    result = out[:1].upper() + out[1:].rstrip()
    if result[-1] not in ['.','?','!']:
        result = result[:] + '.'
    return result