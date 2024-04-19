# Implementation of audio generation and simulating tool

This folder contains implimentation of an audio generation toolkit, which generates ambient audio clips for the Car scenario. The toolkit additionally calculates the similarity score between 2 generated audio files, then simulates pairings between devices based on the similarity score. There is a testing script provided which examines error rates.

This feature was built for the following ZIS scheme:
* *SoundProof (SPF)*  [4]

This feature builds on the paper "Perils of Zero-Interaction Security in the Internet of Things", by Mikhail Fomichev, Max Maass, Lars Almon, Alejandro Molina, Matthias Hollick, in Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, vol. 3, Issue 1, 2019. 

### A paper that "Perils of Zero-Interaction Security in the Internet of Things" references:
[1] N. Karapanos, C. Marforio, and C. Soriente, “Sound-Proof: Usable Two-Factor Authentication Based on Ambient Sound.” Accessed: Apr. 18, 2024. [Online]. Available: https://arxiv.org/pdf/1503.03790.pdf

### A paper that references "Perils of Zero-Interaction Security in the Internet of Things"
[2] M. Conti and C. Lal, “Context-based Co-presence detection techniques: A survey,” Computers & Security, vol. 88, p. 101652, Jan. 2020, doi: https://doi.org/10.1016/j.cose.2019.101652.

This paper builds on the insights provided by "Perils of Zero-Interaction Security in the Internet of Things" by offering a comprehensive survey and analysis of contextual-based proximity detection techniques in ZICDA systems. It extends the understanding of security challenges, adversary models, and existing attacks, providing valuable context for evaluating the schemes discussed in the original paper:


## File Structure

### Audio-Generation:

#### Relevant-Files:

This directory contains the implementation files for SoundProof (SPF) [4] and the script to simulate a pairing.

##### Altered files to do specific work for SoundProof (SPF) [4]
* *newAudioJob.m* - **a main function** altered main function to include only relevant work for SoundProof (SPF) [4].
* *RunAudioJob.m* - a script to run newAudioJob.m for all pairs of files (colocated and non-colocated files), to demonstrate a pairing attempts between all audio files in the Car scenario.
* *RunAudioJob-manual.m* - a script to run newAudioJob.m twice  with 2 pairs of files (colocated and non-colocated), to demonstrate a pairing attempts between a colocated and non-colocated device in the Car scenario.
* *RunTest.m* - a script to run newAudioJob.m for all pairs of files (colocated and non-colocated files) a specified amount of times and observe error rates
* *determine-colocation.py* - a script to simulate pairing between devices based on their similarity score. 

##### Unaltered files copied from Schemes > audio
* *alignTwoSignals.m* - a function to align two discrete (audio) signals.
* *computeSPF.m* - a wrapper to compute the SPF feature and store the results.
* *loadSignal.m* - a function to load two audio signals from audio files (e.g., *.FLAC); the sampling rate in Hz is set inside the function.
* *maxCrossCorrelation.m* - compute maximum cross-correlation between two normalized discrete (audio) signals.
* *normalizeSignal.m* - energy normalization of a discrete (audio) signal.
* *preComputeFilterSPF.m* - precompute the SPF filter bank (produces the spfFilterBank.mat file).
* *saveJsonFile.m* - store the results of audio feature computations in a JSON file.
* *soundProofXcorr.m* - implementation of the SPF feature.
* *thirdOctaveSplitter.m* - split an audio signal into 1/3 octave bands using the spfFilterBank.mat filter bank.
* *xcorrDelay.m* - compute a delay between two discrete (audio) signals using MATLAB's xcorr function.
* *spfFilterBank.mat* - a filter bank necessary for computing the SPF feature (regenerated if is not present in the folder). 

#### generate.py: A script to generate 2 ambient audio files for the Car scenario based on user input
#### generate_all.py: A script to generate all possible audio file pairs (12 total) for demo and testing 


## How to use Audio Genration tool step-by-step: 

### 1. Clone from https://github.com/cgen101/ZIS-Toolkit-AudioGen

### 2. Ensure you have required installations: 
* *Python 3.12.0*
* *numpy version 1.26.4*
* *soundfile 0.12.1*
* *MATLAB Version: 24.1.0.2537033 (R2024a)*
* *Signal Processing Toolbox (Version 24.1)*

### 3. Navigate to Audio-Generation directory and either run *python generate.py*  or run *python generate_all.py* for all possible pairs.
* Follow prompts in terminal to generate audio files
* Each run of *python generate.py* will generate a pair of audio files for pairing simulation
* Each run of *python generate_all.py* will generate all pairs of audio files for pairing simulation
* The .flac files will be written into a sub-directory, 'audio-files', in 'Audio-Generation' with relevant names 
* Keep in mind, each generation of non-colocated files will give slightly different results, as the non-colocated files have an element of randomness in their generation. 

### 4. Change relevant filepaths in RunAudioJob/RunAudioJob_manual/RunTest- root and specific filenames
* *filePath1* should be path to first audio file for pairing 1
* *filePath2* should be path to second audio file for pairing 1
* *filePath3* should be path to first audio file for pairing 2
* *filePath4* should be path to second audio file for pairing 2
* Add as many pairs as you would like to test to filePaths.
* You may test as many pairings as you wish, but keep in mind there must be an even number of files to 
pair .

### 5. Open MATLAB, create a new project from directory 'Audio-Generation'
* Make sure to add Audio-Generation directory with subfolders to project path 
* Set Relevant-Files as your current folder 

### 6. Run 'RunAudioJob' or 'RunAudioJob_manual' or 'RunTest'
* RunAudioJob and RunAudioJob_manual will create a subfolder in 'Relevant-Files' called *'Results'*
* RunAudioJob is for testing all pairings, RunAudioJob_manual is for testing only 2 pairings.
* RunTest is an automated testing script which uses generate_all.py and RunAudioJob.m to test multiple audio generation events, determine similarity scores between pairs, and examine error rates. 
* *'Results'* will contain json files with cross-correlation results for test pairings for test 1-n upon completion, numbered 1-n.

### 7. Navigate to Relevant-Files and run determine-colocation.py if not auto-testing
* To run pairings, change rootPath to your path to 'Results' then run *python determine-colocation.py*
* Make sure to edit rootPath and fileNames to reflect your specific testing case.



