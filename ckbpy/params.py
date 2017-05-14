from abc import ABC, abstractmethod
from urllib.parse import quote
from .types import (RGBColor, ARGBColor,
                    GradientColorStops, AGradientColorStops)


class Param(ABC):
    def __init__(self, type_name, param_name):
        self.type = type_name
        self.name = param_name

    @property
    def param_string(self):
        """Parameter-definition-string for sending to ckb."""
        params = self.format_params()
        return f'{self.type} {quote(self.name)} {params}'

    @abstractmethod
    def format_params(self):
        """Formats the parameter-definition's tail."""


class ValueParam(Param):
    def __init__(self, type_name, param_name, default_value):
        super().__init__(type_name, param_name)
        self.value = self.default_value = default_value

    @abstractmethod
    def set_value_from_str(self, string):
        """Sets the property's value from a string given by ckb."""


class Long(ValueParam):
    def __init__(self, name, prefix='', postfix='',
                 default_value=0, min_value=0, max_value=0):
        super().__init__('long', name, default_value)
        self.prefix = prefix
        self.postfix = postfix
        self.min = min_value
        self.max = max_value

    def set_value_from_str(self, string):
        """Sets the property's value from a string given by ckb."""
        self.value = int(string)

    def format_params(self):
        return (f'{quote(self.prefix)} {quote(self.postfix)} '
                f'{self.default_value} {self.min} {self.max}')


class Double(ValueParam):
    def __init__(self, name, prefix='', postfix='',
                 default_value=0.0, min_value=0.0, max_value=0.0):
        super().__init__('double', name, default_value)
        self.prefix = prefix
        self.postfix = postfix
        self.min = min_value
        self.max = max_value

    def set_value_from_str(self, string):
        """Sets the property's value from a string given by ckb."""
        self.value = float(string)

    def format_params(self):
        return (f'{quote(self.prefix)} {quote(self.postfix)} '
                f'{self.default_value} {self.min} {self.max}')


class Bool(ValueParam):
    def __init__(self, name, text='', default_value=False):
        super().__init__('bool', name, default_value)
        self.text = text

    def set_value_from_str(self, string):
        """Sets the property's value from a string given by ckb."""
        self.value = string == '1'

    def format_params(self):
        default = '1' if self.default_value else '0'
        return (f'{quote(self.text)}  {default}')


class RGB(ValueParam):
    def __init__(self, name, prefix='', postfix='', default_value=RGBColor()):
        super().__init__('rgb', name, default_value)
        self.prefix = prefix
        self.postfix = postfix

    def set_value_from_str(self, string):
        """Sets the property's value from a string given by ckb."""
        self.value = RGBColor.from_str(string)

    def format_params(self):
        return (f'{quote(self.prefix)} {quote(self.postfix)} '
                f'{self.default_value}')


class ARGB(ValueParam):
    def __init__(self, name, prefix='', postfix='', default_value=ARGBColor()):
        super().__init__('argb', name, default_value)
        self.prefix = prefix
        self.postfix = postfix

    def set_value_from_str(self, string):
        """Sets the property's value from a string given by ckb."""
        self.value = ARGBColor.from_str(string)

    def format_params(self):
        return (f'{quote(self.prefix)} {quote(self.postfix)} '
                f'{self.default_value}')


class Gradient(ValueParam):
    def __init__(self, name, prefix='', postfix='',
                 default_value=GradientColorStops()):
        super().__init__('gradient', name, default_value)
        self.prefix = prefix
        self.postfix = postfix

    def set_value_from_str(self, string):
        """Sets the property's value from a string given by ckb."""
        self.value = GradientColorStops.from_str(string)

    def format_params(self):
        return (f'{quote(self.prefix)} {quote(self.postfix)} '
                f'{quote(str(self.default_value))}')


class AGradient(ValueParam):
    def __init__(self, name, prefix='', postfix='',
                 default_value=AGradientColorStops()):
        super().__init__('agradient', name, default_value)
        self.prefix = prefix
        self.postfix = postfix

    def set_value_from_str(self, string):
        """Sets the property's value from a string given by ckb."""
        self.value = AGradientColorStops.from_str(string)

    def format_params(self):
        return (f'{quote(self.prefix)} {quote(self.postfix)} '
                f'{quote(str(self.default_value))}')


class Angle(ValueParam):
    def __init__(self, name, prefix='', postfix='', default_value=0):
        super().__init__('angle', name, default_value)
        self.prefix = prefix
        self.postfix = postfix

    def set_value_from_str(self, string):
        """Sets the property's value from a string given by ckb."""
        self.value = int(string)

    def format_params(self):
        return (f'{quote(self.prefix)} {quote(self.postfix)} '
                f'{self.default_value}')


class String(ValueParam):
    def __init__(self, name, prefix='', postfix='', default_value=''):
        super().__init__('string', name, default_value)
        self.prefix = prefix
        self.postfix = postfix

    def set_value_from_str(self, string):
        """Sets the property's value from a string given by ckb."""
        self.value = string

    def format_params(self):
        return (f'{quote(self.prefix)} {quote(self.postfix)} '
                f'{quote(self.default_value)}')


class Label(Param):
    def __init__(self, name, text):
        super().__init__('label', name)
        self.text = text

    def format_params(self):
        return quote(self.text)
