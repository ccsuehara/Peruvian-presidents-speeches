#!/usr/bin/env python
# coding: utf-8

# In[17]:


#get_ipython().run_line_magic('load_ext', 'autoreload')
#get_ipython().run_line_magic('autoreload', '2')


# In[2]:


import pandas as pd
import re
import lucem_illud_2020
import spacy
from nltk.tokenize import sent_tokenize

import sys
sys.path.insert(0, '../../scripts')
from data_cleaning import *


# In[3]:


speeches_dir = '../../data/presidentialSpeechPeru/txt'


# In[4]:


speeches_raw = loadcorpus(speeches_dir)


# In[5]:


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


# In[6]:


speech['cleaned text'] = speech['raw text'].apply(lambda x: clean_raw_text(x))


# In[7]:


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

speech.loc[(speech['year'].astype('int32') >= 2016), 'administration'] = 'Kuzcynski/Vizcarra'

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

speech.loc[(speech['year'].astype('int32') >= 2018), 'president'] = 'Vizcarra'

speech['year-president'] = speech['year'] + '-' + speech['president']


# In[8]:


speech.head()


# In[9]:


speech['tokenized_words'] = speech['cleaned text'].apply(lambda x: lucem_illud_2020.word_tokenize(x))


# In[10]:


countsDict = {}
for word in speech['tokenized_words'].sum():
    if word in countsDict:
        countsDict[word] += 1
    else:
        countsDict[word] = 1
word_counts = sorted(countsDict.items(), key = lambda x : x[1], reverse = True)
word_counts[:25]


# In[11]:


stop_words = []
for word, count in word_counts:
    if word == 'al':
        break
    else:
        stop_words.append(word)


# In[12]:


more_words = ['por', 'al', 'este', 'en', 'como', 'lo', 'el', 'la', 'las', 'los', 'su', 'sus'
              'y', 'de', 'que', 'a', 'del', 'para', 'con', 'se', 'ante']
for word in more_words:
    stop_words.append(word)


# In[13]:


speech['normalized_words'] = speech['tokenized_words'].apply(lambda x: normalize_tokens(x, stop_words))


# In[14]:


speech['tokenized_sentences'] = speech['cleaned text'].apply(sent_tokenize)


# In[15]:


speech['tokenized_words_in_sentences'] = speech['tokenized_sentences'].apply(lambda x: [lucem_illud_2020.word_tokenize(s) for s in x])


# In[20]:


speech['normalized_words_in_sentences'] = speech['tokenized_words_in_sentences'].apply(lambda x: [normalize_tokens(s, stop_words) for s in x])


# In[ ]:


speech.head()


# In[ ]:


speech.to_pickle('../../data/clean/speech.pkl')

