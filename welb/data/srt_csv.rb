require 'csv'

stage_recording_files = Organization.find(378).stages.map { |s| s.stage_recording_files.first }.compact

# Create a new CSV object
csv = CSV.new(STDOUT)

# Write the header row to STDOUT
csv << ["org_id", "stage_id", "stage_recording_file_id", "recording_name", "srt_url", "created_at"]

# Iterate over the stage_recording_files
stage_recording_files.each do |stage_recording_file|
  # Write a row for each file to STDOUT
  csv << [stage_recording_file.stage.organization_id, stage_recording_file.stage_id, stage_recording_file.id, stage_recording_file.name, stage_recording_file.srt_url, stage_recording_file.created_at]
end

# Close the CSV object
csv.close
