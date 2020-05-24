default: clean install copy zip

install: build_path
	 pip install -r requirements-lambda.txt -t ./build

build_path:
	mkdir ./build

build_dist:
	mkdir ./dist

copy:
	ls -alh
	cp -R src/* ./build/
	ls -alh ./build

zip: build_dist
	cd ./build && zip -r9 ./dist/lambda.zip . 2>&1 >>/dev/null

clean:
	rm -rf ./build
	rm -rf ./dist