# Here's a shell script that adds and commits changes in a Git repository in smaller chunks of 500 MB:

#!/bin/bash

# Usage: git-add-commit.sh <message>

# Check if a commit message was provided
if [ $# -eq 0 ]; then
  echo "Error: No commit message provided"
  exit 1
fi

# Store the commit message in a variable
message="$1"

# Function to determine the size of a file in MB
function size_in_mb() {
  echo $(( $(wc -c < "$1") / 1048576 ))
}

# Store the sum of sizes of staged files in a variable
staged_size=$(git diff --cached --name-only | xargs du -c | tail -n 1 | awk '{print $1}')

# Add changes in smaller chunks
while [ "$staged_size" -gt 0 ]; do
  chunk_size=0
  for file in $(git diff --name-only --cached); do
    file_size=$(size_in_mb "$file")
    if [ "$((chunk_size + file_size))" -le 500 ]; then
      chunk_size=$((chunk_size + file_size))
      git add "$file"
    fi
  done
  git commit -m "$message"
  staged_size=$(git diff --cached --name-only | xargs du -c | tail -n 1 | awk '{print $1}')
done