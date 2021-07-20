# This script contains all the util functions we use for data preparation

from os import listdir
import spacy
import re

NLP = spacy.load('es_core_news_lg')

def loadcorpus(corpus_name, corpus_style="text"):
    texts_raw = {}
    for file in listdir(corpus_name + "/"):
        file2 = corpus_name + "/" + file
        print(file)
        texts_raw[file] = []
        with open(file2, encoding='utf-8') as f:
            for line in f:
                texts_raw[file].append(line)
    return texts_raw

def text_is_number(text):
    try:
        float(text)
        return True
    except ValueError:
        return False

def clean_raw_text(raw_texts):
    clean_texts = []
    for text in raw_texts:
        try:
            if type(text) == bytes:
                text = text.decode("utf-8")
            clean_text = text.replace("\n", "")
            clean_text = clean_text.replace("\xa0", "")
            clean_text = clean_text.replace("\x0c", "")
            clean_text = re.sub(' {2,}', ' ', clean_text)
            if not (clean_text == '' \
                    or clean_text == ' ' \
                    or text_is_number(clean_text)):
                clean_texts.append(clean_text)
        except AttributeError:
            print("ERROR CLEANING")
            print(text)
            continue
        except UnicodeDecodeError:
            print("Unicode Error, Skip")
            continue
    return ' '.join(clean_texts)

def normalize_tokens(word_list, extra_stop=[]):
    #We can use a generator here as we just need to iterate over it
    normalized = []

    if type(word_list) == list and len(word_list) == 1:
        word_list = word_list[0]

    if type(word_list) == list:
        word_list = ' '.join([str(elem) for elem in word_list])

    doc = NLP(word_list.lower())

    # add the property of stop word to words considered as stop words
    if len(extra_stop) > 0:
        for stopword in extra_stop:
            lexeme = NLP.vocab[stopword]
            lexeme.is_stop = True

    for w in doc:
        # if it's not a stop word or punctuation mark, add it to our article
        if w.text != '\n' and not w.is_stop and not w.is_punct and not w.like_num and len(w.text.strip()) > 0:
            # we add the lematized version of the word
            normalized.append(str(w.lemma_))

    return normalized

def word_tokenize(text):
    tokenized = []
    # pass word list through language model.
    doc = NLP(text)
    for token in doc:
        if not token.is_punct and len(token.text.strip()) > 0:
            tokenized.append(token.text)
    return tokenized
