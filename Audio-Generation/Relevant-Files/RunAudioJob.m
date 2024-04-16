
% Common root path-- CHANGE TO YOUR PATH HERE
rootPath = "C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\Test-Dir-Fork\ZIS-toolkit-AudioGen\Audio-Generation\";

% Path to directory containing files to read to/write from 
ioPath = fullfile(rootPath, "Relevant-Files");

% Relative paths for the audio files
filePath1 = fullfile(rootPath, "audio-files", "colocated_city.flac");
filePath2 = fullfile(rootPath, "audio-files", "colocated_city.flac");
filePath3 = fullfile(rootPath, "audio-files", "non_colocated_city.flac");
filePath4 = fullfile(rootPath, "audio-files", "non_colocated_highway_2.flac");

newAudioJob(filePath1, filePath2, ioPath);
newAudioJob(filePath3, filePath4, ioPath);