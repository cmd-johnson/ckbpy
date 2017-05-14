import re
import logging
from urllib import parse
from .types import ARGBColor


class Key(object):
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.color = ARGBColor()


class Preset(object):
    def __init__(self, title, values={}):
        self.title = title
        self.values = values

    def __str__(self):
        params = ' '.join([f'{k}={v}' for k, v in self.values])
        return f'{self.title} {params}'


class Effect(object):
    def __init__(self, guid, name, version, year, author, license,
                 description='', kpmode='none', time='duration', repeat=False,
                 preempt=False, parammode='live', params=[], presets=[]):
        self.guid = guid
        self.name = parse.quote(name)
        self.version = parse.quote(version)
        self.year = parse.quote(year)
        self.author = parse.quote(author)
        self.license = parse.quote(license)
        self.description = parse.quote(description)
        self.kpmode = kpmode
        self.time = time
        self.repeat = repeat
        self.preempt = preempt
        self.parammode = parammode
        self.params = dict((p.name, p) for p in params)
        self.presets = presets

        self.keys = []

    def run(self, argv):
        logging.debug(f'starting effect with {argv}')
        if len(argv) == 2:
            try:
                if argv[1] == '--ckb-info':
                    self.print_info()
                    return
                elif argv[1] == '--ckb-run':
                    self.main()
                    return
            except Exception:
                logging.exception('An unexpected exception occurred')

        print('This program must be run from within ckb')
        exit(-1)

    def print_info(self):
        info = [
            f'guid {self.guid}',
            f'name {self.name}',
            f'version {self.version}',
            f'year {self.year}',
            f'author {self.author}',
            f'license {self.license}',
            f'description {self.description}',
            f'kpmode {self.kpmode}',
            f'time {self.time}',
            'repeat ' + ('on' if self.repeat else 'off'),
            'preempt ' + ('on' if self.preempt else 'off'),
            f'parammode {self.parammode}'
        ]
        info.extend([f'param {p.param_string}' for p in self.params.values()])
        info.extend([f'preset {p}' for p in self.presets])
        print('\n'.join(info))

    def main(self):
        self.keys = self.read_keymap()

        self.skip_until('begin params')
        self.read_param_values()

        self.skip_until('begin run')
        print('begin run')

        # Main loop
        while True:
            line = input()
            if line == 'end run':
                break
            elif line == 'start':
                self.start()
            elif line == 'stop':
                self.stop()
            elif line == 'begin params':
                self.read_param_values()
            elif line.startswith('key'):
                self.read_key(line)
            elif line == 'frame':
                self.print_frame()
            elif line.startswith('time'):
                self.advance_time(line)

        print('end run')

    def skip_until(self, string):
        try:
            while input() != string:
                pass
        except EOFError:
            print(f'Error [ckb-python]: Reached EOF looking for "{string}"')
            exit(-2)

    def read_keymap(self):
        self.skip_until('begin keymap')

        match = re.search(r'^keycount ([\d]+)', input())
        if match is None:
            print('Error [ckb-python]: "begin keymap" not followed by '
                  '"keycount"')
            exit(-3)

        keycount = int(match.group(1))
        keys = []
        while keycount > 0:
            match = re.search(r'^key (\w+) (\d+),(\d+)', input())
            if match is None:
                continue
            key_name = match.group(1)
            key_x = int(match.group(2))
            key_y = int(match.group(3))
            keys.append(Key(key_name, key_x, key_y))
            keycount -= 1

        self.skip_until('end keymap')
        return keys

    def read_param_values(self):
        try:
            while True:
                line = input()
                if line == 'end params':
                    break

                match = re.search(r'^param (\w+) (.+)', line)
                if match is None:
                    continue

                param_name = match.group(1)
                if param_name not in self.params:
                    continue

                param = self.params[param_name]

                value_str = match.group(2)
                param.set_value_from_str(value_str)
                self.param_changed(param)
        except EOFError:
            print('Error [ckb-python]: Reached EOF reading parameters')
            exit(-2)

    def read_key(self, line):
        match = re.search(r'^key (?:(\d+),(\d+)|(\w+)) (down|up)', line)
        if match is None:
            return

        key = None
        if match.group(1):
            x = int(match.group(1))
            y = int(match.group(2))
            key = next((k for k in self.keys if k.x == x and k.y == y), None)
        else:
            name = match.group(3)
            key = next((k for k in self.keys if k.name == name), None)

        if key is not None:
            state = match.group(3) == 'down'
            self.keypress(key, state)

    def print_frame(self):
        print('begin frame')
        for key in self.keys:
            print(f'argb {key.name} {key.color}')
        print('end frame')

    def param_changed(self, param): pass

    def keypress(self, key, state): pass

    def advance_time(self, delta_t): pass

    def start(self): pass

    def stop(self): pass
