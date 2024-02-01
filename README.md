Start NER with (in sner home)
java -mx500m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -port 9191 -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -tokenizerOptions splitHyphenated=false

Start solr 
create a core
run "python solr_setup.py"
run "python main.py -h" 
continue


Data is stored in ./data
./NER_TAGGED stores already tagged files to reduce computation if the files are called again

./solr_home has the solr cores and data
