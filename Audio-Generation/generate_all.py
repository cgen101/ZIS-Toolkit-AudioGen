import os
import numpy as np
import soundfile as sf

def generate_audio_rand(duration, fs, noise_levels):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    ambient_noise = sum([level * np.random.randn(len(t)) for level in noise_levels])
    ambient_noise /= np.max(np.abs(ambient_noise))
    return ambient_noise

def generate_audio(duration, fs, amplitude, frequency):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
    sine_wave /= np.max(np.abs(sine_wave))
    return sine_wave

def save_audio(audio_data, output_file, fs, output_dir):
    output_path = os.path.join(output_dir, output_file)
    sf.write(output_path, audio_data, fs)

def generate_colocated_pairs(duration, fs, output_dir):
    car_states = ['city', 'highway', 'idle']
    for car_state in car_states:
        file_name_1 = f"{'colocated'}_{car_state}.flac"
        file_name_2 = f"{'colocated'}_{car_state}_2.flac"

        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        amplitude = 0.5  # Adjust the amplitude as needed

        # Define frequencies based on the car state
        if car_state == "city":
            frequency_car = 500
            frequency_radio = 800
            frequency_road = 1200
        elif car_state == "highway":
            frequency_car = 700
            frequency_radio = 1000
            frequency_road = 1500
        elif car_state == "idle":
            frequency_car = 400
            frequency_radio = 600
            frequency_road = 900

        # Generate consistent sine wave for car engine noise
        car_engine_noise_1 = generate_audio(duration, fs, amplitude, frequency_car)
        radio_noise_1 = generate_audio(duration, fs, amplitude, frequency_radio)
        road_noise_1 = generate_audio(duration, fs, amplitude, frequency_road)

        # Normalize the audio
        car_engine_noise_1 /= np.max(np.abs(car_engine_noise_1))
        radio_noise_1 /= np.max(np.abs(radio_noise_1))
        road_noise_1 /= np.max(np.abs(road_noise_1))

        # Save the audio files
        save_audio((car_engine_noise_1 * 32767).astype(np.int16), file_name_1, fs, output_dir)
        save_audio((radio_noise_1 * 32767).astype(np.int16), file_name_2, fs, output_dir)
        print(f"Pair {file_name_1} and {file_name_2} generated.")

def generate_non_colocated_pairs(duration, fs, output_dir):
    car_states = ['city', 'highway', 'idle']
    for car_state in car_states: 
        file_name_1 = f"{'non_colocated'}_{car_state}.flac"
        file_name_2 = f"{'non_colocated'}_{car_state}_2.flac"

        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        if car_state == "city":
            car_noise_level_1 = np.random.uniform(0.4, 0.8)
            radio_noise_level_1 = np.random.uniform(0.2, 0.6)
            road_noise_level_1 = np.random.uniform(0.3, 0.7)
            car_noise_level_2 = np.random.uniform(0.4, 0.8)
            radio_noise_level_2 = np.random.uniform(0.2, 0.6)
            road_noise_level_2 = np.random.uniform(0.3, 0.7)
        elif car_state == "highway":
            car_noise_level_1 = np.random.uniform(0.5, 0.9)
            radio_noise_level_1 = np.random.uniform(0.1, 0.5)
            road_noise_level_1 = np.random.uniform(0.2, 0.6)
            car_noise_level_2 = np.random.uniform(0.5, 0.9)
            radio_noise_level_2 = np.random.uniform(0.1, 0.5)
            road_noise_level_2 = np.random.uniform(0.2, 0.6)
        elif car_state == "idle":
            car_noise_level_1 = np.random.uniform(0.2, 0.5)
            radio_noise_level_1 = np.random.uniform(0.1, 0.3)
            road_noise_level_1 = np.random.uniform(0.1, 0.3)
            car_noise_level_2 = np.random.uniform(0.2, 0.5)
            radio_noise_level_2 = np.random.uniform(0.1, 0.3)
            road_noise_level_2 = np.random.uniform(0.1, 0.3)

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


# Define parameters
duration = int(input("Enter sample duration (in seconds): "))
fs = 16000  # Sampling frequency (16 kHz)
output_dir = "audio-files"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Generate pairs of colocated and non-colocated audio files in the output directory
generate_colocated_pairs(duration, fs, output_dir)
generate_non_colocated_pairs(duration, fs, output_dir)

