import sys
import pickle as loader


def find_index(index_dir):
    try:
        return loader.load(open(index_dir, "rb"))
    except loader.PickleError:
        print("There is not such a directory")
        return None


def searcher(query, index):
    dictDocs = index[0]
    dictNews = index[1]
    dictTerms = index[2]

    resultNews = dictTerms[query]

    print("The query " + query + "is in the next news:\n")

    if len(resultNews) < 3:
        for result in resultNews:
            newsID = result[0]

            resultDoc = dictNews[newsID]
            docID = resultDoc[0]
            posNew = resultDoc[1]

            newsDoc = dictDocs[docID]
            newsContent = newsDoc[posNew]

            title = newsContent['title']
            text = newsContent['text']

            print(title + '\n' + text + '\n')

    elif len(resultNews) < 6:
        for result in resultNews:
            newsID = result[0]

            resultDoc = dictNews[newsID]
            docID = resultDoc[0]
            posNew = resultDoc[1]

            newsDoc = dictDocs[docID]
            newsContent = newsDoc[posNew]

            title = newsContent['title']

            for position in result
            text = newsContent['text']

            print(title + '\n' + text + '\n')



if len(sys.argv) != 2:
    print("CORRECT WAY TO START: python SAR_searcher.py <index directory>\n")
else:
    index = find_index(sys.argv[1])
    if index is None:
        exit(0)

    query = "begin"
    while query != "":
        query = input("What do you want to search? \n")

        if query.isalpha():
            searcher(query.lower(), index)

        else:
            print("Anything but letters are not allowed\n")