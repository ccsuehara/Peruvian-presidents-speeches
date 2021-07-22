import requests
import pandas
import pandas as pd
import pdfminer.pdfinterp
import pdfminer.converter
import pdfminer.layout
import pdfminer.pdfpage

import csv
import re
import urllib.parse
import io
import os.path
import os

import os
from os import listdir
from os.path import isfile, join

import random
random.seed(853915)

##Getting the data
##All this work is based in a notebook we created for the course's homeworks.
## this script replaces the 1_downloading Peru presidential speeches 1956-2019

def downloadIfNeeded(targetURL, outputFile, **openkwargs):
    if not os.path.isfile(outputFile):
        outputDir = os.path.dirname(outputFile)
        #This function is a more general os.mkdir()
        if len(outputDir) > 0:
            os.makedirs(outputDir, exist_ok = True)
        r = requests.get(targetURL, stream=True)
        #Using a closure like this is generally better than having to
        #remember to close the file. There are ways to make this function
        #work as a closure too
        with open(outputFile, 'wb') as f:
            f.write(r.content)
    return open(outputFile, **openkwargs)



def readPDF(pdfFile):
    #Based on code from http://stackoverflow.com/a/20905381/4955164
    #Using utf-8, if there are a bunch of random symbols try changing this
    codec = 'utf-8'
    rsrcmgr = pdfminer.pdfinterp.PDFResourceManager()
    retstr = io.StringIO()
    layoutParams = pdfminer.layout.LAParams()
    device = pdfminer.converter.TextConverter(rsrcmgr, retstr, laparams = layoutParams) #, codec = codec)
    #We need a device and an interpreter
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(rsrcmgr, device)
    password = ''
    maxpages = 0
    caching = True
    pagenos=set()
    for page in pdfminer.pdfpage.PDFPage.get_pages(pdfFile, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    device.close()
    returnedString = retstr.getvalue()
    retstr.close()
    return returnedString



url_filenames = ['mensaje-2019-01-vizcarra.pdf',
                 'mensaje-2018-4.pdf',
                 'mensaje-2018-2.pdf', # Agrega el primer mensaje presidencial de vizcarra
                 'mensaje-2017-ppk.pdf',
                 'mensaje-2016-ppk.pdf',
                 'mensaje-2015-oh.pdf',
                 'mensaje-2014-oh.pdf',
                 'mensaje-2013-oh.pdf',
                 'mensaje-2012-oh.pdf',
                 'mensaje-2011-oh.pdf',
                 'mensaje-2010-ag.pdf',
                 'mensaje-2009-ag.pdf',
                 'mensaje-2008-ag.pdf',
                 'mensaje-2007-ag.pdf',
                 'mensaje-2006-ag.pdf',
                 'mensaje-2005-at.pdf',
                 'mensaje-2004-at.pdf',
                 'mensaje-2003-at.pdf',
                 'mensaje-2002-at.pdf',
                 'mensaje-2001-at.pdf',
                'mensaje-2000-vp-noviembre.pdf']


url_filenames2 = ['mensaje-2000-af.pdf',
                 'mensaje-1999-af.pdf',
                 'mensaje-1998-af.pdf',
                 'mensaje-1997-af.pdf',
                 'mensaje-1996-af.pdf',
                 'mensaje-1995-af.pdf',
                 'mensaje-1994-af.pdf',
                 'mensaje-1993-af.pdf',
                 'mensaje-1992-af.pdf',
                 'mensaje-1991-af.pdf',
                 'mensaje-1990-af.pdf',
                 'mensaje-1989-ag.pdf',
                 'mensaje-1988-ag.pdf',
                 'mensaje-1987-ag.pdf',
                 'mensaje-1986-ag.pdf',
                 'mensaje-1985-ag.pdf',
                 'mensaje-1984-fbt.pdf',
                 'mensaje-1983-fbt.pdf',
                 'mensaje-1982-fbt.pdf',
                 'mensaje-1981-fbt.pdf',
                 'mensaje-1980-fbt.pdf']



url_filenames3 = ['mensaje-1979.pdf',
                    'mensaje-1978-1.pdf',
                    'mensaje-1977.pdf',
                    'mensaje-1976.pdf',
                    'mensaje-1975-1.pdf',
                    'mensaje-1974.pdf',
                    'mensaje-1973.pdf',
                    'mensaje-1972.pdf',
                    'mensaje-1971.pdf',
                    'mensaje-1970.pdf',
                    'mensaje-1969.pdf',
                    'mensaje-1968-1.pdf',
                    'mensaje-1967.pdf',
                    'mensaje-1966.pdf',
                    'mensaje-1965.pdf',
                    'mensaje-1964.pdf',
                    'mensaje-1963-2.pdf',
                    'mensaje-1962.pdf',
                    'mensaje-1961.pdf',
                    'mensaje-1960.pdf',
                    'mensaje-1959.pdf',
                    'mensaje-1958.pdf',
                    'mensaje-1957.pdf',
                    'mensaje-1956-2.pdf']


key_president = {'mensaje-1979.pdf':'fmb',
                'mensaje-1978-1.pdf':'fmb',
                'mensaje-1977.pdf':'fmb',
                'mensaje-1976.pdf':'fmb',
                'mensaje-1975-1.pdf':'jva',
                'mensaje-1974.pdf':'jva',
                'mensaje-1973.pdf':'jva',
                'mensaje-1972.pdf':'jva',
                'mensaje-1971.pdf':'jva',
                'mensaje-1970.pdf':'jva',
                'mensaje-1969.pdf':'jva',
                'mensaje-1968-1.pdf':'fbt',
                'mensaje-1967.pdf':'fbt',
                'mensaje-1966.pdf':'fbt',
                'mensaje-1965.pdf':'fbt',
                'mensaje-1964.pdf':'fbt',
                'mensaje-1963-2.pdf':'fbt',
                'mensaje-1962.pdf':'nll',
                'mensaje-1961.pdf':'mpu',
                'mensaje-1960.pdf':'mpu',
                'mensaje-1959.pdf':'mpu',
                'mensaje-1958.pdf':'mpu',
                'mensaje-1957.pdf':'mpu',
                'mensaje-1956-2.pdf':'mpu'
                }



url_prefix = 'http://www.congreso.gob.pe/Docs/participacion/museo/congreso/files/mensajes/2001-2020/files/'
file_prefix_pdf = '../../data/presidentialSpeechPeru/pdf/'
file_prefix_txt = '../../data/presidentialSpeechPeru/txt/'

for speech_file in url_filenames:
    file = downloadIfNeeded(url_prefix + speech_file, file_prefix_pdf + speech_file, mode = 'rb')
    speech = readPDF(file)
    name = re.sub('.pdf', '', speech_file)
    with open(file_prefix_txt + name + '.txt', 'w') as text_file:
        text_file.write(speech)


url_prefix = 'http://www.congreso.gob.pe/Docs/participacion/museo/congreso/files/mensajes/1981-2000/files/'

for speech_file in url_filenames2:
    file = downloadIfNeeded(url_prefix + speech_file, file_prefix_pdf + speech_file, mode = 'rb')
    speech = readPDF(file)
    name = re.sub('.pdf', '', speech_file)
    with open(file_prefix_txt + name + '.txt', 'w') as text_file:
        text_file.write(speech)



url_prefix = 'http://www.congreso.gob.pe/Docs/participacion/museo/congreso/files/mensajes/1961-1980/files/'

for speech_file in url_filenames3:
    file = downloadIfNeeded(url_prefix + speech_file, file_prefix_pdf + speech_file, mode = 'rb')
    speech = readPDF(file)
    name = re.sub('-1\.', '.', speech_file)
    name = re.sub('-2\.', '.', name)
    name = re.sub('.pdf', '', name)
    president = key_president[speech_file]
    with open(file_prefix_txt + name + "-" + president +'.txt', 'w') as text_file:
        text_file.write(speech)


url_sagasti = "https://www.congreso.gob.pe/Docs/spa/files/discursos/discurso-asuncion-(17.11.20).pdf"


name = 'mensaje-2020-fsh'

file = downloadIfNeeded(url_sagasti,file_prefix_pdf + name + '.pdf' ,mode = 'rb')
speech = readPDF(file)

with open(file_prefix_txt + name + '.txt', 'w') as text_file:
        text_file.write(speech)
