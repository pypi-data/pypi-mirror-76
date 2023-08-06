"""Config module."""

from configparser import ConfigParser

from salmagundi.utils import check_path_like

from ._errors import ReadonlyError, DuplicateError, ConfigError
from ._utils import create_getter, create_setter, create_deleter

__all__ = ['Config', 'NOVALUE', 'NOTFOUND']


NOVALUE = type('NoValue', (), {
    '__repr__': lambda x: '<NOVALUE>',
    '__doc__': 'Special value for options without a value.'})()
"""Special value for options without a value (see :doc:`intro`).

The truth value is ``True``.
"""

NOTFOUND = type('NotFound', (), {
    '__repr__': lambda x: '<NOTFOUND>',
    '__bool__': lambda x: False,
    '__doc__': 'Special value for options that are not '
               'found and have no default.'})()
"""Special value for options that are not found and have no default.

The truth value is ``False``.
"""


def _key(key):
    if isinstance(key, str):
        key = (None, key)
    return key


class Config:
    """Configuration class.

    An instance of this class is returned by the function :func:`configure`.

    If ``create_properties=True`` it will have a property for each configuration
    option named as explained in the :doc:`intro`. For extra data this is
    just the name given in the :meth:`add` method.

    Options can also be accessed like this: ``config[secname, optname]``.
    To check if an option exists, the ``in`` operator can be used:
    ``(secname, optname) in config``.

    For extra data either ``None`` must be used for the section name or only
    the name of the data, i.e. ``config[None, name]`` and ``config[name]`` are
    equivalent as are ``(None, name) in config`` and ``name in config``.

    When a :class:`Config` object is used as an iterator it yields 3-tuples
    for each option: ``(secname, optname, value)``.
    """

    def __init__(self, options, create_props, kwargs):
        self._options = {k: (v.name, v.ro) for k, v in options.items()}
        self._values = {k: v.value for k, v in options.items()}
        self._create_props = create_props
        self._kwargs = kwargs

    def __iter__(self):
        return ((sec, opt, self._values[sec, opt])
                for (sec, opt) in self._options)

    def __contains__(self, item):
        return _key(item) in self._options

    def __getitem__(self, key):
        return self._values[_key(key)]

    def __setitem__(self, key, value):
        key = _key(key)
        if self._options[key][1]:
            raise ReadonlyError(
                f'cannot set option {key[1]!r} in section {key[0]!r}')
        self._values[key] = value

    def __delitem__(self, key):
        key = _key(key)
        name = self._options[key][0]
        del self._options[key]
        del self._values[key]
        if name and hasattr(self.__class__, name):
            delattr(self.__class__, name)

    def add(self, key, value, readonly=True):
        """Add extra data to configuration or an option to a section.

        :param key: either a name of extra data or a tuple
                    ``('secname', 'optname')``
        :type: str or tuple
        :param value: the value of the data
        :param bool readonly: if ``True`` the data cannot be changed
        :raises DuplicateError: if an option already exists in a section
        :raises AttributeError: if an attribute with the same name already
                                exists (only if ``create_properties=True``)
        :raises ConfigError: if ``create_properties=True`` and ``name`` or
                             ``secname_optname`` is not a valid Python
                             identifier; the data can still be
                             accessed with ``cfg['name']`` or
                             ``cfg['secname', 'optname']``
        """
        key = _key(key)
        if key in self._options:
            raise DuplicateError(f'Key {key!r} already exists')
        if self._create_props:
            if key[0] is None:
                name = key[1]
            else:
                name = f'{key[0]}_{key[1]}'
        else:
            name = ''
        self._options[key] = (name if name.isidentifier() else None, readonly)
        self._values[key] = value
        if self._create_props:
            if not name.isidentifier():
                raise ConfigError(f'not a valid name: {name}')
            if hasattr(self.__class__, name):
                raise AttributeError(f'attribute {name!r} already exists')
            setattr(self.__class__, name, property(create_getter(key),
                    None if readonly
                    else create_setter(key), create_deleter(key)))

    def sections(self):
        """Return section names.

        :return: list with section names
        :rtype: list
        """
        lst = []
        seen = set()
        for sec, _ in self._options:
            if sec is None:
                continue
            if sec not in seen:
                lst.append(sec)
                seen.add(sec)
        return lst

    def options(self, section):
        """Return option names in the specified section.

        :param str section: a section name
        :return: list with option names
        :rtype: list
        """
        return list(opt for (sec, opt) in self._options
                    if sec == section and section is not None)

    def extras(self):
        """Return names of extra data added with :meth:`add`.

        :return: list with names of extra data
        :rtype: list
        """
        return list(opt for (sec, opt) in self._options if sec is None)

    def as_dict(self, section):
        """Return options and values in a section as a :class:`dict`.

        :param str section: a section name
        :return: mapping option names => values
        :rtype: dict
        """
        return {opt: val for sec, opt, val in self if sec == section}

    def write(self, file, space_around_delimiters=True):
        """Write a representation of the configuration to the specified file.

        Extra data added with :meth:`add` will be excluded.

        :param file: the file
        :type file: :term:`path-like object` or :term:`text file`
                    opened for writing
        :param bool space_around_delimiters: if ``True``, delimiters between
                                             keys and values are surrounded by
                                             spaces
        """
        d = {}
        for (sec, opt) in self._options:
            if sec is None:
                continue
            if sec not in d:
                d[sec] = {}
            value = self._values[sec, opt]
            if value is NOVALUE:
                d[sec][opt] = None
            elif value is not NOTFOUND:
                d[sec][opt] = str(value)
        self._kwargs['interpolation'] = None
        cp = ConfigParser(**self._kwargs)
        cp.read_dict(d)
        try:
            check_path_like(file)
            with open(file, 'w') as fh:
                cp.write(fh, space_around_delimiters=space_around_delimiters)
        except TypeError:
            cp.write(file, space_around_delimiters=space_around_delimiters)

    def debug_info(self):
        """Return an iterator for debugging.

        It yields 5-tuples ``(sec, opt, name, value, readonly)``
        for each option.
        """
        for key, (name, readonly) in self._options.items():
            yield (*key, name, self._values[key], readonly)
