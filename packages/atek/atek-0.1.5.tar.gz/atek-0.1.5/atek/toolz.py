#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from fnmatch import fnmatch
from tabulate import tabulate
from cytoolz.curried import pipe, curry, take, identity, map
from textwrap import fill
from typing import *
from atek.connect import query, show, paths, transpose
from pathlib import Path

__all__ = ["is_df", "filter_col"]

def is_df(obj: Any, param_name: str="dataframe") -> pd.DataFrame:
    if isinstance(obj, pd.DataFrame):
        return obj

    raise ValueError(f"arg '{param_name}' must be a pandas.DataFrame")

Record = Dict[str, Any]
Table = Iterable[Record]
TableOrDF = Union[pd.DataFrame, Table]

def to_records(data: TableOrDF) -> Table:
    return (
        data.to_dict("records") if isinstance(data, pd.DataFrame) else 
        data if isinstance(data, list) else 
        [row for row in data]
    )
        

@curry
def filter_col(patterns: Union[str, List[str]],
    data: TableOrDF) -> TableOrDF:
    """Filteres the columns of a dataframe using list
    of fnmatch patterns"""

    patterns = [patterns] if isinstance(patterns, str) else patterns
    def get_cols(cols, pats):
        return [
            col
            for col in cols
            for pat in pats
            if fnmatch(col.lower(), pat.lower())
        ]

    if isinstance(data, pd.DataFrame):
        return data.filter(get_cols(data.columns, patterns))

    if isinstance(data, Iterable):
        return pipe(
            data
            ,map(lambda d: {
                k: v
                for k, v in d.items()
                if k in get_cols([k for k in d], patterns)
            })
        )


if __name__ == "__main__":
    pipe(
        query("select * from orders limit 3")
        ,filter_col("*del*date*")
        ,list
        ,transpose
        ,show
    )
