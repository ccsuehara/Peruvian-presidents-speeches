#!/usr/bin/env python
# coding: utf-8

# # Data preparation
#
# This notebook reads the `TXT` files of the speeches and builds a single
# dataframe with every tokenized and normalized content we'll use.
#
# Please note that none of the code chunks of this notebook were actually ran
# from here. As the processing part took a great amount of time to be completed,
#  we transformed this notebook in a Python script and submitted it through the
# slurm work manager of the Computer Science department. The script is the file
# `2_data_preparation.py` in this same directory, and the file
# `run_data_preparation.sbatch` loads it to the slurm environment.


import pandas as pd
import re
import spacy
from nltk.tokenize import sent_tokenize

import sys
sys.path.insert(0, '../../scripts')
import data_cleaning as clean


# Defining the directory of the speeches:
speeches_dir = '../../data/presidentialSpeechPeru/txt'

# We load the corpus from this path using a helper function we created:
speeches_raw = clean.loadcorpus(speeches_dir)


# After this, we load the result in a data frame and start adding some
# metadata columns:
speech = pd.DataFrame()
filenames = []
raw = []
for filename, raw_speech in speeches_raw.items():
    print(filename)
    filenames.append(filename)
    raw.append(raw_speech)
speech['filename'] = filenames
speech['raw text'] = raw

pattern = re.compile('[0-9]{4}')
speech['year'] = speech['filename'].apply(lambda x: pattern.search(x).group(0))
speech = speech.sort_values(by='year').reset_index(drop=True)


# Now we clean these raw texts using another ad-hoc function:
speech['cleaned text'] = speech['raw text'].apply(lambda x: clean.clean_raw_text(x))


# Adding the administration and president of each speech:
speech.loc[(speech['year'].astype('int32') >= 1956) &            (speech['year'].astype('int32') <= 1961), 'administration'] = 'Prado'
speech.loc[(speech['year'].astype('int32') >= 1962) &            (speech['year'].astype('int32') <= 1962), 'administration'] = 'Lindley'
speech.loc[(speech['year'].astype('int32') >= 1963) &            (speech['year'].astype('int32') <= 1968), 'administration'] = 'Belaunde(1)'
speech.loc[(speech['year'].astype('int32') >= 1969) &            (speech['year'].astype('int32') <= 1975), 'administration'] = 'Velasco'
speech.loc[(speech['year'].astype('int32') >= 1976) &            (speech['year'].astype('int32') <= 1979), 'administration'] = 'Morales Bermudez'
speech.loc[(speech['year'].astype('int32') >= 1980) &            (speech['year'].astype('int32') <= 1984), 'administration'] = 'Belaunde(2)'
speech.loc[(speech['year'].astype('int32') >= 1985) &            (speech['year'].astype('int32') <= 1989), 'administration'] = 'Garcia(1)'
speech.loc[(speech['year'].astype('int32') >= 1990) &            (speech['year'].astype('int32') <= 1994), 'administration'] = 'Fujimori(1)'
speech.loc[(speech['year'].astype('int32') >= 1995) &            (speech['year'].astype('int32') <= 2000), 'administration'] = 'Fujimori(2)'
speech.loc[(speech['year'].astype('int32') >= 2001) &            (speech['year'].astype('int32') <= 2005), 'administration'] = 'Toledo'
speech.loc[(speech['year'].astype('int32') >= 2006) &            (speech['year'].astype('int32') <= 2010), 'administration'] = 'Garcia(2)'
speech.loc[(speech['year'].astype('int32') >= 2011) &            (speech['year'].astype('int32') <= 2015), 'administration'] = 'Humala'
speech.loc[(speech['year'].astype('int32') >= 2016) &            (speech['year'].astype('int32') <= 2019), 'administration'] = 'Kuzcynski/Vizcarra'
speech.loc[(speech['year'].astype('int32') >= 2020) &            (speech['year'].astype('int32') <= 2020), 'administration'] = 'Sagasti'

