# -*- coding: utf-8 -*-

import json
import jieba
import PyPDF2
import re
import random
import os.path

# Load json database of words: score from scrape.json
# Add new words from text-files or (to do) PDFs
# Review words with less than 1.00 score in flashcard function


def update(words):
    with open('scrape.json',encoding='utf-8') as data1:
        contents = json.load(data1)
    test = contents
    for (i,j) in words.items():
        if i not in test:
            test[i] = j
        else:
            if test[i] + j > 1.0:
                test[i] = 1.0
            else:
                test[i] += j
    with open('scrape.json','w',encoding='utf-8') as fp:
        json.dump(test, fp, ensure_ascii=False)
    print(f'Successfully updated: %s' % words)


def load_all():
    with open('scrape.json',encoding='utf-8') as data1:
        contents = json.load(data1)
    contents2 = contents
    return contents2


def find_chars(list):
    with open('scrape.json', encoding='utf-8') as data:
        contents = json.load(data)
    data = contents
    updatec = []
    for i in list:
        if i not in data:
            updatec.append(i)
    if updatec:
        new_dict = {i:0 for (i) in list}
        update(new_dict)
    else:
        print('Nothing to add!')

def load_chars(doc):
    # doc: a non-PDF file with Chinese text

    with open(doc, 'r', encoding='utf-8') as fp:
        text = fp.read().strip()
    latin = re.compile(r'[^a-zA-Z0-9_\s\[\]”“。、,…!:\-]+')
    to_cut = ''.join(latin.findall(text))
    seg_list = jieba.cut(to_cut)
    find_chars([i for i in seg_list])


def load_chars_pdf(pdf):
    pass

def clearup():
    with open('scrape.json', encoding='utf-8') as data1:
        contents = json.load(data1)
    test = contents
    to_delete = [i for i in test if len(i) == 1]
    for key in to_delete:
        del test[key]
    with open('scrape.json','w',encoding='utf-8') as fp:
        json.dump(test, fp, ensure_ascii=False)
    print('Successfully cleared up %d cards' % len(to_delete))


def flashcards():
    cards = {i:j for (i,j) in load_all().items() if j < 1.0}
    print('\t\tPreparing 10 random cards...')
    review = [i for i in random.sample(list(cards), 10)]
    total = {}
    for i in review:
        while True:
            print('\n\t\t*****  %s  *****' % i)
            first = int(input('\tCan you pronounce %s? 1 or 0\n>' % i))
            second = int(input('\tDo you know the meaning of %s? 1 or 0\n>' % i))
            if type(first) != int or type(second) != int:
                print('\n\tIncorrect Input')
            else:
                score = float(first/20 + second/20)
                total[i] = score
                break

    if len(total) > 0:
        correct = [i for i in total if total[i] >= 0.1]
        print('You got these words totally correct!\n\t %s' % correct)
        print('\nAnd you need to work on these: %s\n\t' % [i for i in review if i not in correct])
        print('\t****** UPDATING WORD DATABASE *******')
        update(total)
    else:
        print('You really need to work on these words: \n%s' % review)



def main():
    inputF = input('\n\tType "L" to scan files for new words'
                   '\n\tOr "Q" to quit\n\tType "P" to print the database'
                   '\n\tOr "F" for flashcards'
                   '\n\tOr "C" to clear-up \n> ')
    if inputF == 'Q':
        print('Goodbye///')
        quit()
    elif inputF == 'P':
        to_print = load_all()
        print('Total %s words' % len(to_print))
        print(to_print)
    elif inputF == "F":
        flashcards()
    elif inputF == "C":
        clearup()
    elif inputF == "L":
        inputL = input('\n\tEnter each filename separated (no commas)\n> ')
        input_x = inputL.split()
        for i in input_x:
            if (not os.path.isfile(i)):
                print('\n\t"%s" is not a valid filename\n' % i)
            elif i.lower().endswith('.pdf'):
                load_chars_pdf(i)
            else:
                load_chars(i)
    main()


if __name__ == "__main__":
     main()
