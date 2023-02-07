require 'csv'
require 'open-uri'

# Create the directory to store the transcripts
Dir.mkdir("org_243_transcripts") unless Dir.exist?("org_243_transcripts")


def snake_case_string(str)
  # remove special characters
  stripped_str = str.gsub(/[^0-9a-z ]/i, '')
  # convert to snake case
  stripped_str.strip.downcase.gsub(' ', '_')
end

# Parse the CSV data from file
CSV.foreach("org_243_transcript_index.csv", headers: true) do |row|
  # Get the data for each file
  org_id = row["org_id"]
  stage_id = row["stage_id"]
  recording_name = row["recording_name"]
  srt_url = row["srt_url"]
  created_at = row["created_at"]

	next if srt_url == ""

  # Skip the file if it doesn't belong to org_378
  next unless org_id == "243"

  # Download the file to the transcripts directory
  File.open("org_243_transcripts/#{stage_id}_#{snake_case_string(recording_name)}.srt", "wb") do |file|
    file.write(open(srt_url).read)
  end
end