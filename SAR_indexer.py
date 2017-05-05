import sys
import glob
import re
import pickle as saver

clean_re = re.compile('\W+')

dictDocs = {}
dictNews = {}
dictTerms = {}


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
            docId = fileName.split('.')[0].split('\\')[1]
            dictDocs[docId] = docContent
            newsList = docContent.split('</DOC>')
            finalSpace = newsList[len(newsList) - 1]

            posNews = 0

            for news in newsList:

                if news != finalSpace:
                    posNews += 1
                    newsId = news.split('<DOCID>')[1].split('</DOCID>')[0]
                    # title = news.split('<TITLE>')[1].split('</TITLE>')[0]
                    text = news.split('<TEXT>')[1].split('</TEXT>')[0]
                    # category = news.split('<CATEGORY>')[1].split('</CATEGORY>')[0]
                    # date = news.split('<DATE>')[1].split('</DATE>')[0]
                    # dictNews[newsId] = {'headline': title, 'text': text, 'category': category, 'date': date}
                    dictNews[newsId] = (docId, posNews)
                    text = clean_news(text).replace("\n", " ")
                    text = text.replace("\t", " ")
                    text = text.split(" ")

                    posTerm = 0

                    for term in text:

                        try:
                            if dictTerms[term] is not None:
                                found = False
                                for case in dictTerms[term]:
                                    if case[0] == newsId:
                                        case[1].append(posTerm)
                                        found = True
                                        break
                                if not found:
                                    dictTerms[term].append([newsId, [posTerm]])
                        except KeyError:
                            dictTerms[term] = [[newsId, [posTerm]]]

            saver._dump((dictDocs, dictNews, dictTerms), open(savePath, "wb"))


if len(sys.argv) != 3:
    print("CORRECT WAY TO START: python SAR_indexer.py <news directory> <file to save index>\n")
else:
    indexer(sys.argv[1], sys.argv[2])

