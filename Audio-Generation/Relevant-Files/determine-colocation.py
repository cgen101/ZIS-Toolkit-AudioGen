# Script to determine if 2 audio files are co-located based on the max
#   cross-correlation score.   

import json
# Define the root path-- CHANGE TO YOUR PATH HERE
rootPath = r'C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\Test-Dir-Fork\ZIS-toolkit-AudioGen\Audio-Generation\Relevant-Files\Results\\'

# List of file names (excluding root path)
fileNames = [
    'cross_correlation_result_1.json',
    'cross_correlation_result_2.json',
    'cross_correlation_result_3.json',
    'cross_correlation_result_4.json',
    'cross_correlation_result_5.json',
    'cross_correlation_result_6.json',
    'cross_correlation_result_7.json',
    'cross_correlation_result_8.json',
    'cross_correlation_result_9.json',
]

# Construct full file paths
filePaths = [rootPath + fileName for fileName in fileNames]

# Process each file
for filePath in filePaths:
    with open(filePath, 'r') as json_file:
        data = json.load(json_file)
        # Process data from each file as needed
        cross_correlation = data.get('crossCorrelation', 0.0)
        fileName1 = ''.join(data.get('file1', []))
        fileName2 = ''.join(data.get('file2', []))
        threshold = 0.07
        if cross_correlation >= threshold:
            print(f"The files '{fileName1}' and '{fileName2}' are colocated based on the cross-correlation value.")
        else:
            print(f"The files '{fileName1}' and '{fileName2}' are not colocated based on the cross-correlation value.")