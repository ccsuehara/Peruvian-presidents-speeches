# This script contains all the util functions we use for data preparation

from os import listdir
import spacy
import re

NLP = spacy.load('es_core_news_lg')
STOP_WORDS = ['y', 'a', 'año', 'país', 'o', 'e', 'cuyo', 'señor', 'cuya',
    'nuevamente', 'don']

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
            clean_text = text.replace("\xa0", "")
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

    cleaned_text = ' '.join(clean_texts)
    cleaned_text = cleaned_text.replace('\n ', '\n')

    return cleaned_text

def normalize_tokens(word_list, extra_stop=STOP_WORDS):
    #We can use a generator here as we just need to iterate over it
    normalized = []

    if type(word_list) == list and len(word_list) == 1:
        word_list = word_list[0]

    elif type(word_list) == list:
        word_list = ' '.join([str(elem) for elem in word_list])

    doc = NLP(word_list.lower())

    # add the property of stop word to words considered as stop words
    if len(extra_stop) > 0:
        for stopword in extra_stop:
            lexeme = NLP.vocab[stopword]
            lexeme.is_stop = True

    for w in doc:
        # if it's not a stop word or punctuation mark, add it to our article
        if w.text != '\n' and not w.is_stop \
           and not w.is_punct and not w.like_num \
           and len(w.text.strip()) > 1 and w.is_alpha:
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

def paragraph_tokenize(text):

    separator1 = '.\n'
    separator2 = '. \n'
    sep = '|||'
    text = text.replace(separator1, sep).replace(separator2, sep)
    paragraphs1 = text.split(sep)
    paragraphs2 = []

    for paragraph in paragraphs1:

        cleaned_paragraph = paragraph.replace('\n', ' ')
        cleaned_paragraph = cleaned_paragraph.strip()
        cleaned_paragraph = re.sub(' {2,}', ' ', cleaned_paragraph)
        if not cleaned_paragraph == '':
            paragraphs2.append(cleaned_paragraph)

    return paragraphs2
