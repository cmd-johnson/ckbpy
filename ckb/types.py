import re


class RGBColor:
    def __init__(self, r=0, g=0, b=0):
        self.rgb = (r, g, b)

    @staticmethod
    def from_str(string):
        match = re.findall(r'[0-9a-f]{2}', string)
        if match is None or len(match) != 3:
            return None
        return RGBColor(*[int(val, 16) for val in match])

    def __str__(self):
        return ''.join([f'{e:02x}' for e in self.rgb])


class ARGBColor:
    def __init__(self, a=0, r=0, g=0, b=0):
        self.argb = (a, r, g, b)

    @staticmethod
    def from_str(string):
        match = re.findall(r'[0-9a-f]{2}', string)
        if match is None or len(match) != 4:
            return None
        return ARGBColor(*[int(val, 16) for val in match])

    def __str__(self):
        return ''.join([f'{e:02x}' for e in self.argb])


class GradientColorStops:
    def __init__(self, color_stops=[]):
        self.color_stops = color_stops

    @staticmethod
    def from_str(string):
        def parse_color_stop(stop):
            match = re.search(r'\d+:[0-9a-f]{2}', string)
            if match is None:
                return None
            return (int(match.group(1)), RGBColor.from_str(match.group(2)))
        stops = string.split(' ')
        return [s for s in map(parse_color_stop, stops) if s is not None]

    def __str__(self):
        return ' '.join([f'{p}:{c}' for (p, c) in self.color_stops])


class AGradientColorStops:
    def __init__(self, color_stops=[]):
        self.color_stops = color_stops

    @staticmethod
    def from_str(string):
        def parse_color_stop(stop):
            match = re.search(r'\d+:[0-9a-f]{2}', string)
            if match is None:
                return None
            return (int(match.group(1)), ARGBColor.from_str(match.group(2)))
        stops = string.split(' ')
        return [s for s in map(parse_color_stop, stops) if s is not None]

    def __str__(self):
        return ' '.join([f'{p}:{c}' for (p, c) in self.color_stops])
