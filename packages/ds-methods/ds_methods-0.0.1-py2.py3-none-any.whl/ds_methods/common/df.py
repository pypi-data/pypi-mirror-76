from typing import Dict, List, Tuple
from numbers import Number
import pandas as pd
from pandas import DataFrame

from .constants import MIN_ROWS_FOR_ACC


class DataFrameUtils:
    @staticmethod
    def get_query_value(value) -> str:
        if not isinstance(value, Number):
            return f"'{value}'"

        return f"{value}"

    @staticmethod
    def compose_query(options: Dict[str, Dict]) -> str:
        filters = []
        for key in options:
            key_options = options[key]
            if 'equal' in key_options:
                filters.append(f"{key} == {DataFrameUtils.get_query_value(key_options['equal'])}")
            else:
                if 'gte' in key_options:
                    filters.append(f"{key} >= {DataFrameUtils.get_query_value(key_options['gte'])}")
                if 'lte' in key_options:
                    filters.append(f"{key} <= {DataFrameUtils.get_query_value(key_options['lte'])}")

        return ' and '.join(filters)

    @staticmethod
    def eval_query(input_data: DataFrame, query: str) -> DataFrame:
        """
        'python' engine is faster for a small data
        """
        if len(input_data.index) < MIN_ROWS_FOR_ACC:
            return input_data.query(query, engine='python')

        return input_data.query(query)

    @staticmethod
    def concatenate_parts(parts: List[DataFrame]) -> DataFrame:
        return pd.concat(
            [part.reset_index(drop=True) for part in parts],
            sort=False,
            axis='columns',
            copy=False,
        ).dropna()

    @staticmethod
    def decompose_into_parts(input_data: DataFrame, include: List[str] = None) -> Tuple[DataFrame, DataFrame]:
        if not include:
            include = ['number']

        return input_data.select_dtypes(include=include), input_data.select_dtypes(exclude=include)
