"""Utils module."""

__all__ = ['convert_choice', 'convert_loglevel', 'convert_predicate',
           'convert_string', 'create_getter', 'create_setter', 'create_deleter']


def convert_choice(choices, *, converter=None, default=None):
    """Return a function that can be used as a converter.

    For an example see the source code of :func:`convert_loglevel`.

    :param choices: any container type that supports the ``in`` operator
                    with acceptable values
    :param converter: a callable that takes one string argument and returns
                      an object of the desired type; ``None`` means no
                      conversion
    :param default: a default value of the desired type or a subclass
                    of :exc:`Exception` which will be raised
    :return: converter function
    :rtype: function(str)
    """
    def f(s):
        x = converter(s) if converter else s
        if x in choices:
            return x
        if isinstance(default, type) and issubclass(default, Exception):
            raise default(f'invalid choice: {s}')
        return default
    return f


_LOGLEVELS = {
    'NOTSET': 0,
    'DEBUG': 10,
    'INFO': 20,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50
}


def convert_loglevel(default_level=None, *, numeric=False):
    """Return a converter function for logging levels.

    Valid values are the logging levels as defined in the :mod:`logging` module.

    :param str default_level: the default logging level
    :param bool numeric: if ``True`` the numeric value of the log level
                         will be returned
    :raises ValueError: if not a valid logging level and ``default_level=None``
    :return: converter function
    :rtype: function(str)
    """
    if numeric:
        choices = _LOGLEVELS.values()
        converter = lambda s: _LOGLEVELS.get(str(s).upper(), s)  # noqa: E731
    else:
        choices = _LOGLEVELS.keys()
        converter = lambda s: str(s).upper()  # noqa: E731
    default = default_level or ValueError
    return convert_choice(choices, converter=converter, default=default)


def convert_predicate(predicate, *, converter=None, default=None):
    """Return a converter function with a predicate.

    >>> positive_float = convert_predicate(lambda x: x > 0.0,
    ... converter=float, default=0.0)
    >>> positive_float('1.2')
    1.2
    >>> positive_float('-1.2')
    0.0

    :param predicate: a callable that takes one argument of the desired type
                      and returns ``True`` if it is acceptable
    :param converter: a callable that takes one string argument and returns
                      an object of the desired type; ``None`` means no
                      conversion
    :param default: a default value of the desired type or a subclass
                    of :exc:`Exception` which will be raised instead
    :return: converter function
    :rtype: function(str)
    """
    def f(s):
        x = converter(s) if converter else s
        if predicate(x):
            return x
        if isinstance(default, type) and issubclass(default, Exception):
            raise default(f'invalid value: {s}')
        return default
    return f


def convert_string(*, start='|', newlines=True):
    """Return a function that can be used as a converter.

    The default converter ``str`` handles multiline values like
    :class:`~configparser.ConfigParser`, i.e. preserving newlines but
    ignoring indentations (because nothing gets realy converted).

    A converter returned by this function can handle such values different.

    >>> s = '''
    ... |def add(a, b):
    ... |    return a + b
    '''
    >>> print(convert_string()(s))
    def add(a, b):
        return a + b

    :param str start: a single none-whitspace character that starts a line
    :param bool newlines: if ``True`` newlines will be preserved
    :raises ValueError: if ``start`` is not a single character
    :return: converter function
    :rtype: function(str)
    """
    start = start.strip()
    if len(start) != 1:
        raise ValueError("parameter 'start' must be a single"
                         " none-whitespace character")

    def f(s):
        lines = s.strip().splitlines()
        if not all(map(lambda line: line and line[0] == start, lines)):
            raise ValueError(f'all lines must start with {start!r}')
        lines = [line[1:] for line in lines]
        return '\n'.join(lines) if newlines else ''.join(lines)
    return f


def create_getter(key):
    """Create getter method."""
    def f(self):
        return self._values[key]
    return f


def create_setter(key):
    """Create setter method."""
    def f(self, value):
        self._values[key] = value
    return f


def create_deleter(key):
    """Create deleter method."""
    def f(self):
        del self[key]
    return f
