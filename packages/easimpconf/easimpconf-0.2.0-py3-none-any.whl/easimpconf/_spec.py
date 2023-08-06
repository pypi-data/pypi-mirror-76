"""Spec module."""

from collections import namedtuple
from configparser import ConfigParser

from salmagundi.strings import str2bool, str2tuple
from salmagundi.utils import check_path_like

from ._config import NOTFOUND
from ._errors import SpecError

__all__ = ['Spec']

_CONFIGSPEC = '_configspec_'
_CONVERTERS = {'str': str, 'int': int, 'float': float, 'bool': str2bool}

_OptSpec = namedtuple('OptSpec', 'converter, conv_name,'
                      'required, flag, raw, default,'
                      'sec_wildcard, opt_wildcard')


class Spec:
    """Specification class."""

    def __init__(self, spec, convs):  # noqa: C901
        converters = _CONVERTERS.copy()
        converters.update(convs)
        cp = ConfigParser(interpolation=None)
        try:
            check_path_like(spec)
            with open(spec) as fh:
                cp.read_file(fh)
        except TypeError:
            cp.read_file(spec)
        readonly = cp.getboolean(_CONFIGSPEC, 'readonly', fallback=True)
        separator = cp.get(_CONFIGSPEC, 'separator', fallback=';')
        wildcard = cp.get(_CONFIGSPEC, 'wildcard', fallback=None)
        noval_tag = cp.get(_CONFIGSPEC, 'novalue', fallback=':novalue:')
        empty_tag = cp.get(_CONFIGSPEC, 'empty', fallback=':empty:')
        none_tag = cp.get(_CONFIGSPEC, 'none', fallback=':none:')
        req_tag = cp.get(_CONFIGSPEC, 'req_tag', fallback=':req:')
        ro_tag = cp.get(_CONFIGSPEC, 'ro_tag', fallback=':ro:')
        rw_tag = cp.get(_CONFIGSPEC, 'rw_tag', fallback=':rw:')
        fix_tag = cp.get(_CONFIGSPEC, 'fix_tag', fallback=':fix:')
        raw_tag = cp.get(_CONFIGSPEC, 'raw_tag', fallback=':raw:')
        cp.remove_section(_CONFIGSPEC)
        converters[noval_tag] = None
        specs = {}
        defaults = {}
        for sec in cp.sections():
            specs[sec] = {}
            if not wildcard or wildcard not in sec:
                defaults[sec] = {}
            for opt in cp.options(sec):
                t = str2tuple(cp.get(sec, opt), sep=separator)
                conv = t[0]
                if not conv:
                    raise SpecError(
                        f'missing spec for option {opt!r} in section {sec!r}')
                try:
                    converter = converters[conv]
                except KeyError:
                    raise SpecError(
                        f'unknown converter for option {opt!r} in '
                        f'section {sec!r}: {conv}')
                req = req_tag in t
                ro = ro_tag in t
                rw = rw_tag in t
                fix = fix_tag in t
                if ro + rw + fix > 1:
                    raise SpecError(
                        f'option {opt!r} in section {sec!r}: only one of '
                        f' {ro_tag!r}, {rw_tag!r}, {fix_tag!r} allowed')
                raw = raw_tag in t
                for s in t[1:]:
                    if s not in (req_tag, ro_tag, rw_tag, fix_tag, raw_tag):
                        if req:
                            raise SpecError(
                                f'option {opt!r} in section {sec!r} has a '
                                f'default value and a {req_tag!r} tag '
                                '(only one allowed)')
                        if s == empty_tag:
                            s = ''
                        try:
                            if converter is None:
                                raise SpecError(
                                    f'no default value allowed for {conv!r} '
                                    f'for option {opt!r} in section {sec!r}')
                            if s == none_tag:
                                default = None
                            else:
                                default = converter(s)
                        except Exception as ex:
                            raise SpecError(
                                f'error converting default value {s!r} for '
                                f'option {opt!r} in section {sec!r} '
                                f'with converter {conv!r}: {ex}')
                        break
                else:
                    if fix:
                        raise SpecError(
                            f'option {opt!r} in section {sec!r} uses '
                            f'{fix_tag!r} without a default value')
                    default = NOTFOUND
                if default is not NOTFOUND and wildcard and wildcard in opt:
                    raise SpecError(
                        f'option {opt!r} in section {sec!r} has wildcard '
                        'and default value')
                if fix:
                    flag = None
                else:
                    flag = ro or (readonly and not rw)
                specs[sec][opt] = _OptSpec(converter, conv, req,
                                           flag, raw, default,
                                           wildcard and wildcard in sec,
                                           wildcard and wildcard in opt)
                if sec in defaults and not fix and default is not NOTFOUND:
                    defaults[sec][opt] = default
        self._data = specs
        self._wildcard = wildcard
        self._defaults = defaults

    @property
    def data(self):
        """Return specification data."""
        return self._data

    @property
    def wildcard(self):
        """Return wildcard character(s)."""
        return self._wildcard

    @property
    def defaults(self):
        """Return default option values."""
        return self._defaults
