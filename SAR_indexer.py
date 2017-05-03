import sys
import glob


def indexer(directory):
    fileList = glob.glob(directory + "/*.sgml")

    if fileList == []:
        print ("There is not such a directory")

    else:
        dictNews = {}

        for fileName in fileList:
            with open(fileName, 'r') as file:
                dictNews [docID] =


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("CORRECT WAY TO START: python SAR_indexer.py <news directory> <file to save index>\n")
    else:
