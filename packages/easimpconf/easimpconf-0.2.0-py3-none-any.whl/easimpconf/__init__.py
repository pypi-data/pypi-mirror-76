"""Easy and simple configuration.

See also: :doc:`intro`
"""

import re
import types
from collections import namedtuple
from configparser import ConfigParser
from functools import lru_cache
from importlib.resources import read_text

from salmagundi.utils import check_path_like

from ._config import NOVALUE, NOTFOUND, Config
from ._errors import (Error, ConfigError, DuplicateError, ReadonlyError,
                      SpecError)
from ._spec import Spec
from ._utils import (convert_choice, convert_loglevel, convert_predicate,
                     convert_string, create_getter, create_setter,
                     create_deleter)

__version__ = read_text(__package__, 'VERSION').strip()

__all__ = ['NOTFOUND', 'NOVALUE', 'Config', 'ConfigError', 'DuplicateError',
           'Error', 'ReadonlyError', 'SpecError', 'configure',
           'convert_choice', 'convert_loglevel', 'convert_predicate',
           'convert_string']

_OptData = namedtuple('OptData', 'name, ro, value')


def _get_name(sec, opt, create_properties):
    if create_properties:
        name = f'{sec}_{opt}'
        if not name.isidentifier():
            raise SpecError(f'not a valid name: {name}')
    else:
        name = None
    return name


def _get_options(cp, sec, spec_opt, wildcard, has_wildcard):
    if has_wildcard:
        opts = []
        for opt in cp.options(sec):
            if re.fullmatch(spec_opt.replace(wildcard, '.*?'), opt):
                opts.append(opt)
        return opts
    else:
        return [spec_opt] if cp.has_option(sec, spec_opt) else []


def _with_spec(cp, create_properties, spec, kwargs):
    @lru_cache
    def get_sections(spec_sec, wildcard, has_wildcard):
        if has_wildcard:
            secs = []
            for sec in cp.sections():
                if re.fullmatch(spec_sec.replace(wildcard, '.*?'), sec):
                    secs.append(sec)
            return secs
        else:
            return [spec_sec] if spec_sec in cp else []

    options = {}
    for spec_sec, spec_opt in [(spec_sec, spec_opt) for spec_sec in spec.data
                               for spec_opt in spec.data[spec_sec]]:
        opt_spec = spec.data[spec_sec][spec_opt]
        secs = get_sections(spec_sec, spec.wildcard, opt_spec.sec_wildcard)
        if not secs:
            if not opt_spec.sec_wildcard:
                if opt_spec.required:
                    raise ConfigError(
                        f'missing required option {spec_opt!r} '
                        f'in section {spec_sec!r}')
                if not opt_spec.opt_wildcard:
                    value = opt_spec.default
                    name = _get_name(spec_sec, spec_opt, create_properties)
                    options[(spec_sec, spec_opt)] = _OptData(
                        name, opt_spec.flag is not False, value)
        else:
            for sec in secs:
                opts = _get_options(cp, sec, spec_opt, spec.wildcard,
                                    opt_spec.opt_wildcard)
                if not opts:
                    if opt_spec.required:
                        raise ConfigError(
                            f'missing required option {spec_opt!r} '
                            f'in section {sec!r}')
                    if not opt_spec.opt_wildcard:
                        value = opt_spec.default
                        name = _get_name(sec, spec_opt, create_properties)
                        options[(sec, spec_opt)] = _OptData(
                            name, opt_spec.flag is not False, value)
                else:
                    for opt in opts:
                        if opt_spec.flag is None:
                            raise ConfigError(
                                f'option {opt!r} in section {sec!r} is fixed')
                        value = cp.get(sec, opt, raw=opt_spec.raw)
                        if (value is None and
                                kwargs.get('allow_no_value', False)):
                            if opt_spec.converter is None:
                                value = NOVALUE
                            else:
                                raise ConfigError(
                                    f'option {opt!r} in section {sec!r} '
                                    'has no value')
                        else:
                            try:
                                value = opt_spec.converter(value)
                            except Exception as ex:
                                raise ConfigError(
                                    f'error converting value {value!r} for '
                                    f'option {opt!r} in section {sec!r} with '
                                    f'converter {opt_spec.conv_name!r}: {ex}')
                        name = _get_name(sec, opt, create_properties)
                        options[(sec, opt)] = _OptData(
                            name, opt_spec.flag is not False, value)
    get_sections.cache_clear()
    return options


def _without_spec(cp, create_properties, kwargs):
    options = {}
    for sec, opt in [(sec, opt)
                     for sec in cp.sections()
                     for opt in cp.options(sec)]:
        name = _get_name(sec, opt, create_properties)
        value = cp.get(sec, opt)
        if value is None and kwargs.get('allow_no_value', False):
            value = NOVALUE
        options[(sec, opt)] = _OptData(name, False, value)
    return options


def configure(conf, spec, *, create_properties=True, converters=None, **kwargs):
    """For an explanation see the :doc:`intro`.

    :param conf: the configuration
    :type conf: :term:`path-like object` or :term:`text file` opened for reading
                or :class:`~configparser.ConfigParser` object
    :param spec: the specification
    :type spec: :term:`path-like object` or :term:`text file` opened for reading
                or ``None``
    :param bool create_properties: if ``True`` properties will be created, else
                                   only item access with [sec,opt] can be used
    :param dict converters: same as the ``converters`` argument of
                            :class:`~configparser.ConfigParser`
                            but used directly by this function
    :param kwargs: arguments for the :class:`~configparser.ConfigParser`
                   (ignored if ``conf`` is a :class:`~configparser.ConfigParser`
                   object)
    :return: configuration object
    :rtype: Config
    :raises SpecError: if there is a problem with the specification
    :raises ConfigError: if there is a problem with the configuration
    :raises configparser.Error: from :class:`~configparser.ConfigParser`
    """
    if spec is not None:
        spec_data = Spec(spec, converters if converters else {})
    else:
        spec_data = None
    cp = ConfigParser(**kwargs)
    if spec_data:
        cp.read_dict(spec_data.defaults)
    if isinstance(conf, ConfigParser):
        cp.read_dict(conf)
    else:
        try:
            check_path_like(conf)
            with open(conf) as fh:
                cp.read_file(fh)
        except TypeError:
            cp.read_file(conf)
    if spec is None:
        options = _without_spec(cp, create_properties, kwargs)
    else:
        options = _with_spec(cp, create_properties, spec_data, kwargs)

    def cls_cb(ns):
        ns['__module__'] = __name__
        if create_properties:
            for key, data in options.items():
                ns[data.name] = property(create_getter(key),
                                         None if data.ro
                                         else create_setter(key),
                                         create_deleter(key))

    C = types.new_class('Config', (Config,), {}, cls_cb)
    return C(options, create_properties, kwargs)
