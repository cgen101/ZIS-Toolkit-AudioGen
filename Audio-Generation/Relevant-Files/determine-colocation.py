# Script which evaluates colocation of file pairs based on their similarity score

import os
import json

# Define the root path
rootPath = r'C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\Test-Dir-Fork\ZIS-toolkit-AudioGen\Audio-Generation\Relevant-Files\Results\\'

# Get all file names in the root path
fileNames = os.listdir(rootPath)

# Filter only JSON files if needed
fileNames = [fileName for fileName in fileNames if fileName.endswith('.json')]

# Construct full file paths
filePaths = [os.path.join(rootPath, fileName) for fileName in fileNames]

# Process each file
for filePath in filePaths:
    with open(filePath, 'r') as json_file:
        data = json.load(json_file)
        # Process data from each file as needed
        cross_correlation = data.get('crossCorrelation', 0.0)
        fileName1 = ''.join(data.get('file1', []))
        fileName2 = ''.join(data.get('file2', []))
        threshold = 0.03
        if cross_correlation >= threshold:
            print(f"The files '{fileName1}' and '{fileName2}' are colocated based on the cross-correlation value.")
        else:
            print(f"The files '{fileName1}' and '{fileName2}' are not colocated based on the cross-correlation value.")

for filePath in filePaths:
    os.remove(filePath)