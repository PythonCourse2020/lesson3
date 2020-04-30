from math import inf, isnan, nan
from numbers import Number
import operator


class Series:
    def __init__(self, values=None, index=None):
        """
        Args:
            values (None | Number | list): Values of the series. Defaults
                to None.
            index (None | list): Indices to use for the series. Defaults to
                None
        """
        if values is None:
            values = []
        elif isinstance(values, Number):
            values = [values]
        else:
            values = list(values)

        if index is None:
            index = list(range(len(values)))
        else:
            index = list(index)

        if len(values) != len(index):
            raise ValueError("values must have the same length as index")

        self._values = values
        self._index = index

    def eq(self, other):
        """
        Checks if two series are equal to each other. Two series are
        equal if they have the same values and the same index. A TypeError
        is raised if other is not a Series.

        A special case exists for math.nan values. By design, nan != nan, so the
        expectation is that the way to identify if two values are both nan is by
        using the 'is' operator. However, nan is not always treated as a singleton.
        To address this issue, an additional last resort check is performed on the values
        using math.isnan.

        Args:
            other (Series):

        Returns:
            bool
        """
        if not isinstance(other, Series):
            raise TypeError("Operation not supported")

        # Short-circuit if the lengths are different
        if len(self) != len(other):
            return False

        # Short circuit for simple equality
        if self._values == other._values and self._index == other._index:
            return True

        return all(
            i1 == i2 and ((v1 == v2) or (v1 is v2) or (isnan(v1) and isnan(v2)))
            for (i1, v1), (i2, v2) in zip(self.iteritems(), other.iteritems())
        )

    @property
    def index(self):
        """
        Return the index in a copied list.

        Returns:
            list
        """
        return list(self._index)

    @property
    def loc(self):
        """
        Implemented by __getitem__. Using @property to enable .loc[key]
        instead of .loc(key).

        Args:
            key (object):

        Returns:
            Number
        """
        return self

    @property
    def iloc(self):
        """
        Positional index access to values.

        Returns:
            list
        """
        return list(self._values)

    def iteritems(self):
        """
        Returns a generator yielding tuple(index, value) for each
        element of the Series.

        Returns:
            generator (object, Number)
        """
        return zip(self._index, self._values)

    def __contains__(self, key):
        """
        Implementation of "in" operator. Checks if the value exists
        in index.

        Args:
            key (object):
        
        Returns:
            bool
        """
        return key in self._index

    def __getitem__(self, key):
        """
        This method implements list-like access e.g. self[key]. We use this
        as an equivalent to .loc - the implementation for it calles this method.
        The counterpart of this, for setting values using e.g. self[key] = value
        is __setitem__.

        Raises an IndexError if key does not exist in index.

        Args:
            key (object):

        Returns:
            Number
        """
        if isinstance(key, Series):
            return self._getitem_by_series(key)

        return self._getitem_by_index(key)

    def __setitem__(self, key, value):
        index = self._index.index(key)

        self._values[index] = value

    def _getitem_by_series(self, bool_slice):
        index = []
        values = []

        for i, v in zip(bool_slice._index, bool_slice._values):
            if v is True:
                index.append(i)
                values.append(self[i])

        return Series(values, index=index)

    def _getitem_by_index(self, key):
        try:
            # index is a method of list() which returns the first occurance
            # of a value in a list or throws a ValueError if it doesn't
            # exist
            index = self._index.index(key)
        except ValueError:
            raise IndexError(f"Index {key} not found")

        return self._values[index]

    def __iter__(self):
        """
        The iterator is over a copy of self._valuess.

        Returns:
            iter
        """
        return iter(list(self._values))

    def __len__(self):
        """
        Returns the length of the series.

        Returns:
            int
        """
        return len(self._values)

    def __lt__(self, other):
        """
        Implementation of '<' operator. Dispatched to _boolean_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._boolean_bin_op(operator.lt, other)

    def __le__(self, other):
        """
        Implementation of '<=' operator. Dispatched to _boolean_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._boolean_bin_op(operator.le, other)

    def __eq__(self, other):
        """
        Implementation of '==' operator. Dispatched to _boolean_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._boolean_bin_op(operator.eq, other)

    def __ne__(self, other):
        """
        Implementation of '!=' operator. Dispatched to _boolean_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._boolean_bin_op(operator.ne, other)

    def __ge__(self, other):
        """
        Implementation of '>=' operator. Dispatched to _boolean_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._boolean_bin_op(operator.ge, other)

    def __gt__(self, other):
        """
        Implementation of '>' operator. Dispatched to _boolean_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._boolean_bin_op(operator.gt, other)

    def __add__(self, other):
        """
        Implementation of '+' operator. Dispatched to _arithmetic_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._arithmetic_bin_op(operator.add, other)

    def __sub__(self, other):
        """
        Implementation of '-' operator. Dispatched to _arithmetic_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._arithmetic_bin_op(operator.sub, other)

    def __truediv__(self, other):
        """
        Implementation of '/' operator. Dispatched to _arithmetic_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._arithmetic_bin_op(operator.truediv, other, inf)

    def __floordiv__(self, other):
        """
        Implementation of '//' operator. Dispatched to _arithmetic_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._arithmetic_bin_op(operator.floordiv, other, inf)

    def __mul__(self, other):
        """
        Implementation of '*' operator. Dispatched to _arithmetic_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._arithmetic_bin_op(operator.mul, other)

    def __mod__(self, other):
        """
        Implementation of '%' operator. Dispatched to _arithmetic_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._arithmetic_bin_op(operator.mod, other, nan)

    def __pow__(self, other):
        """
        Implementation of '**' operator. Dispatched to _arithmetic_bin_op. 
        Supported types for other are Number and Series.
        
        Args:
            other (Number|Series):
        
        Returns:
            Series
        """
        return self._arithmetic_bin_op(operator.pow, other)

    def __neg__(self):
        """
        Implementation of '-' unary operator. Dispatched to _unary_op. 

        Returns:
            Series
        """
        return self._unary_op(operator.neg)

    def __pos__(self):
        """
        Implementation of '+' unary operator. Dispatched to _unary_op. 

        Returns:
            Series
        """
        return self._unary_op(operator.pos)

    def __repr__(self):
        """
        Repr should return a string that holds a valid expression which
        when executed instantiates an equivalent object.

        E.g:
            Series([10, 20]) ->
                Series([10, 20], index=[0, 1])
            
            Series() ->
                Series([], index=[])
            
        Returns:
            str
        """
        template = "Series({values}, index={index})"

        return template.format(values=str(self._values), index=str(self._index))

    def __str__(self):
        """
        Returns a string, one row per series item, with index separated
        by value through a tab. If the series is empty, the string
        Series([]) is returned

        E.g:
            Series([10, 20]) -> 
                0   10
                1   20
            
            Series() ->
                Series([])
        
        Returns:
            str
        """
        # Can use len(self) here as __len__ is implemented!
        if len(self) == 0:
            return "Series([])"

        item_template = "{0}\t{1}"
        rows = [
            item_template.format(index, value)
            for index, value in zip(self._index, self._values)
        ]

        return "\n".join(rows)

    def _zip_series_by_index(self, other):
        """
        Takes the current series and another series and matches them element by element 
        on index, using the ordering in the current series. For any disjoint elements,
        it uses nan as value. The return value is a generator for a 2-tuple,
        the first element being the index and the second being a 2-tuple
        of the values at that index of the current series and the other series
        respectively.

        E.g:
            a = Series([10, 20, 30], index=[0, 1, 2])
            b = Series([1, 2, 3], index=[1, 2, 3])
            
            Series._zip_series_by_index(a, b) yields:
                (0, (10, nan))
                (1, (20, 1)),
                (2, (30, 2)),
                (3, (nan, 3))
        Args:
            other (Series):
        
        Returns:
            iter(tuple(object, tuple(Number, Number))):
        """
        for index in self._index:
            # Index in both series
            if index in other._index:
                yield index, (self[index], other[index])
            else:
                yield index, (self[index], nan)

        # For the given series, we only need to look at the missing indices
        for index in other._index:
            if index not in self._index:
                yield index, (nan, other[index])

    def _arithmetic_bin_op(self, op, other, zero_div_result=None):
        """
        Applies a binary arithmetic function op on the current instance and returns
        a new Series.

        Args:
            op (callable):
            other (Number|Series):
            zero_div_result (None|object): Value to replace operation
                results when a ZeroDivisionError is raised. Defaults to None,
                which means that the error is not suppressed.

        Returns:
            Series
        """
        if isinstance(other, Number):
            return self._arithmetic_bin_op_scalar(op, other, zero_div_result)
        elif isinstance(other, Series):
            return self._arithmetic_bin_op_series(op, other, zero_div_result)

        raise NotImplementedError()

    def _arithmetic_bin_op_series(self, op, series, zero_div_result=None):
        """
        Apply op function on the current instance and a series.
        Returns a Series with retrn values of op. Values can also be nan
        if the element did not exist at a particular index, as the returned
        series has the indices in both series.

        Args:
            op (callable): Function that takes two parameters and returns
                a bool.
            series (Series):
            zero_div_result (None|object):
        
        Returns:
            Series
        """
        index = []
        values = []

        for i, (left, right) in self._zip_series_by_index(series):
            index.append(i)

            try:
                values.append(op(left, right))
            except ZeroDivisionError:
                if zero_div_result is not None:
                    values.append(zero_div_result)
                else:
                    raise

        return Series(values, index=index)

    def _arithmetic_bin_op_scalar(self, op, scalar, zero_div_result=None):
        """
        Apply op function on the current instance and a scalar.
        Returns a Series with the same index as the current instance
        and the return value of op.

        Args:
            op (callable): Function that takes two parameters and returns
                a bool.
            scalar (Number):
            zero_div_result (None|object):
        
        Returns:
            Series
        """
        try:
            values = [op(v, scalar) for v in self._values]
        except ZeroDivisionError:
            if zero_div_result is not None:
                values = [zero_div_result] * len(self)
            else:
                raise

        return Series(values, index=self._index)

    def _boolean_bin_op(self, op, other):
        """
        Applies a boolean binary operation op on the current instance and returns
        a new Series.

        Args:
            op (callable):
            other (Number|Series):
        
        Returns:
            Series
        """
        if isinstance(other, Number):
            return self._boolean_bin_op_scalar(op, other)
        elif isinstance(other, Series):
            return self._boolean_bin_op_series(op, other)

        raise NotImplementedError()

    def _boolean_bin_op_series(self, op, series):
        """
        Apply op element-wise and return a new series. The indices must
        match perfectly, otherwise a ValueError is raised.

        Args:
            op (callable): Function that takes two parameters and returns
                a bool.
            series (Seried):
        
        Returns:
            Series
        """
        if self._index != series._index:
            raise ValueError("Index mismatch")

        values = [op(a, b) for a, b in zip(self._values, series._values)]

        return Series(values, index=self._index)

    def _boolean_bin_op_scalar(self, op, scalar):
        """
        Apply op function on the current instance and a scalar.
        Returns a Series with the same index as the current instance
        and the return value of op.

        Args:
            op (callable): Function that takes two parameters and returns
                a bool.
            scalar (Number):
        
        Returns:
            Series
        """
        values = [op(v, scalar) for v in self._values]

        return Series(values, index=self._index)

    def _unary_op(self, op):
        """
        Takes a unary operation op and applies it to each element in the
        current series. Runs op element-wise and returns a new Series with the
        same index and the resulting values.

        Args:
            op (callable):
        
        Returns:
            Series
        """
        values = [op(v) for v in self._values]

        return Series(values, index=self._index)
