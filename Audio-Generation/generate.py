import numpy as np
import soundfile as sf
import os

def generate_audio(duration, fs, noise_levels):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    ambient_noise = sum([level * np.random.randn(len(t)) for level in noise_levels])
    ambient_noise /= np.max(np.abs(ambient_noise))
    return ambient_noise

def generate_audio_const(duration, fs, amplitude, frequency):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
    sine_wave /= np.max(np.abs(sine_wave))
    return sine_wave

def save_audio(audio_data, output_file, fs):
    sf.write(output_file, audio_data, fs)

def save_audio_to_dir(audio_data, output_file, fs, output_dir):
    output_path = os.path.join(output_dir, output_file)
    save_audio(audio_data, output_path, fs)

def get_user_choice():
    while True:
        print("Choose which files to generate:")
        print("1. Non-colocated")
        print("2. Colocated")
        choice = input("Enter your choice (1/2): ")

        if choice in ['1', '2']:
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    if choice == '1':
        duration = int(input("Enter sample duration (in seconds): "))
        car_state_1 = input("Enter car state for the first file (city/highway/idle): ").lower()
        file_name_1 = f"non_colocated_{car_state_1}.flac"

        return file_name_1, duration

    elif choice == '2':
        duration = int(input("Enter sample duration (in seconds): "))
        car_state_1 = input("Enter car state for the colocated file (city/highway/idle): ").lower()
        file_name_1 = f"colocated_{car_state_1}.flac"

        return file_name_1, duration

# Get user input for audio generation
file_name_1, duration = get_user_choice()

# Define parameters
fs = 16000  # Sampling frequency (16 kHz)

# Generate time vector
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Generate car engine noise based on user's choice
if "non_colocated" in file_name_1:
    car_state_1 = file_name_1.split("_")[2].split(".")[0]
    if car_state_1 == "city":
        car_noise_level_1 = np.random.uniform(0.4, 0.8)
        radio_noise_level_1 = np.random.uniform(0.2, 0.6)
        road_noise_level_1 = np.random.uniform(0.3, 0.7)
    elif car_state_1 == "highway":
        car_noise_level_1 = np.random.uniform(0.5, 0.9)
        radio_noise_level_1 = np.random.uniform(0.1, 0.5)
        road_noise_level_1 = np.random.uniform(0.2, 0.6)
    elif car_state_1 == "idle":
        car_noise_level_1 = np.random.uniform(0.2, 0.5)
        radio_noise_level_1 = np.random.uniform(0.1, 0.3)
        road_noise_level_1 = np.random.uniform(0.1, 0.3)
else:  # Colocated
    car_state_1 = file_name_1.split("_")[1].split(".")[0]
    if car_state_1 == "city":
        car_noise_level_1 = 0.6
        radio_noise_level_1 = 0.4
        road_noise_level_1 = 0.5
    elif car_state_1 == "highway":
        car_noise_level_1 = 0.8
        radio_noise_level_1 = 0.3
        road_noise_level_1 = 0.6
    elif car_state_1 == "idle":
        car_noise_level_1 = 0.4
        radio_noise_level_1 = 0.2
        road_noise_level_1 = 0.3

# Generate car engine noise
car_engine_noise_1 = car_noise_level_1 * np.random.randn(len(t))

# Generate radio noise
radio_noise_1 = radio_noise_level_1 * np.random.randn(len(t))

# Generate road noise
road_noise_1 = road_noise_level_1 * np.random.randn(len(t))

# Combine all noises
ambient_noise_1 = car_engine_noise_1 + radio_noise_1 + road_noise_1

# Normalize the audio
ambient_noise_1 /= np.max(np.abs(ambient_noise_1))

# Save the first audio to a .wav file in the "audio-files" directory
output_dir = "audio-files"
output_file_1 = os.path.join(output_dir, file_name_1)
save_audio((ambient_noise_1 * 32767).astype(np.int16), output_file_1, fs)

print(f"First ambient audio saved to {output_file_1}")

# Generate the second audio based on the same user choice
if "non_colocated" in file_name_1:
    car_state_2 = input("Enter car state for the second file (city/highway/idle): ").lower()
    file_name_2 = f"non_colocated_{car_state_2}_2.flac"
else:
    car_state_2 = car_state_1
    file_name_2 = f"colocated_{car_state_2}_2.flac"

# Generate car engine noise based on user's choice
if "non_colocated" in file_name_2:
    if car_state_2 == "city":
        car_noise_level_2 = np.random.uniform(0.4, 0.8)
        radio_noise_level_2 = np.random.uniform(0.2, 0.6)
        road_noise_level_2 = np.random.uniform(0.3, 0.7)
    elif car_state_2 == "highway":
        car_noise_level_2 = np.random.uniform(0.5, 0.9)
        radio_noise_level_2 = np.random.uniform(0.1, 0.5)
        road_noise_level_2 = np.random.uniform(0.2, 0.6)
    elif car_state_2 == "idle":
        car_noise_level_2 = np.random.uniform(0.2, 0.5)
        radio_noise_level_2 = np.random.uniform(0.1, 0.3)
        road_noise_level_2 = np.random.uniform(0.1, 0.3)
else:  # Colocated
    if car_state_2 == "city":
        car_noise_level_2 = 0.6
        radio_noise_level_2 = 0.4
        road_noise_level_2 = 0.5
    elif car_state_2 == "highway":
        car_noise_level_2 = 0.8
        radio_noise_level_2 = 0.3
        road_noise_level_2 = 0.6
    elif car_state_2 == "idle":
        car_noise_level_2 = 0.4
        radio_noise_level_2 = 0.2
        road_noise_level_2 = 0.3
# Generate car engine noise
car_engine_noise_2 = car_noise_level_2 * np.random.randn(len(t))

# Generate radio noise
radio_noise_2 = radio_noise_level_2 * np.random.randn(len(t))

# Generate road noise
road_noise_2 = road_noise_level_2 * np.random.randn(len(t))

# Combine all noises
ambient_noise_2 = car_engine_noise_2 + radio_noise_2 + road_noise_2

# Normalize the audio
ambient_noise_2 /= np.max(np.abs(ambient_noise_2))

# Save the second audio to a .wav file in the "audio-files" directory
output_file_2 = os.path.join(output_dir, file_name_2)
save_audio((ambient_noise_2 * 32767).astype(np.int16), output_file_2, fs)

print(f"Second ambient audio saved to {output_file_2}")