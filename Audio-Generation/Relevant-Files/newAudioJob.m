function newAudioJob(filePath1, filePath2, expPath)
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
    
    % Save JSON to file
    resultFile = fullfile(resultsFolder, 'cross_correlation_result.json');
    if exist(resultFile, 'file') == 2
        fprintf('"%s" already exists, writing to "cross_correlation_result_2.json".\n', resultFile);
        saveJsonFile(fullfile(resultsFolder, 'cross_correlation_result_2.json'), result);
    else
        saveJsonFile(resultFile, result);
    end
    
    fprintf('Cross-correlation computation finished.\n');
end