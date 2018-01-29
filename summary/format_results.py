from json import dumps, loads
from glob import glob
import re
import sys
import numpy as np
import os

# Number of sensors to compare each sensor with
NUM_SENSORS = 0

# Sensor mapping: car experiment
SENSORS_CAR1 = ['01', '02', '03', '04', '05', '06']
SENSORS_CAR2 = ['07', '08', '09', '10', '11', '12']

# Sensor mapping: office experiment
SENSORS_OFFICE1 = ['01', '02', '03', '04', '05', '06', '07', '08']
SENSORS_OFFICE2 = ['09', '10', '11', '12', '13', '14', '15', '16']
SENSORS_OFFICE3 = ['17', '18', '19', '20', '21', '22', '23', '24']

# List of sensor mappings
SENSORS = []

# Root path - points to the result folder of structure:
# /Sensor-xx/audio/<audio_features>/<time_intervals>
ROOT_PATH = ''

# Root path - points to the power folder of structure:
# /Sensor-xx/audio/soundProofXcorr/<time_intervals>/Power.json
POWER_PATH = ''

# Summary file name
SUMMARY_FILE = 'Summary.json'


def align_summary(path):
    # Iterate over matched files
    for json_file in glob(path, recursive=True):
        print('parsed file: ' + json_file)

        # Get target sensor number, e.g. 01, 02, etc.
        # (take different slashes into account: / or \)
        match = re.search(r'(?:/|\\)Sensor-(.*)(?:/|\\)audio(?:/|\\)', json_file)

        # If there is no match - exit
        if not match:
            print('align_summary: no match for the sensor field, exiting...')
            sys.exit(0)

        # Construct target sensor string, e.g. Sensor-01, Sensor-02, etc.
        target_sensor = 'Sensor-' + match.group(1)

        # Open and read the JSON file
        with open(json_file, 'r') as f:
            json = loads(f.read())
            results = json['results']
            # Count the number of results
            res_len = len(results)

        # Check if the results are complete
        if res_len < NUM_SENSORS:
            # Get the number of sensor fields to be added
            res_count = NUM_SENSORS-res_len

            # Iterate over missing sensors
            for i in range(1, res_count + 1):
                # Make it 01, 02, etc.
                if i < 10:
                    insert_sensor = 'Sensor-' + '0' + str(i)
                else:
                    insert_sensor = 'Sensor-' + str(i)

                # Path of file to be parsed (take different slashes into account: / or \)
                sym_path = re.sub(r'Sensor-(.*)(?:/|\\)audio(?:/|\\)', insert_sensor + '/audio/', json_file)

                print('sym file: %s ---- with field: %s' % (sym_path, target_sensor.lower()))

                # Open and read JSON file
                with open(sym_path, 'r') as f:
                    sym_json = loads(f.read())
                    # Get the field to be symmetrically added to json_file
                    sym_field = sym_json['results'][target_sensor.lower()]

                # Add sym_field to results
                json['results'][insert_sensor.lower()] = sym_field

            # Save the updated json file
            with open(json_file, 'w') as f:
                f.write(dumps(json, indent=4, sort_keys=True))


