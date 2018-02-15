all: install

install: cacm cs276 build

requirements:
	pip install -r requirements.txt

cacm: cacm_folder temp
	wget -O temp/cacm.tar.gz http://ir.dcs.gla.ac.uk/resources/test_collections/cacm/cacm.tar.gz
	tar --directory=Data/CACM -xvf temp/cacm.tar.gz cacm.all common_words qrels.text query.text

cs276: cs276_folder temp
	wget -O temp/pa1-data.zip http://web.stanford.edu/class/cs276/pa/pa1-data.zip
	unzip -d Data/CS276 temp/pa1-data.zip 'pa1-data/*'
	mv Data/CS276/pa1-data/* Data/CS276
	rm -r Data/CS276/pa1-data

build: index_folder collection_folder requirements temp
	python build.py

temp:
	mkdir -p temp/

cacm_folder:
	mkdir -p Data/CACM/

cs276_folder:
	mkdir -p Data/CS276/

index_folder:
	mkdir -p Data/Index/

collection_folder:
	mkdir -p Data/Collection/
	mkdir -p Data/Collection/CS276/

.PHONY: clean mrproper

clean:
	rm -r temp/

mrproper:
	rm -r Data/CACM/
	rm -r Data/CS276/
	rm -r Data/Index/
	rm -r Data/Collection/
