################
# MAKEFILE
# This makefile defines directives to work with jupyterbook
# commands
# all: builds the book then deploys to output
# build: build the book. The result will be in analysis/_build/html
# clean: cleans the book and the output folder.
# clean_book: remove analysis/_build Useful to clean all the cache.
# clean_output: cleans the output folder
# dev_server: start a server on port 10000 to inspect the book. You need to have a tunnel to the remote machine from your local machine
#             then visit 127.0.0.1:10000 in your local machine.
#             You can make a ssh connection with port forwarding with : ssh yourcontainer -L :10000:127.0.0.1:10000
# deploy: copies analysis/_build/html to ../output and writes a manifest file for RSconnect. You still need to commit and push to github.

.PHONY: all build clean_book clean_output env_setup dev_server

all: clean_book build clean_output deploy

build:
	jupyter-book build book

clean_book:
	rm -rf book/_build

clean_output:
	rm -rf ../docs/*

dev_server:
	python -m http.server 10000 -d book/_build/html

env_setup:
	./env_setup.sh

deploy:
	./deploy.sh
