# Script to determine if 2 audio files are co-located based on the max
#   cross-correlation score.   

import json

# Load JSON data from the file
# CHANGE FILEPATH HERE
filePath = r'C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\ZIS-toolkit\Audio-Generation\Relevant-Files\Results\cross_correlation_result.json'
with open(filePath, 'r') as json_file:
    data = json.load(json_file)

# Extract cross-correlation value from the JSON data
cross_correlation = data.get('crossCorrelation', 0.0)  # Default to 0.0 if key not found

# Define the threshold for colocation (you can adjust this threshold as needed)
threshold = 0.011 # Example threshold value

# Determine colocation status based on the threshold
if cross_correlation >= threshold:
    print("The devices are colocated based on the cross-correlation value.")
else:
    print("The devices are not colocated based on the cross-correlation value.")