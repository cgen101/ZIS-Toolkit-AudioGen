% Script to run newAudioJob on all pairs of files multiple times and 
% observe false rejection rates (FRR) and false acceptance rates (FAR)

% Common root path-- CHANGE TO YOUR PATH HERE
rootPath = "C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\Test-Dir-Fork\ZIS-toolkit-AudioGen\Audio-Generation\";
% Define the Python script file path
pythonScript = '"C:\Users\chlo\Documents\Spring 24\Security (CS4371)\Project\Test-Dir-Fork\ZIS-toolkit-AudioGen\Audio-Generation\generate_all.py"';
% Path to directory containing json results
resultPath = fullfile(rootPath, "Relevant-Files", "Results");

FAR = 0;
FRR = 0;
colocated = false;
% Main test loop
for i = 0:4
    system(['python ', pythonScript]);
    run(fullfile(rootPath, 'Relevant-Files', 'RunAudioJob.m'));
    fileNames = dir(fullfile(resultPath, '*.json'));
    % Process each file
    for j = 1:numel(fileNames)
        % Load and process JSON data
        filePath = fullfile(resultPath, fileNames(j).name);
        fid = fopen(filePath, 'r');
        rawData = fread(fid, inf, 'uint8=>char');
        fclose(fid);

        data = jsondecode(rawData');

        % Extract file names and extensions from JSON
        fileName1Array = data.file1; 
        fileName2Array = data.file2;
        cross_correlation = data.crossCorrelation;

        % Combine file name and extension
        fileName1 = strcat(fileName1Array{1}, fileName1Array{2});
        fileName2 = strcat(fileName2Array{1}, fileName2Array{2});

        fprintf("File Name 1: '%s'\n", fileName1);
        fprintf("File Name 2: '%s'\n", fileName2);

        threshold = 0.03;

        if cross_correlation >= threshold
            fprintf("The files '%s' and '%s' are colocated based on the cross-correlation value.\n", fileName1, fileName2);
            colocated = true;
        else
            fprintf("The files '%s' and '%s' are not colocated based on the cross-correlation value.\n", fileName1, fileName2);
            colocated = false;
        end

        if any(~contains(fileName1, 'non')) && ~colocated
            FRR = FRR + 1;
            fprintf("The files '%s' and '%s' resulted in false rejection.\n", fileName1, fileName2);
        end

        if any(contains(fileName1, 'non')) && colocated
            FAR = FAR + 1;
            fprintf("The files '%s' and '%s' resulted in false acceptance.\n", fileName1, fileName2);
        end
    end
    % Delete all files from the "Results" directory
    for k = 1:numel(fileNames)
       fileToDelete = fullfile(resultPath, fileNames(k).name);
        delete(fileToDelete);
    end
end

FRRrate = (FRR/15)*100; 
FARrate = (FAR/30)*100; 


fprintf("False rejection rate out of 15 tests: %.2f%%\n", FRRrate);
fprintf("False acceptance rate out of 30 tests: %.2f%%\n", FARrate);

audioFilesDir = fullfile(rootPath, "audio-files");

% Delete all files in the audio-files
delete(fullfile(audioFilesDir, '*.*'));