def add_last_summary(path, feature):
    # Iterate over matched files
    for json_file in glob(path, recursive=True):

        print('parsed file: ' + json_file)

        # Get the current folder, e.g. 10sec, 1min, etc.
        # (take different slashes into account: / or \)
        regex = re.escape(feature) + r'(?:/|\\)(.*)(?:/|\\)'
        match = re.search(regex, json_file)

        # If there is no match - exit
        if not match:
            print('add_last_summary: no match for the folder name, exiting...')
            sys.exit(0)

        cur_folder = match.group(1)

        # Get target sensor number - the last one Sensor-12(car) or Sensor-24(office)
        # (take different slashes into account: / or \)
        match = re.search(r'(?:/|\\)Sensor-(.*)(?:/|\\)audio(?:/|\\)', json_file)

        # If there is no match - exit /
        if not match:
            print('add_last_summary: no match for the sensor field, exiting...')
            sys.exit(0)

        # Construct target sensor string, e.g. Sensor-12(car) or Sensor-24(office)
        target_num = match.group(1)
        target_sensor = 'Sensor-' + target_num

        # Dictionary to store result fields
        json_dict = {}

        # Iterate over all sensors
        for i in range(1, NUM_SENSORS + 1):
            # Make it 01, 02, etc.
            if i < 10:
                insert_sensor = 'Sensor-' + '0' + str(i)
            else:
                insert_sensor = 'Sensor-' + str(i)

            # Path of file to be parsed (take different slashes into account: / or \)
            sym_path = re.sub(r'Sensor-(.*)(?:/|\\)audio(?:/|\\)', insert_sensor + '/audio/', json_file) \
            + SUMMARY_FILE

            print('sym file: %s ---- with field: %s' % (sym_path, target_sensor.lower()))

            # Open and read JSON file
            with open(sym_path, 'r') as f:
                sym_json = loads(f.read())
                # Get the field to be symmetrically added to json_file
                sym_field = sym_json['results'][target_sensor.lower()]

            # Add sym_field to results
            json_dict[insert_sensor.lower()] = sym_field

        # Result that goes into JSON (name stolen from Max;))
        rv = {}

        # Metadata dict
        meta_dict = {}

        # Metadata fields: target sensor, feature, duration and value
        meta_dict['sensor'] = target_num
        meta_dict['feature'] = feature
        meta_dict['duration'] = cur_folder

        if feature == 'audioFingerprint' or feature == 'noiseFingerprint':
            meta_dict['value'] = 'fingerprints_similarity_percent'
        elif feature == 'soundProofXcorr':
            meta_dict['value'] = 'max_xcorr'
        elif feature == 'timeFreqDistance':
            meta_dict['value'] = 'max_xcorr, time_freq_dist'

        # Add metadata
        rv['metadata'] = meta_dict

        # Add results
        rv['results'] = json_dict

        filename = json_file + SUMMARY_FILE
        print('Saving a file: %s' % filename)
        # Save the new JSON file
        with open(filename, 'w') as f:
            f.write(dumps(rv, indent=4, sort_keys=True))


# ToDo: add parallelization to this function
def add_spf_power(data_path, power_path):
    # Iterate over matched files
    for json_file in glob(data_path, recursive=True):
        print('parsed file: %s' % json_file)

        # Get the match
        match = re.search(r'^(.*)(?:/|\\)Sensor-(.*)(?:/|\\)audio', json_file)

        # If there is no match - exit
        if not match:
            print('add_spf_power: no match for the root folder, exiting...')
            sys.exit(0)

        res = json_file.split(match.group(1))

        if not res[0] and res[1]:
            power_path = power_path + res[1]
        else:
            print('add_spf_power: split of root folder failed: %s --- exiting...' % match.group(1))
            sys.exit(0)

        # Open and read data JSON file
        with open(json_file, 'r') as f:
            json_data = loads(f.read())
            data_res = json_data['results']
            metadata = json_data['metadata']
            # Count the number of results
            res_data_len = len(data_res)
            print(res_data_len)

        # Open and read power JSON file
        with open(power_path, 'r') as f:
            json_power = loads(f.read())
            power_res = json_power['results']
            # Count the number of results
            res_power_len = len(power_res)
            print(res_power_len)

        if res_data_len != res_power_len:
            print('add_spf_power: length mismatch between %s and %s --- exiting...' % (json_file, power_path))
            sys.exit(0)

        # List to store power values
        power_list = []

        # Store power values in the power list
        for k, v in power_res.items():
            power_list.append(v)

        # Index to iterate over the power_list
        idx = 0

        # Iterate over the data_res dictionary and add power values from power_list to data_res (sigh!)
        for k, v in data_res.items():
            for k1, v1 in power_list[idx].items():
                # data_res[k][k1] = v1
                v[k1] = v1
            idx += 1

        # Result that goes into JSON (name stolen from Max;))
        rv = {}

        # Add metadata
        rv['metadata'] = metadata

        # Add results
        rv['results'] = data_res

        # Save the result back to json_file
        with open(json_file, 'w') as f:
            f.write(dumps(rv, indent=4, sort_keys=True))

