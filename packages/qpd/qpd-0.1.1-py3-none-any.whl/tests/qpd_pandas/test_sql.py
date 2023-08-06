from typing import Any

import pandas as pd

from qpd_pandas import QPDPandasEngine
from qpd_test.sql_suite import SQLTests


class PandasSQLTests(SQLTests.Tests):
    def make_qpd_engine(self):
        return QPDPandasEngine()

    def to_native_df(self, data: Any, columns: Any) -> Any:  # pragma: no cover
        if isinstance(data, pd.DataFrame):
            return data
        return pd.DataFrame(data, columns=columns)
