#!/bin/bash

transcripts_dir='./data/org_378_transcripts'

# Calculate the total number of words across all files
total_words=$(find $transcripts_dir/*.srt -type f -print0 | xargs -0 cat | wc -w)

# Calculate the number of files
number_of_files=$(find $transcripts_dir/*.srt -type f | wc -l)

# Calculate the average number of words per file
average_words_per_file=$(echo "scale=2; $total_words / $number_of_files" | bc)

# Output the result
echo "Average words per file: $average_words_per_file"

total_size=$(find "$transcripts_dir" -type f -print0 | xargs -0 ls -l | awk '{sum+=$5} END {print sum}')
number_of_files=$(find "$transcripts_dir" -type f | wc -l)
average_size=$(echo "scale=2; $total_size / $number_of_files" | bc)
echo "Average file size: $average_size bytes"
