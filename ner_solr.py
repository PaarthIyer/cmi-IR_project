# from SolrIndex import *
from NamedEntityRec import *
import pysolr
import json
import os
import string


def core_obj(x):
    link = 'http://localhost:8983/solr/'+x+'/'
    return pysolr.Solr(link, always_commit=True)


def IndexJSON(filename, solr, to_tag=["headlines", "text"], dirpath="./data/"):
    print("Tagging files...")
    filepath = dirpath+filename

    # We keep a tagged copy if we want to index again
    if not os.path.isfile("./NER_TAGGED files/NER_TAGGED_"+os.path.basename(filepath)):
        bunched_files = []

        # read the file
        with open(filepath) as json_file:
            data = json.load(json_file)

        # some init for prograss bar
        i = 0
        num = len(data)
        cn = 0

        # for each of the docs in the json, we combine their to_tag fields,
        #          tag them with the returned tags, and add that tagged doc
        #          to bunched_files
        for original in data:
            tags = text_ner(". ".join([original[x] for x in to_tag]))
            tagged_json = original | tags
            bunched_files.append(tagged_json)
            i += 1

            # prograssbar
            if (i > cn*num/20):
                cn += 1
                print("\033[A"+"Tagging Progress : ["+"#"*cn+"-"*(20-cn)+"]")

        # save the tagged copy
        with open("./NER_TAGGED files/NER_TAGGED_"+os.path.basename(filepath), "w") as f:
            f.write(json.dumps(bunched_files, indent=4))
    else:
        with open("./NER_TAGGED files/NER_TAGGED_"+os.path.basename(filepath)) as json_file:
            bunched_files = json.load(json_file)

    print("Files tagged with named entities. Indexing...")

    # index the files
    solr.add(bunched_files)

    print("\033[A\033[A")
    print("Files Indexed                                 \n")


def FormQuery(string1):

    # get the tags for the query
    tags = text_ner(string1)

    # set default field to text
    args = {'df': 'text'}

    # add the initial query as default query
    query = string1+' '

    # for each of the tags, we weigh it by 2 in it's own field, and by 0.6 in other fields
    for key in tags.keys():
        for word in tags[key]:
            query += " ".join([key+":"+x+"^2" for x in word.split()])+" "
            # for key_ in tags.keys():
            #     if key_ is not key:
            #         query += " ".join([key_+":"+x +
            #                           "^0.6 " for x in word.split()])

    return query

# Remember to capitalize properly
def SearchSolr(string1, solr, save=True, out=["headlines"], file_write=["headlines", "text"], numres=10):

    # set default field to text
    args = {'df': 'text'}

    # add the initial query as default query
    query = FormQuery(string1)

    # search
    results = solr.search(query, **args)

    # print the results
    print("\n")
    j = 0
    for res in results:
        j += 1
        for i in out:
            print(res[i])
        print("\n")
        if (j >= numres):
            break

    # save the results
    if save:
        with open("./Output.txt", "w") as outfile:
            for res in results:
                for i in file_write:
                    outfile.write(
                        ''.join(x for x in res[i] if x in string.printable) + "\n\n")
                outfile.write("\n###########################\n\n")



def IndexJSONFiles(dirname, solr, dirpath="./data/"):

    print("Tagging files...")

    dirpath = dirpath+dirname
    bunched_files = []
    listdir = os.listdir(dirpath)
    i = 0
    num = len(listdir)
    cn = 0
    if dirpath[-1] != '/':
        dirpath += '/'
    for file in listdir:
        if file.endswith(".json"):
            bunched_files.append(JSONlabel(dirpath+file))
        i += 1
        if (i > cn*num/20):
            cn += 1
            print("\033[A"+"Tagging Progress : ["+"#"*cn+"-"*(20-cn)+"]")

    print("\033[A                                      \033[A")
    print("Files tagged with named entities. Indexing...")
    solr.add(bunched_files)
    print("\033[A\033[A")
    print("Files Indexed                                 \n")
