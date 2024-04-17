
% Script to run newAudioJob on 2 pairs of files to demonstrate attempted pairing between
%   co-located and non-colocated devices 

% Common root path-- CHANGE TO YOUR PATH HERE
rootPath = "C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\Test-Dir-Fork\ZIS-toolkit-AudioGen\Audio-Generation\";

% Path to directory containing files to read to/write from 
ioPath = fullfile(rootPath, "Relevant-Files");

% Relative paths for the audio files
filePath1 = fullfile(rootPath, "audio-files", "colocated_highway_2.flac");
filePath2 = fullfile(rootPath, "audio-files", "colocated_highway.flac");
filePath3 = fullfile(rootPath, "audio-files", "non_colocated_idle_2.flac");
filePath4 = fullfile(rootPath, "audio-files", "non_colocated_idle.flac");

newAudioJob(filePath1, filePath2, ioPath);
newAudioJob(filePath3, filePath4, ioPath);