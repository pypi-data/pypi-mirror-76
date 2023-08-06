from schema import Schema, And

from ds_methods.common.enums import BaseEnum


class BasicMethod(BaseEnum):
    MIN = 'min'
    MAX = 'min'
    MEAN = 'mean'
    MEDIAN = 'median'
    STD = 'std'


options_schema = Schema(
    {'method': And(str, lambda x: BasicMethod.validate(x))},
    ignore_extra_keys=True,
)
