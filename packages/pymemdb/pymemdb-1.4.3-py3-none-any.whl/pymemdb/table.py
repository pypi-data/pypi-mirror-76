from collections import defaultdict
from collections.abc import Iterable
from typing import Optional, Generator, Union, Hashable, List, Dict
import sys

import dataset

from pymemdb import Column, ColumnDoesNotExist


version = sys.version_info
if version.major < 3:  # pragma: no cover
    raise Exception("Python version must be 3.6 or higher")
if version.major >= 3 and version.minor < 8:  # pragma: no cover
    ORDER_TYPE = Union[str, bool]
else:  # pragma: no cover
    from typing import Literal  # type: ignore
    ORDER_TYPE = Literal["ascending", "descending", False]  # type:ignore

ROW_GEN = Generator[dict, None, None]


class Table:
    """Object that represents a Table in the Database.
       Can also used standalone"""

    def __init__(self, name: Optional[str] = None,
                 primary_id: str = "id") -> None:
        self.name = name
        self.idx_name = primary_id
        self._columns: defaultdict = defaultdict(Column)
        self.idx = 1
        self.keys: set = set()
        self.create_column(name=self.idx_name, unique=True)

    @classmethod
    def from_dataset(cls, table: dataset.table.Table, name=None) -> None:
        if name is None:
            name = table.name

        pk = None
        for col in table.table.columns:
            if col.primary_key is True:
                pk = col.name
                break

        pymemdb_table = cls(name, primary_id=pk)
        for row in table:
            pymemdb_table.insert(row)

        return pymemdb_table

    def to_dataset(self, db: dataset.Database, drop=False):
        if self.name in db.tables and drop:
            db[self.name].drop()
        if self.name not in db.tables:
            db.create_table(self.name, primary_id=self.idx_name)

        with db as tx:
            for row in self.all():
                tx[self.name].insert(row)

    def all(self, ordered: ORDER_TYPE = False) -> ROW_GEN:
        """returns a generator of all rows of the table.

        Keyword Arguments:
            ordered {["ascending", "descending", False]} -- Can be set to
                ascending or descending to sort by the primary id column
                (default: {False})
        Raises:
            ValueError: [if 'ordered' is not in {"ascending', 'descending',
                                                 False}]

        Returns:
            Generator -- [A Generator over all the rows in the table]

        Yields:
            dict -- [Dictionary that contains all elements of a row in the
                     table]
        """
        if ordered is False:
            for i in self.keys:
                yield self._get_row(i)
        elif ordered == "ascending":
            for i in sorted(self.keys):
                yield self._get_row(i)
        elif ordered == "descending":
            for i in sorted(self.keys, reverse=True):
                yield self._get_row(i)
        else:
            raise ValueError("Value for kwarg 'ordered' not in [False, "
                             "ascending, descending] !")

    def create_column(self, name: str, default: Hashable = None,
                      unique: bool = False) -> None:
        """Create a Column in the table.

        Arguments:
            name {str} -- Name of the column

        Keyword Arguments:
            default {Hashable} -- Default value for the column
                                    (default: {None})
            unique {bool} -- If values are enforced to be unique for this
                             column. If True, trying to insert a value more
                             than once will raise UniqueConstraintError
                             (default: {False})
        """
        self._columns[name] = Column(default=default, unique=unique)

    @property
    def columns(self) -> List[str]:
        """Returns a list of all column names of the table.

        Returns:
            List[str] -- [List of column names]

        """
        return list(self._columns)

    def drop(self) -> None:
        """Delete table."""
        del self

    def insert(self, row: Dict) -> int:
        """Inserts a row in the table. If a column is not present,
           it will be created with default value None

        Arguments:
            row {Dict} -- dictionary that represents a row in the table.

        Raises:
            UniqueConstraintError: [if constraint of a column is violated]

        Returns:
            int -- [primary key for the row inserted]
        """
        if self.idx_name in row:
            idx = row[self.idx_name]
        else:
            while self.idx in self.keys:
                self.idx += 1
            idx = self.idx
        self.keys.add(idx)
        for key, val in row.items():
            self._columns[key].insert(idx, val)
        if self.idx_name not in row:
            self._columns[self.idx_name].insert(idx, idx)
        return idx

    def insert_ignore(self, row: Dict, keys: List[str], ignore_errors: bool = True) -> Optional[int]:
        """Inserts rows into the table. If another row is already present
           where all the values are identical for the fields in 'keys', the
           insert will be skipped

        Arguments:
            row {Dict} -- [row to be inserted]
            keys {List[str]} -- [List of columns to check for ignore]

        Raises:
            UniqueConstraintError: [if constraint of a column is violated]

        Returns:
            Optional[int] -- [primary key for the row inserted or None if
                              the insert was skipped]

        """
        results = self.find(**{key: row[key] for key in keys}, ignore_errors=ignore_errors)
        try:
            next(results)
        except StopIteration:
            return self.insert(row)
        return None

    def find(self, ignore_errors: bool = True,
             **kwargs) -> Generator[dict, None, None]:
        """finds rows in the table.

        Keyword Arguments:
            **kwargs -- keyword is the column name and value represents the
                        value to search.
                        if value is in iterable, it matches a
                        SELECT * WHERE keyword IN val
                        search.
            ignore_errors {bool} -- if True, it raises an error if a column
                                    does not exist in the table
                                    (default: {False})

        Returns:
            Generator[dict] -- [Generator over all rows that match the search]
        """
        results = self._find_rows(ignore_errors=ignore_errors, **kwargs)

        for idx in results:
            yield {self.idx_name: idx, **self._get_row(idx)}

    def find_one(self, ignore_errors: bool = False, **kwargs) -> Optional[dict]:
        """finds a single row from the table, if there is one.
        Keyword Arguments:
            ignore_errors {bool} -- if True, it raises an error if a column
                                    does not exist in the table
                                    (default: {False})

        Returns:
            Optional[dict] -- single row from the table or None if there is
                              none that matches the query.
        """

        try:
            row = next(self.find(ignore_errors=ignore_errors, **kwargs))
        except StopIteration:
            return None
        return row

    def delete(self, ignore_errors: bool = False, **kwargs) -> int:
        pks = {row[self.idx_name] for row in self.find(**kwargs)}
        if len(pks) == 0 and not ignore_errors:
            raise KeyError(f"No matching rows found for {kwargs}")
        for pk in pks:
            self.keys.remove(pk)
        for col in self._columns.values():
            for pk in pks:
                col.drop(pk)
        return len(pks)

    def update(self, where: dict, **kwargs) -> int:
        pks = self._find_rows(**where)
        if not pks:
            return 0

        for col, val in kwargs.items():
            cell_dict = self._columns[col].cells
            val_dict = self._columns[col].values
            for pk in pks:
                cell_dict[pk] = val
                val_dict[val].add(pk)
        return len(pks)

    def update_replace(self, where: dict, **kwargs):
        n_rows = self.update(where=where, **kwargs)
        if n_rows == 0:
            return 0

        new_where = {**where, **kwargs}
        rows = self.find(**new_where)
        result_counter = defaultdict(frozenset)
        for row in rows:
            pk = row[self.idx_name]
            del row[self.idx_name]
            r = result_counter[tuple(row.items())]
            result_counter[tuple(row.items())] = r.union({pk})

        rowcount = 0
        for pks in result_counter.values():
            if len(pks) < 2:
                continue
            keep = min(pks)
            pks = pks.difference({keep})
            n = self.delete(**{self.idx_name: pks})
            rowcount += n

        return rowcount

    def _get_row(self, idx: int) -> dict:
        row = {col: self._columns[col].find_value(idx) for col in self.columns}
        row = {self.idx_name: idx, **row}
        return row

    def _find(self, col: str, val: Hashable) -> set:
        if isinstance(val, Iterable) and not isinstance(val, str):
            results: set = set()
            for v in val:
                results.update(self._columns[col].find(v))
            return results
        return self._columns[col].find(val)

    def _find_rows(self, ignore_errors: bool = True, **kwargs) -> set:
        results: set = set()
        for col, val in kwargs.items():
            if col not in self._columns:
                if ignore_errors:
                    continue
                else:
                    raise KeyError(f"Column {col} not in Table!")
            if len(results) == 0:
                results = self._find(col, val)
            else:
                pk = self._find(col, val)
                results = results.intersection(pk)
            if val == self._columns[col].default:
                column_cells = set(self._columns[col].cells)
                mis_def_keys = self.keys.symmetric_difference(column_cells)
                results.update(mis_def_keys)
            if not results:
                return set()
        return results

    def __eq__(self, other):
        return self.name == other.name

    def __getitem__(self, col):
        if col not in self._columns:
            raise ColumnDoesNotExist("Column {col} does not exist!")
        return self._columns[col]

    def __delitem__(self, col):
        if col not in self._columns:
            raise ColumnDoesNotExist(f"Column {col} does not exist!")
        del self._columns[col]

    def __len__(self):
        return len(self.keys)
