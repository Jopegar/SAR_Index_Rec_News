import sys
import pickle as loader
import re

termSearch = []
dictTerms = {}
dictTitle = {}
dictCategory = {}
dictDate = {}
dictNews = {}
dictDocs = {}


def find_index(index_dir):
    try:
        return loader.load(open(index_dir, "rb"))
    except loader.PickleError:
        print("There is not such a directory")
        return None


def AAndBSearch(newsTermOne, newsTermTwo):
    resultNews = []

    indexOne = indexTwo = 0

    while indexOne < len(newsTermOne) and indexTwo < len(newsTermTwo):
        if newsTermOne[indexOne] == newsTermTwo[indexTwo]:
            resultNews.append(newsTermOne[indexOne])
            indexOne += 1
            indexTwo += 1

        elif newsTermOne[indexOne] < newsTermTwo[indexTwo]:
            indexOne += 1

        else:
            indexTwo += 1

    return resultNews


def AAndNotBSearch(newsTermOne, newsTermTwo):
    resultNews = []

    indexOne = indexTwo = 0

    while indexOne < len(newsTermOne) and indexTwo < len(newsTermTwo):
        if newsTermOne[indexOne] == newsTermTwo[indexTwo]:
            indexOne += 1
            indexTwo += 1

        elif newsTermOne[indexOne] < newsTermTwo[indexTwo]:
            resultNews.append(newsTermOne[indexOne])
            indexOne += 1

        else:
            indexTwo += 1

    while indexOne < len(newsTermOne):
        resultNews.append(newsTermOne[indexOne])
        indexOne += 1

    return resultNews


def NotASearch(newsTerm):
    resultNews = []
    for newID, value in dictNews.items():
        resultNews.append(newID)

    resultNews = AAndNotBSearch(resultNews, newsTerm)

    return resultNews


def AOrBSearch(newsTermOne, newsTermTwo):
    resultNews = []

    indexOne = indexTwo = 0

    while indexOne < len(newsTermOne) and indexTwo < len(newsTermTwo):
        if newsTermOne[indexOne] == newsTermTwo[indexTwo]:
            resultNews.append(newsTermOne[indexOne])
            indexOne += 1
            indexTwo += 1

        elif newsTermOne[indexOne] < newsTermTwo[indexTwo]:
            resultNews.append(newsTermOne[indexOne])
            indexOne += 1

        else:
            resultNews.append(newsTermTwo[indexTwo])
            indexTwo += 1

    while indexOne < len(newsTermOne):
        resultNews.append(newsTermOne[indexOne])
        indexOne += 1

    while indexTwo < len(newsTermTwo):
        resultNews.append(newsTermTwo[indexTwo])
        indexTwo += 1

    return resultNews


def searcher(query):
    query = query.split()
    condQuery = ["AND", "OR", "NOT"]

    # we are going to process the advanced and the normal query first
    for partQuery in query:
        if partQuery not in condQuery:
            currentIndex = query.index(partQuery)
            if ":" in partQuery:
                header = partQuery.split(":")[0]
                term = partQuery.split(":")[1].lower()

                if term.isalpha():
                    if "headline" in header:
                        if term in dictTitle:
                            query[currentIndex] = dictTitle[term]
                        else:
                            print("The term %s is not in any title.\n" % term)
                            return

                    elif "category" in header:
                        if term in dictCategory:
                            query[currentIndex] = dictCategory[term]
                        else:
                            print("The category %s not exist.\n" % term)
                            return

                    else:
                        if term in dictTerms:
                            newsTerm = []
                            for newID, value in dictTerms[term].items():
                                newsTerm.append(newID)
                            query[currentIndex] = newsTerm
                            termSearch.append(term)
                        else:
                            print("The term %s is not in a news.\n" % term)
                            return

                else:
                    if "date" in header:
                        if term in dictDate:
                            query[currentIndex] = dictDate[term]
                        else:
                            print("In the date %s there are any news.\n" % term)
                            return

                    else:
                        print("The word " + term + " is not valid for the search. Please just alphanumerics terms\n")
                        return

            else:
                if partQuery in dictTerms:
                    newsTerm = []
                    for newID, value in dictTerms[partQuery].items():
                        newsTerm.append(newID)
                    query[currentIndex] = newsTerm
                    termSearch.append(partQuery)
                else:
                    print("The term %s is not in a news.\n" % partQuery)
                    return

    while "NOT" in query:
        currentIndex = query.index("NOT")
        newsTerm = query[currentIndex + 1]

        query[currentIndex] = NotASearch(newsTerm)

        del query[currentIndex + 1]

    index = 0
    while index < len(query):
        if not isinstance(query[index], list):
            index += 1

        elif index + 1 < len(query) and isinstance(query[index + 1], list):
            query[index] = AAndBSearch(query[index], query[index + 1])
            del query[index + 1]

        else:
            index += 2

    while len(query) > 1:
        if "AND" in query[1]:
            query[0] = AAndBSearch(query[0], query[2])
            del query[2]
            del query[1]

        elif "OR" in query[1]:
            query[0] = AOrBSearch(query[0], query[2])
            del query[2]
            del query[1]

    printResult(query[0])


def printResult(resultNews):

    if len(resultNews) < 3:
        for newsID in resultNews:
            resultDoc = dictNews[newsID]
            docID = resultDoc[0]
            posNew = resultDoc[1]

            newsDoc = dictDocs[docID]
            newsContent = newsDoc[posNew]

            title = newsContent['headline']
            text = newsContent['text']

            print(title + '\n' + text + '\n')

    elif len(resultNews) < 6:
        for newsID in resultNews:
            resultDoc = dictNews[newsID]
            docID = resultDoc[0]
            posNew = resultDoc[1]

            newsDoc = dictDocs[docID]
            newsContent = newsDoc[posNew]

            title = newsContent['headline']
            text = newsContent['text']

            text = re.findall("\w+", text)

            if len(termSearch) > 0:
                for term in termSearch:
                    dictResult = dictTerms[term]
                    positionTerm = dictResult[newsID]

                    print(title + '\n')

                    for position in positionTerm:
                        print(" ".join(text[max(0, position - 25):min(position + 25, len(text) - 1)]) + "\n\n")

    else:
        for newsID in resultNews:
            resultDoc = dictNews[newsID]
            docID = resultDoc[0]
            posNew = resultDoc[1]

            newsDoc = dictDocs[docID]
            newsContent = newsDoc[posNew]

            title = newsContent['headline']

            print(title + '\n')

    print(len(resultNews))

if len(sys.argv) != 2:
    print("CORRECT WAY TO START: python SAR_searcher.py <index directory>\n")
else:
    index = find_index(sys.argv[1])
    if index is None:
        exit(0)
    else:
        dictDocs = index[0]
        dictNews = index[1]
        dictTerms = index[2]
        dictTitle = index[3]
        dictCategory = index[4]
        dictDate = index[5]

    query = "begin"
    while query != "":
        query = input("What do you want to search? (You can know the differents forms of the query if you input ""+info+"")(if you want to exit, type ""+exit+"")\n")
        termSearch = []
        if '+info+' in query:
            print("The diferent types of query you can do is: \n\t"
                  "1. term -> search the news where ""term"" is\n\t"
                  "2. headline:term text:term category:term date:term -> advanced search\n\t"
                  "3. term AND term, term OR term, NOT term or a mix\n\t")

        elif '+exit+' in query:
            exit(0)
        else:
            searcher(query)