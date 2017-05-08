import sys
import glob
import re
import pickle as saver

clean_re = re.compile('\W+')

dictDocs = {}
dictNews = {}
dictTerms = {}
dictTitle = {}
dictCategory = {}
dictDate = {}


def clean_news(text):
    text = clean_re.sub(' ', text).lower()
    return text


def indexer(directory, savePath):
    fileList = glob.glob(directory + "/*.sgml")

    if fileList == []:
        print("There is not such a directory")

    else:
        for fileName in fileList:

            file = open(fileName, 'r')
            docContent = file.read()
            docID = fileName.split('.')[0].split('\\')[1]

            newsList = docContent.split('</DOC>')
            finalSpace = newsList[len(newsList) - 1]

            posNews = 0

            for news in newsList:

                if news != finalSpace:
                    newsID = news.split('<DOCID>')[1].split('</DOCID>')[0]
                    title = news.split('<TITLE>')[1].split('</TITLE>')[0]
                    text = news.split('<TEXT>')[1].split('</TEXT>')[0]
                    category = news.split('<CATEGORY>')[1].split('</CATEGORY>')[0].lower()
                    date = news.split('<DATE>')[1].split('</DATE>')[0]

                    title = clean_news(title).replace("\n", " ")
                    title = title.replace("\t", " ")
                    title = title.split(" ")

                    for term in title:
                        term = term.lower()
                        try:
                            if dictTitle[term] is not None:
                                dictTitle[term].append(newsID)
                        except KeyError:
                            dictTitle[term] = [newsID]

                    try:
                        if dictCategory[term] is not None:
                            dictCategory[term].append(newsID)
                    except KeyError:
                        dictCategory[term] = [newsID]

                    try:
                        if dictDate[date] is not None:
                            dictDate[date].append(newsID)
                    except KeyError:
                        dictDate[date] = [newsID]

                    try:
                        if dictDocs[docID] is not None:
                            dictDocs[docID].append({'headline': title, 'text': text, 'category': category, 'date': date})
                    except KeyError:
                        dictDocs[docID] = [{'headline': title, 'text': text, 'category': category, 'date': date}]

                    dictNews[newsID] = (docID, posNews)

                    text = clean_news(text).replace("\n", " ")
                    text = text.replace("\t", " ")
                    text = text.split(" ")

                    posTerm = 0

                    for term in text:
                        term = term.lower()
                        try:
                            if dictTerms[term] is not None:
                                found = False
                                for case in dictTerms[term]:
                                    if case[0] == newsID:
                                        case[1].append(posTerm)
                                        found = True
                                        break
                                if not found:
                                    dictTerms[term].append([newsID, [posTerm]])
                        except KeyError:
                            dictTerms[term] = [[newsID, [posTerm]]]
                    posNews += 1

            saver._dump((dictDocs, dictNews, dictTerms, dictTitle, dictCategory, dictDate), open(savePath, "wb"))


if len(sys.argv) != 3:
    print("CORRECT WAY TO START: python SAR_indexer.py <news directory> <file to save index>\n")
else:
    indexer(sys.argv[1], sys.argv[2])

