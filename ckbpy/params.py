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

    def get_color_for_phase(self, phase):
        """Calculates the gradient's color for the given phase in [0.0,1.0]."""
        phase_percent = max(0, min(100, int(phase * 100)))
        color_stops = self.value.color_stops
        # If the phase is outside of the color_stop's bounds, there isn't much
        # calculation to do.
        if phase_percent <= color_stops[0][0]:
            return color_stops[0][1]
        if phase_percent >= color_stops[len(color_stops) - 1][0]:
            return color_stops[len(color_stops) - 1][1]

        # Find the color stops closest to the phase
        left = color_stops[0]
        right = color_stops[1]
        next_index = 2
        while not (left[0] <= phase_percent and right[0] >= phase_percent):
            left = right
            right = color_stops[next_index]
            next_index += 1

        # Interpolate linearly between the two color-stops
        right_share = (phase_percent - left[0]) / (right[0] - left[0])
        left_share = 1.0 - right_share
        return RGBColor(
            r=int(left[1].r * left_share + right[1].r * right_share),
            g=int(left[1].g * left_share + right[1].g * right_share),
            b=int(left[1].b * left_share + right[1].b * right_share)
        )

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

    def get_color_for_phase(self, phase):
        """Calculates the gradient's color for the given phase in [0.0,1.0]."""
        phase_percent = max(0.0, min(100.0, phase * 100))
        color_stops = self.value.color_stops
        # If the phase is outside of the color_stop's bounds, there isn't much
        # calculation to do.
        if phase_percent <= color_stops[0][0]:
            return color_stops[0][1]
        if phase_percent >= color_stops[len(color_stops) - 1][0]:
            return color_stops[len(color_stops) - 1][1]

        # Find the color stops closest to the phase
        left = color_stops[0]
        right = color_stops[1]
        next_index = 2
        while not (left[0] <= phase_percent and right[0] >= phase_percent):
            left = right
            right = color_stops[next_index]
            next_index += 1

        # Interpolate linearly between the two color-stops
        right_share = (phase_percent - left[0]) / (right[0] - left[0])
        left_share = 1.0 - right_share
        return ARGBColor(
            a=int(left[1].a * left_share + right[1].a * right_share),
            r=int(left[1].r * left_share + right[1].r * right_share),
            g=int(left[1].g * left_share + right[1].g * right_share),
            b=int(left[1].b * left_share + right[1].b * right_share)
        )

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
