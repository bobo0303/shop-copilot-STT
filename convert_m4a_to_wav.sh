#!/bin/bash  
  
# Directory containing m4a files  
SOURCE_DIR="/app/asr_data/Sam"  
  
# Directory where you want to save wav files  
OUTPUT_DIR="/app/asr_data/Sam"  
  
# Create output directory if it does not exist  
mkdir -p "$OUTPUT_DIR"  
  
# Loop through each m4a file in the source directory  
for FILE in "$SOURCE_DIR"/*.m4a; do  
    # Extract the filename without the extension  
    BASENAME=$(basename "$FILE" .m4a)  
      
    # Define the output filename  
    OUTPUT_FILE="$OUTPUT_DIR/$BASENAME.wav"  
      
    # Convert m4a to wav using ffmpeg  
    if ffmpeg -i "$FILE" -acodec pcm_s16le -ar 44100 "$OUTPUT_FILE"; then
        # If conversion was successful, remove the original .m4a file
        rm "$FILE"
        echo "Successfully converted and removed: $FILE"
    else
        echo "Conversion failed for: $FILE"
    fi  
done  
  
echo "Conversion complete."
