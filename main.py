import getopt, sys
import pathlib
from NamedEntityRec import *
from ner_solr import *
import json, pprint


def print_help():
    print("\nArguments help")
    print("-h | --Help       : Display Arguments help")
    print("\nSolr indexing : ")
    print("-i | --Index      : Index a single JSON file with multiple entries")
    print("-m | --MultiIndex : Index multiple JSON from directory")
    print("-s | --Search     : Search in specified core")
    print("-q | --Query      : Look at solr query")
    print("\nStanford NER utils : ")
    print("-n | --FileNER    : Perform NER on a txt file, and save it to tagged.json\n")

if __name__=="__main__":
    argumentList = sys.argv[1:]
    if len(argumentList) == 0:
        print_help()

    options = "himsqn"

    long_options = ["Help", "Index", "MultiIndex","Search","Query","FileNER"]

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--Help"):
                print_help()
                
            elif currentArgument in ("-i", "--Index"):
                core = input("\nEnter core : ")
                x = input("Enter file name (relative to ./data) :  ")
                print("")
                IndexJSON(x, core_obj(core))
                
            elif currentArgument in ("-m", "--MultiIndex"):
                core = input("\nEnter core : ")
                x = input("Enter dir path (relative to ./data) :  ")
                print("")
                IndexJSONFiles(x, core_obj(core))

            elif currentArgument in ("-s", "--Search"):
                core = input("\nEnter core : ")
                x = input("Input search query :  ")
                SearchSolr(x, core_obj(core))
                print("################\nOutput stored in Output.txt\n################")

            elif currentArgument in ("-q", "--Query"):
                x = input("Input search query :  ")
                print(FormQuery(x))
                print("")
                
            elif currentArgument in ("-n","--FileNER"):
                x = input("\nInput txt file name (relative to ./data) :  ")
                print("\n")
                file_extension = pathlib.Path(x).suffix
                if file_extension == ".txt":
                    sample = file_ner("./data/"+x)
                    pprint.pprint(sample);print("\n")
                    with open("tagged.json", 'w') as fl:
                        json.dump(sample, fl, indent=4)
                else:
                    print("Incorrect file format\n")

    except getopt.error as err:
        print(str(err))