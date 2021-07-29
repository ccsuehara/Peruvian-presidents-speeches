
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


def remove_stop(lst, lst_stop):
    new_lst = []
    for word in lst: 
        if word in lst_stop:
            pass
        else:
            new_lst.append(word)
    return new_lst


def count_stops(lst, lst_stop):
    counter = 0
    for word in lst: 
        if word in lst_stop:
            counter += 1

    return counter