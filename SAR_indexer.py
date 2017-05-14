import sys
import glob
import re
import pickle as saver
import time
import codecs

dictDocs = {}
dictNews = {}
dictTerms = {}
dictTitle = {}
dictCategory = {}
dictDate = {}


def indexer(directory, savePath):
    start_time = time.time()

    fileList = glob.glob(directory + "/*.sgml")

    if not fileList:
        print("There is not such a directory")

    else:
        for fileName in fileList:

            file = codecs.open(fileName, 'r', 'utf-8')
            docContent = file.read()
            docID = fileName.split('.')[0].split('\\')[2]

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

                    postList = dictCategory.get(category.lower(), [])
                    postList.append(newsID)
                    dictCategory[category] = postList

                    postList = dictDate.get(date, [])
                    postList.append(newsID)
                    dictDate[date] = postList

                    postList = dictDocs.get(docID, [])
                    postList.append({'headline': title, 'text': text, 'category': category, 'date': date})
                    dictDocs[docID] = postList

                    title = re.findall("\w+", title.lower())

                    for term in title:
                        postList = dictTitle.get(term, [])
                        if newsID not in postList:
                            postList.append(newsID)
                        dictTitle[term] = postList

                    dictNews[newsID] = (docID, posNews)

                    text = re.findall("\w+", text.lower())

                    posTerm = 0

                    for term in text:
                        dictAux = dictTerms.get(term, {})
                        postList = dictAux.get(newsID, [])
                        postList.append(posTerm)
                        dictAux[newsID] = postList
                        dictTerms[term] = dictAux
                        posTerm += 1
                    posNews += 1

            saver.dump((dictDocs, dictNews, dictTerms, dictTitle, dictCategory, dictDate), open(savePath, "wb"))
    print("--- %s seconds ---" % (time.time() - start_time))


if len(sys.argv) != 3:
    print("CORRECT WAY TO START: python SAR_indexer.py <news directory> <file to save index>\n")
else:
    indexer(sys.argv[1], sys.argv[2])