speech.loc[(speech['year'].astype('int32') >= 1956) &            (speech['year'].astype('int32') <= 1961), 'president'] = 'Prado'
speech.loc[(speech['year'].astype('int32') >= 1962) &            (speech['year'].astype('int32') <= 1962), 'president'] = 'Lindley'
speech.loc[(speech['year'].astype('int32') >= 1963) &            (speech['year'].astype('int32') <= 1968), 'president'] = 'Belaunde'
speech.loc[(speech['year'].astype('int32') >= 1969) &            (speech['year'].astype('int32') <= 1975), 'president'] = 'Velasco'
speech.loc[(speech['year'].astype('int32') >= 1976) &            (speech['year'].astype('int32') <= 1979), 'president'] = 'Morales Bermudez'
speech.loc[(speech['year'].astype('int32') >= 1980) &            (speech['year'].astype('int32') <= 1984), 'president'] = 'Belaunde'
speech.loc[(speech['year'].astype('int32') >= 1985) &            (speech['year'].astype('int32') <= 1989), 'president'] = 'Garcia'
speech.loc[(speech['year'].astype('int32') >= 1990) &            (speech['year'].astype('int32') <= 2000), 'president'] = 'Fujimori'
speech.loc[(speech['year'].astype('int32') >= 2001) &            (speech['year'].astype('int32') <= 2005), 'president'] = 'Toledo'
speech.loc[(speech['year'].astype('int32') >= 2006) &            (speech['year'].astype('int32') <= 2010), 'president'] = 'Garcia'
speech.loc[(speech['year'].astype('int32') >= 2011) &            (speech['year'].astype('int32') <= 2015), 'president'] = 'Humala'
speech.loc[(speech['year'].astype('int32') >= 2016) &            (speech['year'].astype('int32') <= 2017), 'president'] = 'Kuzcynski'
speech.loc[(speech['year'].astype('int32') >= 2018) &            (speech['year'].astype('int32') <= 2019), 'president'] = 'Vizcarra'
speech.loc[(speech['year'].astype('int32') >= 2020) &            (speech['year'].astype('int32') <= 2020), 'president'] = 'Sagasti'

#Exception for Paniagua
speech.loc[(speech['year'].astype('int32') == 2000) &            (speech['filename'].astype('str')  == 'mensaje-2000-vp-noviembre.txt'), 'administration'] = 'Paniagua'
speech.loc[(speech['year'].astype('int32') == 2000) &            (speech['filename'].astype('str')  == 'mensaje-2000-vp-noviembre.txt'), 'president'] = 'Paniagua'


speech['year-president'] = speech['year'] + '-' + speech['president']

speech.head()

# Tokenizing words:
speech['tokenized_words'] = speech['cleaned text'].apply(lambda x: clean.word_tokenize(x))

# Now we normalize:
speech['normalized_words'] = speech['tokenized_words'].apply(lambda x: clean.normalize_tokens(x))

# Then, we tokenize sentences using the function from `nltk` for this:
speech['tokenized_sentences'] = speech['cleaned text'].apply(sent_tokenize)

# Now we tokenize each word in each sentence:
speech['tokenized_words_in_sentences'] = speech['tokenized_sentences'].apply(lambda x: [clean.word_tokenize(s) for s in x])

# Finally, we normalized each tokenized word within each sentence:
speech['normalized_words_in_sentences'] = speech['tokenized_words_in_sentences'].apply(lambda x: [clean.normalize_tokens(s) for s in x])

# Saving the result:
speech.to_pickle('../../data/clean/speech.pkl')


speech_init = speech.loc[(speech['year'].astype('int32') == 1963) |
                         (speech['year'].astype('int32') == 1969) |
                        (speech['year'].astype('int32') == 1976) |
                        (speech['year'].astype('int32') == 1980) |
                        (speech['year'].astype('int32') == 1985) |
                        (speech['year'].astype('int32') == 1990) |
                        (speech['year'].astype('int32') == 1995) |
                        (speech['year'].astype('int32') == 2000) |
                        (speech['year'].astype('int32') == 2001) |
                        (speech['year'].astype('int32') == 2006) |
                        (speech['year'].astype('int32') == 2011) |
                        (speech['year'].astype('int32') == 2016) |
                        (speech['year'].astype('int32') == 2000) |
                        ((speech['year'].astype('int32') == 2018) & (speech['filename'] == 'mensaje-2018-2.txt')) |
                        (speech['year'].astype('int32') == 2020) ]

speech_init.reset_index(drop = True, inplace = True)

speech_init.to_pickle('../../data/clean/speech_init.pkl')
