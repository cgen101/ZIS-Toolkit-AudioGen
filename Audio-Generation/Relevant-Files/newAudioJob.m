function newAudioJob(filePath1, filePath2, expPath)
% AUDIOJOB Main script used to generate results for: 
% Karapanos, Nikolaos, et al. 
% "Sound-Proof: Usable Two-Factor Authentication Based on Ambient Sound."
% USENIX Security Symposium. 2015.

%   Input args:
%   - filePath1 - Full path to the first FLAC audio file (string)
%   - filePath1 - Full path to the second FLAC audio file (string)
%    - expPath -  Full path to directory for i/o
    % Version of the script
    scriptVersion = 'v1.2.3';
    
    % Extract file names from file paths
    [~, name1, ext1] = fileparts(filePath1);
    [~, name2, ext2] = fileparts(filePath2);
    
    % Basic sampling frequency with which we are working
    Fs = 16000; % Change this if necessary
    
    % Load filter bank
    spfFilterBankFile = fullfile(expPath, 'spfFilterBank.mat');
    if exist(spfFilterBankFile, 'file') == 2
        fprintf('"%s" exists, loading it...\n', spfFilterBankFile);
        load(spfFilterBankFile);
    else
        fprintf('"%s" does not exist, precomputing...\n', spfFilterBankFile);
        spfFilterBank = preComputeFilterSPF();
        save(spfFilterBankFile, 'spfFilterBank');
    end

    % Load two audio signals
    S1 = loadSignal(filePath1, 'native');
    S2 = loadSignal(filePath2, 'native');
    
    % Compute maximum cross-correlation
    [maxCorr, ~] = maxCrossCorrelation(S1, S2);

    % Save results to JSON without storing the lag
    resultsFolder = fullfile(expPath, 'Results');
    if ~exist(resultsFolder, 'dir')
        mkdir(resultsFolder);
    end
    
% Create JSON structure with file names included
result = struct('file1', [name1 ext1], 'file2', [name2 ext2], 'crossCorrelation', maxCorr, 'scriptVersion', scriptVersion);

% Initialize a counter to add to the filename if it already exists
counter = 1;
while true
    % Generate the filename with or without the counter
    if counter == 1
        resultFile = fullfile(resultsFolder, 'cross_correlation_result_1.json');
    else
        resultFile = fullfile(resultsFolder, sprintf('cross_correlation_result_%d.json', counter));
    end
    
    % Check if the file already exists
    if exist(resultFile, 'file') == 2
        fprintf('"%s" already exists, trying the next filename.\n', resultFile);
        counter = counter + 1;  % Increment the counter
    else
        % Save JSON to file
        saveJsonFile(resultFile, result);
        fprintf('JSON saved to "%s".\n', resultFile);
        break;  % Exit the loop if the file is successfully saved
    end
end

fprintf('Cross-correlation computation finished.\n');
end