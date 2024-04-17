% Script to run newAudioJob on 2 pairs of files to demonstrate attempted pairing between
% co-located and non-colocated devices

% Common root path-- CHANGE TO YOUR PATH HERE
rootPath = "C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\Test-Dir-Fork\ZIS-toolkit-AudioGen\Audio-Generation\";

% Path to directory containing files to read to/write from
ioPath = fullfile(rootPath, "Relevant-Files");

% Relative paths for the audio files
%ADD MORE FILEPATHS HERE FOR ADDITIONAL PAIRINGS
filePaths = {fullfile(rootPath, "audio-files", "colocated_highway_2.flac"), ...
             fullfile(rootPath, "audio-files", "colocated_highway.flac"), ...
             fullfile(rootPath, "audio-files", "non_colocated_highway_2.flac"), ...
             fullfile(rootPath, "audio-files", "non_colocated_highway.flac")};

% Loop through pairs of file paths and run newAudioJob for each pair
for i = 1:2:length(filePaths)
    filePath1 = filePaths{i};
    filePath2 = filePaths{i+1};
    newAudioJob(filePath1, filePath2, ioPath);
end