#!/bin/bash

# Base directory is the current working directory (assuming you're running the script from the project root)
PROJECT_DIR="."

# Loop through all files in the project directory and its subdirectories, excluding unnecessary files and directories
find "$PROJECT_DIR" -type d \( -name 'node_modules' -o -name '.git' -o -name 'images' -o -name 'dist' -o -name 'build' \) -prune \
    -o -type f \( -name '*.DS_Store' -o -name '*.webp' -o -name '*.jpeg' -o -name '*.pdf' -o -name '*.ico' -o -name '*.png' -o -name '*.pyc' -o -name '*.md' -o -name '*.gitignore' -o -name 'LICENSE' -o -name '*.csv' -o -name 'review_code.sh' -o -name 'list.txt' \) -prune \
    -o -type f -exec echo "---- START OF {} ----" \; -exec cat {} \; -exec echo "---- END OF {} ----" \; -exec echo \;
