% Karapanos, Nikolaos, et al. 
% "Sound-Proof: Usable Two-Factor Authentication Based on Ambient Sound."
% Simplified driver file to compute cross-correlation for audio files 
%   according to SPF scheme. See 'audioJob.m' in 'Schemes>audio' for original 
%   audioJob.m

%   Input args:
%   - filePath1 - Full path to the first FLAC audio file (string)
%   - filePath1 - Full path to the second FLAC audio file (string)
%   - expPath   - Full path to directory for reading/writing 

function newAudioJob(filePath1, filePath2, expPath)
    % Version of the script
    scriptVersion = 'v1.2.3';
    
    % Basic sampling frequency with which we are working
    Fs = 16000; % Change this if necessary
    
    % Load filter bank
    spfFilterBankFile = strcat(expPath, '/', 'spfFilterBank.mat');
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
    % Save results to JSON without storing the lag
    resultsFolder = fullfile(expPath, 'Results');
    if ~exist(resultsFolder, 'dir')
        mkdir(resultsFolder);
    end
    
    % Save cross-correlation result to sub-folder "Results" (which will be created if !exist)
    % If cross_correlation_result.json already exists (test 1), result 
    %   will be written to cross_correlation_result_2.json (test 2)
    resultFile = fullfile(resultsFolder, 'cross_correlation_result.json');
    if exist(resultFile, 'file') == 2
        fprintf('"%s" already exists, writing to "cross_correlation_result_2.json".\n', resultFile);
        result = struct('crossCorrelation', maxCorr, 'scriptVersion', scriptVersion);
        saveJsonFile(fullfile(resultsFolder, 'cross_correlation_result_2.json'), result);
    else
        result = struct('crossCorrelation', maxCorr, 'scriptVersion', scriptVersion);
        saveJsonFile(resultFile, result);
    end
    
    fprintf('Cross-correlation computation finished.\n');
    end