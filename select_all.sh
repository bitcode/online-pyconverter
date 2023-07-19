#!/bin/bash

# Clear the clipboard
echo -n '' | xsel -b

# Iterate over the files
for file in app.py requirements.txt templates/upload.html
do
    echo "File: $file" | xsel -b -a
    echo "" | xsel -b -a
    cat "$file" | xsel -b -a
    echo "" | xsel -b -a
done
