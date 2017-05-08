import sys
import pickle as loader


def find_index(index_dir):
    try:
        return loader.load(open(index_dir, "rb"))
    except loader.PickleError:
        print("There is not such a directory")
        return None


def searcher(query, index):
    provisionalQueryList = []
    for parameter in query:
        for word in parameter:
            header = ''
            searchText = ''
            headerComplete = False
            for letter in word:
                if not letter.isalpha() or letter != ':':
                    print("The word" + word + "is not valid for the search.\n")
                    return
                else:
                    if letter != ':':
                        if headerComplete:
                            header += letter
                        else:
                            searchText += letter
                    else:
                        headerComplete = True
            if not headerComplete and header != '':
                provisionalQueryList.append('text', header)
            else:
                if header in ['headline', 'text', 'category', 'date']:
                    provisionalQueryList.append((header, searchText))
                else:
                    print("The parameter" + header + 'is not valid.\n')
                    return
                if searchText == '':
                    print('The search cannot be blank.\n')
                    return
    countList = {'headline': 0, 'text': 0, 'category': 0, 'date': 0}
    for param in provisionalQueryList:
        countList[param[0]] += 1

    for count in countList:
        if count[1] > 1:
            print('There are more than one' + count[0] + '.\n')
            return

    queryList = {}
    for query in provisionalQueryList:
        queryList[query[0]] = query[1]

    dictDocs = index[0]
    dictNews = index[1]
    dictTerms = index[2]
    dictTitle = index[3]
    dictCategory = index[4]
    dictDate = index[5]


    print("The query " + query[0] + "is in the next news:\n")

    if len(resultNews) < 3:
        for result in resultNews:
            newsID = result[0]

            resultDoc = dictNews[newsID]
            docID = resultDoc[0]
            posNew = resultDoc[1]

            newsDoc = dictDocs[docID]
            newsContent = newsDoc[posNew]

            title = newsContent['headline']
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

            title = newsContent['headline']
            text = newsContent['text']

            positionTerm = result[1]

            print(title + '\n')

            for position in positionTerm:
                textPos = text.split()
                print(textPos[max(0, position-10):min(position+10, len(text)-1)] + "\n\n")

    else:
        for result in resultNews:
            newsID = result[0]

            resultDoc = dictNews[newsID]
            docID = resultDoc[0]
            posNew = resultDoc[1]

            newsDoc = dictDocs[docID]
            newsContent = newsDoc[posNew]

            title = newsContent['headline']

            print(title + '\n')

if len(sys.argv) != 2:
    print("CORRECT WAY TO START: python SAR_searcher.py <index directory>\n")
else:
    index = find_index(sys.argv[1])
    if index is None:
        exit(0)

    query = "begin"
    while query != "":
        query = input("What do you want to search? \n").split()
        searcher(query, index)