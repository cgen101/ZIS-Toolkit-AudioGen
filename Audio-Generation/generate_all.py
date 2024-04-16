import os
import itertools
import numpy as np
import soundfile as sf

def generate_audio(duration, fs, noise_levels):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    ambient_noise = sum([level * np.random.randn(len(t)) for level in noise_levels])
    ambient_noise /= np.max(np.abs(ambient_noise))
    return ambient_noise

def save_audio(audio_data, output_file, fs, output_dir):
    output_path = os.path.join(output_dir, output_file)
    sf.write(output_path, audio_data, fs)

def generate_pairs(duration, fs, noise_levels, output_dir):
    car_states = ['city', 'highway', 'idle']
    colocated_permutations = list(itertools.permutations(car_states, 2))
    non_colocated_permutations = list(itertools.permutations(car_states, 2))

    for car_state_1, car_state_2 in colocated_permutations:
        for colocated in [True, False]:
            file_name_1 = f"{'non_colocated' if not colocated else 'colocated'}_{car_state_1}.flac"
            file_name_2 = f"{'non_colocated' if not colocated else 'colocated'}_{car_state_2}_2.flac"

            t = np.linspace(0, duration, int(fs * duration), endpoint=False)
            car_noise_level_1, radio_noise_level_1, road_noise_level_1 = get_noise_levels(car_state_1)
            car_noise_level_2, radio_noise_level_2, road_noise_level_2 = get_noise_levels(car_state_2)

            car_engine_noise_1 = car_noise_level_1 * np.random.randn(len(t))
            radio_noise_1 = radio_noise_level_1 * np.random.randn(len(t))
            road_noise_1 = road_noise_level_1 * np.random.randn(len(t))
            ambient_noise_1 = car_engine_noise_1 + radio_noise_1 + road_noise_1
            ambient_noise_1 /= np.max(np.abs(ambient_noise_1))

            car_engine_noise_2 = car_noise_level_2 * np.random.randn(len(t))
            radio_noise_2 = radio_noise_level_2 * np.random.randn(len(t))
            road_noise_2 = road_noise_level_2 * np.random.randn(len(t))
            ambient_noise_2 = car_engine_noise_2 + radio_noise_2 + road_noise_2
            ambient_noise_2 /= np.max(np.abs(ambient_noise_2))

            save_audio((ambient_noise_1 * 32767).astype(np.int16), file_name_1, fs, output_dir)
            save_audio((ambient_noise_2 * 32767).astype(np.int16), file_name_2, fs, output_dir)

            print(f"Pair {file_name_1} and {file_name_2} generated.")

def get_noise_levels(car_state):
    if car_state == "city":
        return np.random.uniform(0.4, 0.8), np.random.uniform(0.2, 0.6), np.random.uniform(0.3, 0.7)
    elif car_state == "highway":
        return np.random.uniform(0.5, 0.9), np.random.uniform(0.1, 0.5), np.random.uniform(0.2, 0.6)
    elif car_state == "idle":
        return np.random.uniform(0.2, 0.5), np.random.uniform(0.1, 0.3), np.random.uniform(0.1, 0.3)

# Define parameters
duration = int(input("Enter sample duration (in seconds): "))
fs = 16000  # Sampling frequency (16 kHz)
noise_levels = [0.6, 0.4, 0.5]  # Initial noise levels for colocated files
output_dir = "audio-files"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Generate pairs of colocated and non-colocated audio files in the output directory
generate_pairs(duration, fs, noise_levels, output_dir)