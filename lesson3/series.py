from numbers import Number


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

        Args:
            other (Series):

        Returns:
            bool
        """
        if not isinstance(other, Series):
            raise TypeError("Operation not supported")

        return self._values == other._values and self._index == other._index

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
        Return a new series with boolean values, true if the condition
        is satisfied by an element at that index, False otherwise.

        Args:
            other (Number):

        Returns:
            Series
        """
        if isinstance(other, Number):
            # Generalise this by replacing "<" with operator.lt(v, other)
            new_values = [v < other for v in self._values]
            return Series(new_values, index=self._index)

        elif isinstance(other, Series):
            values = [
                left < right
                for left, right in zip(self._values, other._values)
            ]
            return Series(values, index=self._index)

        else:
            raise TypeError("operation not supported")

    def __le__(self, other):
        if not isinstance(other, Number):
            raise NotImplementedError()

        new_values = [v <= other for v in self._values]

        return Series(new_values, index=self._index)

    def __eq__(self, other):
        if isinstance(other, Number):
            new_values = [v == other for v in self._values]
            return Series(new_values, index=self._index)

        values = [left == right for left, right in zip(self._values, other._values)]
        return Series(values, index=self._index)

    def __repr__(self):
        """
        Repr should return a string that holds a valid expression which
        when executed instantiates an equivalent object.

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
