cd /d D:\stanford-ner-4.2.0

java -mx500m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -port 9191 -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -tokenizerOptions splitHyphenated=false
