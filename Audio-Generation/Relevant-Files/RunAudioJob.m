% Script to run newAudioJob.m twice, once for colocated files and once for non-colocated 
%   files 

% Path to directory containing files to read to/write from 
ioPath = "C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\ZIS-toolkit\Audio-Generation\Relevant-Files";

% Path to first audio file for test 1
filePath1 = "C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\ZIS-toolkit\Audio-Generation\non_colocated_highway.flac";
% Path to second audio file for test 1
filePath2 = "C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\ZIS-toolkit\Audio-Generation\non_colocated_idle_2.flac";

% Path to first audio file for test 2
filePath3 = "C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\ZIS-toolkit\Audio-Generation\colocated_city.flac";
% Path to second audio file for test 2
filePath4 = "C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\ZIS-toolkit\Audio-Generation\colocated_city_2.flac";

newAudioJob(filePath1, filePath2, ioPath);

newAudioJob(filePath3, filePath4, ioPath);