from sner import Ner
import json

"""
run this in the ner folder
java -mx500m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -port 9191 -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -tokenizerOptions splitHyphenated=false
"""


def Named_Entities(iob):
    root = []
    for token in iob:
        if token[1] == 'O':
            root.append('O')
        else:
            try:
                word = token[0]
                word = word.replace('\r', '')
                if root[-1][0] == token[1]:
                    root[-1] = (token[1], root[-1][1] + " " + word)
                else:
                    root.append((token[1], word))
            except:
                word = token[0]
                word = word.replace('\r', '')
                root.append((token[1], word))
    root = list(set(root))
    try:
        root = [x for x in root if not x == 'O']
    except:
        pass
    return root


def file_ner(file_name):
    with open(file_name, encoding="utf8") as f:
        lines = f.readlines()

    lines = ("".join(lines)).replace("\n", " ")

    tagger = Ner(host='localhost', port=9191)
    classif_text = tagger.get_entities(lines)

    taggs = Named_Entities(classif_text)

    result = {}
    for i in taggs:
        result.setdefault(i[0], []).append(i[1])
    return result


def text_ner(text):
    tagger = Ner(host='localhost', port=9191)
    classif_text = tagger.get_entities(text)

    taggs = Named_Entities(classif_text)

    result = {}
    for i in taggs:
        result.setdefault(i[0], []).append(i[1])
    return result


def JSONlabel(filename, to_tag=["headlines", "text"]):
    with open(filename) as json_file:
        original = json.load(json_file)
        tags = text_ner(". ".join([original[x] for x in to_tag]))
        tagged_json = original | tags
    return tagged_json
