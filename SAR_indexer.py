import sys
import glob


def indexer(directory):

    fileList = glob.glob(directory + "/*.sgml")

    if fileList == []:
        print("There is not such a directory")

    else:
        dictFiles = {}
        dictNews = {}

        for fileName in fileList:
            file = open(fileName, 'r')
            fileContent = file.read()
            dictFiles[fileName.split('.')[0].split('\\')[1]] = fileContent
            newsList = fileContent.split('</DOC>')
            aux = newsList[len(newsList)-1]
            for new in newsList:
                if new != aux:
                    newId = new.split('<DOCID>')[1].split('</DOCID>')[0]
                    title = new.split('<TITLE>')[1].split('</TITLE>')[0]
                    text = new.split('<TEXT>')[1].split('</TEXT>')[0]
                    category = new.split('<CATEGORY>')[1].split('</CATEGORY>')[0]
                    date = new.split('<DATE>')[1].split('</DATE>')[0]
                    dictNews[newId] = {'headline': title, 'text': text, 'category': category, 'date': date}

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #    print("CORRECT WAY TO START: python SAR_indexer.py <news directory> <file to save index>\n")
    # else:
    # indexer(sys.argv[1])
    indexer('/mini_enero')
