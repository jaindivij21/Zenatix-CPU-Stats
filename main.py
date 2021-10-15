import json
import os
from elasticsearch import Elasticsearch
from src import helpers as proc


def main():
    # get the results -> stores process data every minute for 10 minutes (10 entries)
    result = proc.listOfProcesses()  # result is a list of list of dictionaries

    # get the process list excerpt (10 pids) from the first* minute
    excerpt = proc.getExcerpt(result[0])

    # get the processes list which use more than 2% of memory for the first* minute
    highMem = proc.highMemUsage(result[0])

    # establish connection to the elastic search
    es = Elasticsearch(HOST="http://localhost", POST=9200)
    es = Elasticsearch()

    i = 1
    for minute in result:
        # minute is a list of dict
        for dict in minute:
            es.index(index="processes", doc_type="proc", id=i, document=dict)
            i += 1


if __name__ == '__main__':
    main()
