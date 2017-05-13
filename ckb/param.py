from abc import abstractmethod
from urllib.parse import quote
from ckb.types import RGBColor, ARGBColor, GradientColorStops


class Param(object):
    def __init__(self, type_name, param_name):
        self.type = type_name
        self.name = quote(param_name)

    def __str__(self):
        params = self.format_params()
        return f'{self.type} {self.name} {params}'

    @abstractmethod
    def format_params(self): pass


class Long(Param):
    def __init__(self, name, prefix='', postfix='',
                 default_value=0, min_value=0, max_value=0):
        super(Long, self).__init__('long', name)
        self.prefix = quote(prefix)
        self.postfix = quote(postfix)
        self.default_value = default_value
        self.min = min_value
        self.max = max_value

    def format_params(self):
        return (f'{self.prefix} {self.postfix} '
                f'{self.default_value} {self.min} {self.max}')


class Double(Param):
    def __init__(self, name, prefix='', postfix='',
                 default_value=0.0, min_value=0.0, max_value=0.0):
        super(Double, self).__init__('double', name)
        self.prefix = quote(prefix)
        self.postfix = quote(postfix)
        self.default_value = default_value
        self.min = min_value
        self.max = max_value

    def format_params(self):
        return (f'{self.prefix} {self.postfix} '
                f'{self.default_value} {self.min} {self.max}')


class Bool(Param):
    def __init__(self, name, text='', default_value=False):
        super(Bool, self).__init__('bool', name)
        self.text = quote(text)
        self.default_value = default_value

    def format_params(self):
        default = '1' if self.default_value else '0'
        return (f'{self.text}  {default}')


class RGB(Param):
    def __init__(self, name, prefix='', postfix='', color=RGBColor()):
        super(RGB, self).__init__('rgb', name)
        self.prefix = quote(prefix)
        self.postfix = quote(postfix)
        self.color = color

    def format_params(self):
        return f'{self.prefix} {self.postfix} {self.color}'


class ARGB(Param):
    def __init__(self, name, prefix='', postfix='', color=ARGBColor()):
        super(ARGB, self).__init__('argb', name)
        self.prefix = quote(prefix)
        self.postfix = quote(postfix)
        self.color = color

    def format_params(self):
        return f'{self.prefix} {self.postfix} {self.color}'


class Gradient(Param):
    def __init__(self, name, prefix='', postfix='',
                 color_stops=GradientColorStops()):
        super(Gradient, self).__init__('gradient', name)
        self.prefix = quote(prefix)
        self.postfix = quote(postfix)
        self.color_stops = color_stops

    def format_params(self):
        return f'{self.prefix} {self.postfix} {self.color_stops}'


class AGradient(Param):
    def __init__(self, name, prefix='', postfix='',
                 color_stops=GradientColorStops()):
        super(AGradient, self).__init__('agradient', name)
        self.prefix = quote(prefix)
        self.postfix = quote(postfix)
        self.color_stops = color_stops

    def format_params(self):
        return f'{self.prefix} {self.postfix} {self.color_stops}'


class Angle(Param):
    def __init__(self, name, prefix='', postfix='', default_value=0):
        super(Angle, self).__init__('angle', name)
        self.prefix = quote(prefix)
        self.postfix = quote(postfix)
        self.default_value = default_value

    def format_params(self):
        return f'{self.prefix} {self.postfix} {self.default_value}'


class String(Param):
    def __init__(self, name, prefix='', postfix='', default_value=''):
        super(String, self).__init__('string', name)
        self.prefix = prefix
        self.postfix = postfix
        self.default_value = default_value

    def format_params(self):
        return f'{self.prefix} {self.postfix} {self.default_value}'


class Label(Param):
    def __init__(self, name, text):
        super(Label, self).__init__('label', name)
        self.text = quote(text)

    def format_params(self):
        return self.text
