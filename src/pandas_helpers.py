import re
import numpy as np
import pandas as pd


def clean_column_names(self):
    new_column_names = {old: old.lower() for old in self.columns}

    replacements = [("\W", "_"),
                    ("_+", "_")
                    ]
    for pat, rep in replacements:
        new_column_names = {old: re.sub(string=new_column_names[old],
                                        pattern=pat,
                                        repl=rep)
                            for old in self.columns}

    new_column_names = {old: new_column_names[old].strip("_") for old in self.columns}

    return self.rename(columns=new_column_names)


pd.DataFrame.clean_column_names = clean_column_names


def parse_date_columns(self):
    for date_column in self.filter(regex="date").columns:
        self[date_column] = pd.to_datetime(self[date_column])
    return self


pd.DataFrame.parse_date_columns = parse_date_columns


def zero_to_null(self, subset):
    for column in subset:
        self[column] = self[column].apply(lambda x: x if x != 0 else np.nan)
    return self


pd.DataFrame.zero_to_null = zero_to_null


def merge_multi(self, df, on="api", how="left", suffixes=("", "r")):
    try:
        left = self.reset_index()
    except ValueError:
        left = self.reset_index(drop=True)

    try:
        right = df.reset_index()
    except ValueError:
        right = df.reset_index(drop=True)

    return left.merge(right, on=on, how=how, suffixes=suffixes).set_index(
        self.index.names
    )


pd.DataFrame.merge_multi = merge_multi


def deduplicate(self, key, numeric_column="max", non_numeric="first", override: dict = None):
    if override is None:
        override = dict([])
    how_to_agg = {
        index: numeric_column if np.issubdtype(value, np.number) else non_numeric
        for (index, value) in self.dtypes.iteritems()
    }
    how_to_agg.update(override)
    return self.groupby(key).agg(how_to_agg)


pd.DataFrame.deduplicate = deduplicate


def parse_api_columns(self):
    for api_column in self.filter(regex="api").columns:
        self[api_column] = self[api_column] \
            .apply(str) \
            .str.replace(r"\W", "") \
            .str.pad(14, side="right", fillchar="0")
    return self


pd.DataFrame.parse_api_columns = parse_api_columns
