import pandas as pd
from tabulate import tabulate
import os


def get_file_paths(path_to_data:str):
    file_names = []
    file_paths = []
    for paths, _, files in os.walk(path_to_data):
        if len(files) > 0:
            file_names.extend(files)
            file_paths.extend([paths] * len(files))
    return file_paths, file_names


def read_data():
    stdev_ending = "_stddev.csv"
    crit_ending = "_criticalTemp.csv"
    temp_ending = "_temp.csv"

    result_header = ["N", "k", "Init", "Max Temperature", "Steps", "Weak steps", "Max Temp States", "Mean Temp", "Initial States Number"]
    results = pd.DataFrame(columns=result_header)

    paths, files = get_file_paths("data/oldformat/modified")
    for path, filename in zip(paths, files):

        # critical temperatures loading, loaded vector represents critical temperatures for many initial states
        if filename.endswith(crit_ending):
            with open(os.path.join(path, filename)) as rf:
                df = pd.read_csv(rf, sep=',')
                df.columns = ["Crit Temperature"]
                results = process_crit_results(results, df, filename)

        # std loading
        if filename.endswith(stdev_ending):
            pass
        # temperature log loading
        if filename.endswith(temp_ending):
            pass
    return results


def hist(df: pd.DataFrame):
    print(df.columns)
    df.filter(items=["N", "k", "Max Temperature"])
    print(df.head())
    df.hist(column="'Max Temperature", bins=100)


def read_parameters(filename: str):
    results_row = {}
    s = filename.split("_")
    results_row["N"] = s[2]
    results_row["k"] = s[4]
    results_row["Init"] = s[9]
    results_row["Max Temperature"] = s[12]
    results_row["Steps"] = s[14]
    results_row["Weak Steps"] = s[16]
    return results_row


def process_crit_results(results_df: pd.DataFrame, df: pd.DataFrame, filename: str):
    results_row = read_parameters(filename)
    results_row["Max Temp States"] = df["Crit Temperature"].max()
    results_row["Mean Temp"] = df["Crit Temperature"].mean()
    results_row["Initial States Number"] = df["Crit Temperature"].size
    results_df = results_df.append(results_row, ignore_index=True)
    return results_df


if __name__ == "__main__":
    df = read_data()
    # hist(df)
    print(tabulate(df, headers="keys", tablefmt="psql"))

