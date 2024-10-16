#!/bin/bash

# Directory containing files to rename
TARGET_DIR="/app/asr_data/Sam/1"

# Directory to move renamed files
DEST_DIR="/app/asr_data/Sam/1/"

# Create the destination directory if it does not exist
mkdir -p "$DEST_DIR"

# Loop through each .wav file in the target directory
for FILE in "$TARGET_DIR"/*.wav; do
    # Extract the filename without the directory path
    BASENAME=$(basename "$FILE")
    
    # Remove any "_#" pattern followed by numbers from the filename
    NEWNAME=$(echo "$BASENAME" | sed 's/_[0-9]*//g')
    
    # Define the destination file path
    DEST_FILE="$DEST_DIR/$NEWNAME"
    
    # Rename and move the file only if the new name is different
    if [ "$BASENAME" != "$NEWNAME" ]; then
        echo "Renaming and moving: $BASENAME --> $DEST_FILE"
        mv "$FILE" "$DEST_FILE"
    else
        echo "Moving: $BASENAME --> $DEST_FILE"
        mv "$FILE" "$DEST_FILE"
    fi
done

echo "Rename and move complete."
