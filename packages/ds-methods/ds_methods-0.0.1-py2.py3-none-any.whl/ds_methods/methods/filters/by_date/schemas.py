from datetime import datetime
from schema import Schema, Optional, And


options_schema = Schema(
    And({
        Optional('gte'): datetime,
        Optional('lte'): datetime,
    }, lambda x: 'gte' in x or 'lte' in x),
    ignore_extra_keys=True,
)