# Todo: split to individual functions, e.g. wrap_up_afp(), etc.
def wrap_up_results(path, feature):
    # Iterate over matched files
    for json_file in glob(path, recursive=True):

        print('parsed files: %s' % json_file)

        co_located_list = []
        non_colocated_list = []

        # Open and read JSON file
        with open(json_file, 'r') as f:
            json = loads(f.read())
            results = json['results']
            metadata = json['metadata']

        # Get the target sensor
        target_sensor = metadata['sensor']

        # Todo: adjust the check using SENSORS list
        # Get co-located and non-colocated lists of sensor numbers
        if target_sensor in SENSORS_CAR1:
            co_located_list = list(SENSORS_CAR1)
            co_located_list.remove(target_sensor)
            non_colocated_list = list(SENSORS_CAR2)
        else:
            co_located_list = list(SENSORS_CAR2)
            co_located_list.remove(target_sensor)
            non_colocated_list = list(SENSORS_CAR1)

        # Lists of co-located and non-colocated values
        co_located_val = []
        non_colocated_val = []

        # Accumulate co-located and non-colocated values
        for k, v in results.items():
            # Get the sensor number, e.g. 01, 02, etc.
            sensor_num = k.split('-')[1]

            if sensor_num in co_located_list:
                co_located_val.append(v)
            else:
                non_colocated_val.append(v)

        # Dictionaries of co-located and non-colocated results
        co_located_dict = {}
        non_colocated_dict = {}

        if feature == 'audioFingerprint' or feature == 'soundProofXcorr':
            # Lists for max, min, mean (co-located and non-colocated)
            co_located_max_list = []
            co_located_min_list = []
            co_located_mean_list = []

            non_colocated_max_list = []
            non_colocated_min_list = []
            non_colocated_mean_list = []

            # Threshold percent for SPF
            if feature == 'soundProofXcorr':
                co_located_th_list = []
                non_colocated_th_list = []

            # Get co-located values
            for val in co_located_val:
                co_located_max_list.append(val['max'])
                co_located_min_list.append(val['min'])
                co_located_mean_list.append(val['mean'])
                if feature == 'soundProofXcorr':
                    co_located_th_list.append(val['threshold_percent'])

            # Get non-colocated values
            for val in non_colocated_val:
                non_colocated_max_list.append(val['max'])
                non_colocated_min_list.append(val['min'])
                non_colocated_mean_list.append(val['mean'])
                if feature == 'soundProofXcorr':
                    non_colocated_th_list.append(val['threshold_percent'])

            # Convert co-located and non-colocated mean lists to np arrays
            co_located_mean_array = np.array(list(co_located_mean_list), dtype=float)
            non_colocated_mean_array = np.array(list(non_colocated_mean_list), dtype=float)

            # Compute mean_mean, median_mean, std_mean, min_min, max_max, for co-located array
            co_located_dict['mean_mean'] = np.mean(co_located_mean_array)
            co_located_dict['median_mean'] = np.median(co_located_mean_array)
            co_located_dict['std_mean'] = np.std(co_located_mean_array)
            co_located_dict['min_min'] = np.amin(np.array(list(co_located_min_list), dtype=float))
            co_located_dict['max_max'] = np.amax(np.array(list(co_located_max_list), dtype=float))
            if feature == 'soundProofXcorr':
                co_located_dict['threshold_percent_avg'] = np.mean(np.array(list(co_located_th_list), dtype=float))

            # Compute mean_mean, median_mean, std_mean, min_min, max_max, for non-colocated array
            non_colocated_dict['mean_mean'] = np.mean(non_colocated_mean_array)
            non_colocated_dict['median_mean'] = np.median(non_colocated_mean_array)
            non_colocated_dict['std_mean'] = np.std(non_colocated_mean_array)
            non_colocated_dict['min_min'] = np.amin(np.array(list(non_colocated_min_list), dtype=float))
            non_colocated_dict['max_max'] = np.amax(np.array(list(non_colocated_max_list), dtype=float))
            if feature == 'soundProofXcorr':
                non_colocated_dict['threshold_percent_avg'] = np.mean(np.array(list(non_colocated_th_list), dtype=float))

        elif feature == 'noiseFingerprint':
            # Convert co-located and non-colocated values to np arrays
            co_located_array = np.array(list(co_located_val), dtype=float)
            non_colocated_array = np.array(list(non_colocated_val), dtype=float)

            # Compute mean, median, std, min, max for co-located array
            co_located_dict['mean'] = np.mean(co_located_array)
            co_located_dict['median'] = np.median(co_located_array)
            co_located_dict['std'] = np.std(co_located_array)
            co_located_dict['min'] = np.amin(co_located_array)
            co_located_dict['max'] = np.amax(co_located_array)

            # Compute mean, median, std, min, max for non-colocated array
            non_colocated_dict['mean'] = np.mean(non_colocated_array)
            non_colocated_dict['median'] = np.median(non_colocated_array)
            non_colocated_dict['std'] = np.std(non_colocated_array)
            non_colocated_dict['min'] = np.amin(non_colocated_array)
            non_colocated_dict['max'] = np.amax(non_colocated_array)

        elif feature == 'timeFreqDistance':
            # Xcorr lists for max, min, mean (co-located and non-colocated)
            co_located_max_xcorr_list = []
            co_located_min_xcorr_list = []
            co_located_mean_xcorr_list = []

            non_colocated_max_xcorr_list = []
            non_colocated_min_xcorr_list = []
            non_colocated_mean_xcorr_list = []

            # Tfd lists for max, min, mean (co-located and non-colocated)
            co_located_max_tfd_list = []
            co_located_min_tfd_list = []
            co_located_mean_tfd_list = []

            non_colocated_max_tfd_list = []
            non_colocated_min_tfd_list = []
            non_colocated_mean_tfd_list = []

            # Get co-located values
            for val in co_located_val:
                # max_xcorr
                co_located_max_xcorr_list.append(val['max_xcorr']['max'])
                co_located_min_xcorr_list.append(val['max_xcorr']['min'])
                co_located_mean_xcorr_list.append(val['max_xcorr']['mean'])
                # time_freq_dist
                co_located_max_tfd_list.append(val['time_freq_dist']['max'])
                co_located_min_tfd_list.append(val['time_freq_dist']['min'])
                co_located_mean_tfd_list.append(val['time_freq_dist']['mean'])

            # Get non-colocated values
            for val in non_colocated_val:
                # max_xcorr
                non_colocated_max_xcorr_list.append(val['max_xcorr']['max'])
                non_colocated_min_xcorr_list.append(val['max_xcorr']['min'])
                non_colocated_mean_xcorr_list.append(val['max_xcorr']['mean'])
                # time_freq_dist
                non_colocated_max_tfd_list.append(val['time_freq_dist']['max'])
                non_colocated_min_tfd_list.append(val['time_freq_dist']['min'])
                non_colocated_mean_tfd_list.append(val['time_freq_dist']['mean'])

            # Result dictionaries for xcorr and tfd (co-located and non-colocated)
            co_located_xcorr_dict = {}
            non_colocated_xcorr_dict = {}

            co_located_tfd_dict = {}
            non_colocated_tfd_dict = {}

            # Convert co-located and non-colocated mean lists of xcorr and tfd to np arrays
            co_located_mean_xcorr_array = np.array(list(co_located_mean_xcorr_list), dtype=float)
            non_colocated_mean_xcorr_array = np.array(list(non_colocated_mean_xcorr_list), dtype=float)

            co_located_mean_tfd_array = np.array(list(co_located_mean_tfd_list), dtype=float)
            non_colocated_mean_tfd_array = np.array(list(non_colocated_mean_tfd_list), dtype=float)

            # Compute mean_mean, median_mean, std_mean, min_min, max_max, for co-located array xcorr
            co_located_xcorr_dict['mean_mean'] = np.mean(co_located_mean_xcorr_array)
            co_located_xcorr_dict['median_mean'] = np.median(co_located_mean_xcorr_array)
            co_located_xcorr_dict['std_mean'] = np.std(co_located_mean_xcorr_array)
            co_located_xcorr_dict['min_min'] = np.amin((np.array(list(co_located_min_xcorr_list), dtype=float)))
            co_located_xcorr_dict['max_max'] = np.amax((np.array(list(co_located_max_xcorr_list), dtype=float)))

            # Compute mean_mean, median_mean, std_mean, min_min, max_max, for non-colocated array xcorr
            non_colocated_xcorr_dict['mean_mean'] = np.mean(non_colocated_mean_xcorr_array)
            non_colocated_xcorr_dict['median_mean'] = np.median(non_colocated_mean_xcorr_array)
            non_colocated_xcorr_dict['std_mean'] = np.std(non_colocated_mean_xcorr_array)
            non_colocated_xcorr_dict['min_min'] = np.amin((np.array(list(non_colocated_min_xcorr_list), dtype=float)))
            non_colocated_xcorr_dict['max_max'] = np.amax((np.array(list(non_colocated_max_xcorr_list), dtype=float)))

            # Compute mean_mean, median_mean, std_mean, min_min, max_max, for co-located array tfd
            co_located_tfd_dict['mean_mean'] = np.mean(co_located_mean_tfd_array)
            co_located_tfd_dict['median_mean'] = np.median(co_located_mean_tfd_array)
            co_located_tfd_dict['std_mean'] = np.std(co_located_mean_tfd_array)
            co_located_tfd_dict['min_min'] = np.amin((np.array(list(co_located_min_tfd_list), dtype=float)))
            co_located_tfd_dict['max_max'] = np.amax((np.array(list(co_located_max_tfd_list), dtype=float)))

            # Compute mean_mean, median_mean, std_mean, min_min, max_max, for non-colocated array tfd
            non_colocated_tfd_dict['mean_mean'] = np.mean(non_colocated_mean_tfd_array)
            non_colocated_tfd_dict['median_mean'] = np.mean(non_colocated_mean_tfd_array)
            non_colocated_tfd_dict['std_mean'] = np.mean(non_colocated_mean_tfd_array)
            non_colocated_tfd_dict['min_min']= np.amin((np.array(list(non_colocated_min_tfd_list), dtype=float)))
            non_colocated_tfd_dict['max_max']= np.amax((np.array(list(non_colocated_max_tfd_list), dtype=float)))

            # Pack the results to co_located_dict and non_colocated_dict
            co_located_dict['max_xcorr'] = co_located_xcorr_dict
            co_located_dict['time_freq_dist'] = co_located_tfd_dict

            non_colocated_dict['max_xcorr'] = non_colocated_xcorr_dict
            non_colocated_dict['time_freq_dist'] = non_colocated_tfd_dict

        else:
            print('process_feature: unknown feature: %s --- exiting...' % feature)
            sys.exit(0)

        # Append co-located and non-colocated sensor lists
        co_located_dict['_sensors'] = co_located_list
        non_colocated_dict['_sensors'] = non_colocated_list

        # Add new fields to the results
        json['results']['co_located'] = co_located_dict
        json['results']['non_colocated'] = non_colocated_dict

        print('saving a file: %s' % json_file)

        # Save the updated JSON file
        with open(json_file, 'w') as f:
            f.write(dumps(json, indent=4, sort_keys=True))


