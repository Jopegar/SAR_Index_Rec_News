import sys
import re
import pickle as saver
import time
import codecs
import os

dictNews = {}
dictTerms = {}
dictTitle = {}
dictCategory = {}
dictDate = {}


def indexer(directory, savePath):

    start_time = time.time()

    for (path, names, fileList) in os.walk(directory):

        fileList.sort()

        if not fileList:
            print("There is not such a directory")

        else:
            for fileName in fileList:
                # docID = fileName.split('.')[0]
                fileName = path + "/" + fileName
                file = codecs.open(fileName, 'r', 'utf-8')
                docContent = file.read()

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

                        title = re.findall("\w+", title.lower())

                        posTerm = 0

                        for term in title:
                            postInver = dictTitle.get(term, [])

                            positions = []

                            if len(postInver) > 0:
                                postList = postInver[-1]
                                if postList[0] == newsID:
                                    postList[1].append(posTerm)
                                    posTerm += 1
                                    continue

                            positions.append(posTerm)
                            postInver.append([newsID, positions])
                            dictTitle[term] = postInver
                            posTerm += 1

                        dictNews[newsID] = (fileName, posNews)

                        text = re.findall("\w+", text.lower())

                        posTerm = 0

                        for term in text:
                            postInver = dictTerms.get(term, [])

                            positions = []

                            if len(postInver) > 0:
                                postList = postInver[-1]
                                if postList[0] == newsID:
                                    postList[1].append(posTerm)
                                    posTerm += 1
                                    continue

                            positions.append(posTerm)
                            postInver.append([newsID, positions])
                            dictTerms[term] = postInver
                            posTerm += 1
                        posNews += 1

    for (pathSaver, names, fileList) in os.walk(savePath):
        savePath = pathSaver + "/" + fileList[0]
    saver.dump((dictNews, dictTerms, dictTitle, dictCategory, dictDate), open(savePath, "wb"))
    print("--- %s seconds ---" % (time.time() - start_time))


if len(sys.argv) != 3:
    print("CORRECT WAY TO START: python SAR_indexer.py <news directory> <file to save index>\n")
else:
    indexer(sys.argv[1], sys.argv[2])

