
import pandas  as pandas



def wordCounter(wordLst):
    wordCounts = {}
    for word in wordLst:
        #We usually need to normalize the case
        if type(word) != tuple:
            wLower = word.lower()
        else:
            wLower = word
        if wLower in wordCounts:
            wordCounts[wLower] += 1
        else:
            wordCounts[wLower] = 1
    #convert to DataFrame
    countsForFrame = {'word' : [], 'count' : []}
    for w, c in wordCounts.items():
        countsForFrame['word'].append(w)
        countsForFrame['count'].append(c)

    df = pandas.DataFrame(countsForFrame)

    df.sort_values(['count'], ascending = False, inplace = True)

    return df


def contar_esp(lst,  palabra):
    counter = lst.count(palabra)
    return counter