def format_afp():

    # Audio feature
    feature = 'audioFingerprint'

    # Path to summary.json files
    afp_summary = ROOT_PATH + 'Sensor-*/audio/' + feature + '/*/' + SUMMARY_FILE
    last_afp_summary = ROOT_PATH + 'Sensor-' + str(NUM_SENSORS + 1) + '/audio/' + feature + '/*/'

    # Format results
    align_summary(afp_summary)
    add_last_summary(last_afp_summary, feature)

    # Wrap up results: overview of co-located vs. non-colocated
    wrap_up_results(afp_summary, feature)


def format_nfp():

    # Audio feature
    feature = 'noiseFingerprint'

    # Path to summary.json files
    nfp_summary = ROOT_PATH + 'Sensor-*/audio/' + feature + '/*/' + SUMMARY_FILE
    last_nfp_summary = ROOT_PATH + 'Sensor-' + str(NUM_SENSORS + 1) + '/audio/' + feature + '/*/'

    # Format results
    align_summary(nfp_summary)
    add_last_summary(last_nfp_summary, feature)

    # Wrap up results: overview of co-located vs. non-colocated
    wrap_up_results(nfp_summary, feature)


def format_spf():

    # Audio feature
    feature = 'soundProofXcorr'

    # Path to summary.json files
    spf_summary = ROOT_PATH + 'Sensor-*/audio/' + feature + '/*/' + SUMMARY_FILE
    last_spf_summary = ROOT_PATH + 'Sensor-' + str(NUM_SENSORS + 1) + '/audio/' + feature + '/*/'

    # Format results
    align_summary(spf_summary)
    add_last_summary(last_spf_summary, feature)

    # Wrap up results: overview of co-located vs. non-colocated
    wrap_up_results(spf_summary, feature)


