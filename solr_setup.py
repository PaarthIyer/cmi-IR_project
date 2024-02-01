import requests
import sys

def add_field(core,name, typee="text_en", link = "http://localhost:8983/solr/"):
    field = {
        "add-field":{
            "name":name,
            "type":typee,
            "stored":"true" }}
    req = requests.post(link+core+"/schema",json=field)
    return req

if __name__=="__main__":
    core = sys.argv[1]
    add_field(core, "headlines")
    add_field(core, "text")
