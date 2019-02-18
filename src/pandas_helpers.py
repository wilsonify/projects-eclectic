import re
import numpy as np
import pandas as pd
import logging


def clean_column_names(self):
    logging.info("clean_column_names")
    new_column_names = {old: old.lower() for old in self.columns}

    replacements = [(r"\W", "_"),
                    (r"_+", "_")
                    ]

    for pat, rep in replacements:
        logging.debug("replacing {} with {}".format(pat, rep))
        new_column_names = {old: re.sub(string=new_column_names[old],
                                        pattern=pat,
                                        repl=rep)
                            for old in self.columns}

    logging.debug("stripping _")
    new_column_names = {old: new_column_names[old].strip("_") for old in self.columns}
    logging.debug("rename dict = {}".format(new_column_names))

    return self.rename(columns=new_column_names)


pd.DataFrame.clean_column_names = clean_column_names


def parse_date_columns(self):
    logging.info("parse_date_columns")
    for date_column in self.filter(regex="date").columns:
        logging.debug("parsing {}".format(date_column))
        self[date_column] = pd.to_datetime(self[date_column])
    return self


pd.DataFrame.parse_date_columns = parse_date_columns


def zero_to_null(self, subset):
    logging.info("zero_to_null")
    for column in subset:
        logging.debug("converting {} zero to null".format(column))
        self[column] = self[column].apply(lambda x: x if x != 0 else np.nan)
    return self


pd.DataFrame.zero_to_null = zero_to_null


def merge_multi(self, df, **kwargs):
    logging.info("multi index merge")
    try:
        left = self.reset_index()
    except ValueError as ve:
        logging.debug("{}, try reset_index".format(ve))
        left = self.reset_index(drop=True)

    try:
        right = df.reset_index()
    except ValueError as ve:
        logging.debug("{}, try reset_index".format(ve))
        right = df.reset_index(drop=True)

    return left.merge(right, **kwargs).set_index(
        self.index.names
    )


pd.DataFrame.merge_multi = merge_multi


def deduplicate(self, key, numeric_column="max", non_numeric="first", override: dict = None):
    logging.info("deduplicate")
    if override is None:
        override = dict([])
    how_to_agg = {
        index: numeric_column if np.issubdtype(value, np.number) else non_numeric
        for (index, value) in self.dtypes.iteritems()
    }
    how_to_agg.update(override)
    logging.debug("aggregating {} groups {}".format(key, how_to_agg))
    return self.groupby(key).agg(how_to_agg)


pd.DataFrame.deduplicate = deduplicate


def parse_api_columns(self):
    logging.info("parse_api_columns")
    for api_column in self.filter(regex="api").columns:
        logging.debug("formatting {}".format(api_column))
        self[api_column] = self[api_column] \
            .apply(str) \
            .str.replace(r"\W", "") \
            .str.pad(14, side="right", fillchar="0")
    return self


pd.DataFrame.parse_api_columns = parse_api_columns
