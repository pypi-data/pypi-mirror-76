from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

from qpd.dataframe import Column, DataFrame
from qpd.specs import (
    AggFunctionSpec,
    ArgumentSpec,
    IsValueSpec,
    OrderBySpec,
    WindowFunctionSpec,
)


class QPDEngine(ABC):
    def __call__(self, func_name: str, *args: Any, **kwargs: Any) -> Any:
        return getattr(self, func_name)(*args, **kwargs)

    def rename(self, col: Column, name: str) -> Column:
        return col.rename(name)

    def extract_col(self, df: DataFrame, name: str) -> Column:
        return df[name]

    def assemble_df(self, *args: Any) -> DataFrame:
        return DataFrame(*args)

    @abstractmethod
    def to_df(self, obj: Any) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def to_col(self, value: Any, name: str = "") -> Column:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def to_native(self, df: DataFrame) -> Any:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def basic_unary_arithmetic_op(
        self, col: Column, op: str
    ) -> Column:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def binary_arithmetic_op(
        self, col1: Column, col2: Column, op: str
    ) -> Column:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def comparison_op(
        self, col1: Column, col2: Column, op: str
    ) -> Column:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def binary_logical_op(
        self, col1: Column, col2: Column, op: str
    ) -> Column:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def logical_not(self, col: Column) -> Column:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def filter_col(self, col: Column, cond: Column) -> Column:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def is_value(
        self, col: Column, is_value: IsValueSpec
    ) -> Column:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def is_in(
        self, col: Column, *values: Any, positive: bool
    ) -> Column:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def is_between(
        self, col: Column, lower: Column, upper: Column, positive: bool
    ) -> Column:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def filter_df(self, df: DataFrame, cond: Column) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def case_when(self, *cols: Column) -> Column:  # pragma: no cover
        """ `cols` must be in the format of
        `when1`, `value1`, ... ,`default`, and length must be >= 3.
        The reason to design the interface in this way is to simplify the translation
        from SQL to engine APIs.

        :return: [description]
        :rtype: Column
        """
        raise NotImplementedError

    @abstractmethod
    def drop_duplicates(self, df: DataFrame) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def order_by_limit(
        self, df: DataFrame, order_by: OrderBySpec, limit: int
    ) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def union(
        self, df1: DataFrame, df2: DataFrame, unique: bool
    ) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def intersect(
        self, df1: DataFrame, df2: DataFrame, unique: bool
    ) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def except_df(
        self, df1: DataFrame, df2: DataFrame, unique: bool
    ) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def join(
        self, df1: DataFrame, df2: DataFrame, join_type: str, on: List[str]
    ) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def group_agg(
        self,
        df: DataFrame,
        keys: List[str],
        agg_map: Dict[str, Tuple[str, AggFunctionSpec]],
    ) -> DataFrame:  # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def window(  # noqa: C901
        self,
        df: DataFrame,
        func: WindowFunctionSpec,
        args: List[ArgumentSpec],
        dest_col_name: str,
    ) -> DataFrame:  # pragma: no cover
        raise NotImplementedError