def format_tfd():

    # Audio feature
    feature = 'timeFreqDistance'

    # Path to summary.json files
    tfd_summary = ROOT_PATH + 'Sensor-*/audio/' + feature + '/*/' + SUMMARY_FILE
    last_tfd_summary = ROOT_PATH + 'Sensor-' + str(NUM_SENSORS + 1) + '/audio/' + feature + '/*/'

    # Format results
    align_summary(tfd_summary)
    add_last_summary(last_tfd_summary, feature)

    # Wrap up results: overview of co-located vs. non-colocated
    wrap_up_results(tfd_summary, feature)


def format_power():

    # Power path - adjust this only
    # power_path = 'C:/Users/mfomichev/Desktop/car_power'

    # Audio feature
    feature = 'soundProofXcorr'

    # Path to result data files
    spf_path = ROOT_PATH + 'Sensor-*/audio/' + feature + '/*/Sensor-*.json'

    # Add power levels to result data files
    add_spf_power(spf_path, POWER_PATH)

if __name__ == "__main__":
    # Check the number of input args
    if len(sys.argv) == 3:

        # Assign input args
        scenario = sys.argv[1]
        ROOT_PATH = sys.argv[2]

        # Check if the second arg is a valid path
        if not os.path.exists(ROOT_PATH):
            print('<root_path>: %s does not exist!' % ROOT_PATH)
            exit(0)

        # Check if the first arg is a string 'car' or 'office'
        # or an existing path pointing to the power folder
        if scenario == 'car':
            NUM_SENSORS = 11
            SENSORS.append(SENSORS_CAR1)
            SENSORS.append(SENSORS_CAR2)
        elif scenario == 'office':
            NUM_SENSORS = 23
            SENSORS.append(SENSORS_OFFICE1)
            SENSORS.append(SENSORS_OFFICE2)
            SENSORS.append(SENSORS_OFFICE3)
        else:
            # In case of power scenario we expect existing POWER_PATH
            POWER_PATH = scenario
            if not os.path.exists(POWER_PATH):
                print('<power_path>: %s does not exist!' % POWER_PATH)
                exit(0)

            # Format power
            # format_power()

        # Format results
        '''
        format_afp()
        format_nfp()
        format_spf()
        format_tfd()
        '''

    else:
        print('Usage: aggregate_results.py <root_path> <num_workers>')
        sys.exit(0)



