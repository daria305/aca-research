import pandas as pd
from tabulate import tabulate

from read_data import read_data


def hist(df: pd.DataFrame):
    print(df.columns)
    df.filter(items=["N", "k", "Max Temperature"])
    print(df.head())
    df.hist(column="'Max Temperature", bins=100)


def process_crit_results(results_df: pd.DataFrame, df: pd.DataFrame, filename: str):
    results_row = read_parameters(filename)
    results_row["Max Temp States"] = df["Crit Temperature"].max()
    results_row["Mean Temp"] = df["Crit Temperature"].mean()
    results_row["Initial States Number"] = df["Crit Temperature"].size
    results_df = results_df.append(results_row, ignore_index=True)
    return results_df


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


if __name__ == "__main__":
    read_data("./data/aca-search-result-t5n6k4")

