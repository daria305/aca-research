import math

import pandas as pd
import itertools
import os

ending_cri_temp = "_criticalTemp.csv"
ending_std = "_stddev.csv"
ending_adj = "_adjacencyMatrix.csv"
ending_states = "historicalStates"

states_header = ["N", "k", "Init", "Temp", "Unique States", "Pattern Length", "Pattern", "Repetition Start Index", "Times Repeated"]


def get_file_paths(path_to_data: str):
    file_names = []
    file_paths = []
    for paths, _, files in os.walk(path_to_data):
        if len(files) > 0:
            file_names.extend(files)
            file_paths.extend([paths] * len(files))
    return file_paths, file_names


def read_data(path_to_data: str):
    paths, files = get_file_paths(path_to_data)
    all = []
    for path, filename in zip(paths, files):
        if ending_states in filename:
            results_row = read_stats_file(path, filename)
            print(results_row)
            all.append(results_row)
    results_df = pd.DataFrame(all, columns=states_header)

    print(results_df.head())
    results_df.to_csv(os.path.join(path_to_data, "results.csv"), index=False)


def read_parameters(file_name):
    params = {}
    s = file_name.split("_")
    params["N"] = int(s[2])
    params["k"] = int(s[4])
    params["Init"] = s[9]
    params["Temp"] = float(s[12][:-4])
    return params


def read_stats_file(path: str, file_name: str):
    print("Reading stats file: ", file_name)
    with open(os.path.join(path, file_name)) as rf:
        df = pd.read_csv(rf, sep=',')
    df.columns = ["node_"+str(i) for i in range(len(df.columns))]
    df["joined"] = df.astype(str).agg(''.join, axis=1)
    results = read_parameters(file_name)
    results["Unique States"] = count_unique(df)
    m, pattern, index, times_repeated = find_repetition(list(df["joined"]))
    results["Pattern Length"] = m
    results["Pattern"] = pattern
    results["Repetition Start Index"] = index
    results["Times Repeated"] = times_repeated
    return results


def count_unique(df: pd.DataFrame):
    return df.drop_duplicates().shape[0]


def find_repetition(x: []):
    max_memory = math.floor(len(x) / 2)
    for m in range(2, max_memory):
        pattern = x[-m:]
        cursor = len(pattern) - 1
        for i, row in enumerate(reversed(x)):
            # print("Cursor: ", cursor, "element: ", pattern[cursor])
            if row != pattern[cursor]:
                index = len(x) - i
                if i+1 > 2*m:
                    rep_N_times = math.floor((len(x) - index) / m)
                    print("Found repetition for memory: ", m, "pattern: ", pattern, ", starting at index: ", index, "repeated", rep_N_times, "times")
                    return m, pattern, index, rep_N_times
                # print("No repetition found, break at index", index, "memory=", m)
                break
            cursor -= 1
            if cursor < 0:
                cursor = len(pattern) - 1
    return None, None, None, None


if __name__ == "__main__":
    test()
