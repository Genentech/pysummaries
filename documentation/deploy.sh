#!/bin/bash

# just clean the output folder and copy the built hmtl there
# you still need to commit and push so that the bee or RSConnect output gets
# refreshed

cp -r book/_build/html/* ../docs
touch ../docs/.nojekyll

