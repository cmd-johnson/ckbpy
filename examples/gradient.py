#!/usr/bin/env python
import sys
import ckbpy as ckb


class Animation:
    def __init__(self, target=0.0, phase=0.0):
        self.target = target
        self.phase = phase


class GradientEffect(ckb.Effect):
    def __init__(self):
        default_gradient = ckb.AGradientColorStops([(0, 'ffffffff')])
        params = [ckb.AGradient("gradient", "Gradient:",
                                default_value=default_gradient)]

        presets = [
            ckb.Preset('Fade in', {
                'gradient': ckb.AGradientColorStops([
                    (0,   ckb.ARGBColor.from_str('00000000')),
                    (100, ckb.ARGBColor.from_str('ffffffff'))
                ]),
                'duration': 1.0,
                'stop': 0,
                'kpstop': 0
            }),
            ckb.Preset('Rainbow', {
                'gradient': ckb.AGradientColorStops([
                    (0,   ckb.ARGBColor.from_str('ffff0000')),
                    (17,  ckb.ARGBColor.from_str('ffffff00')),
                    (33,  ckb.ARGBColor.from_str('ff00ff00')),
                    (50,  ckb.ARGBColor.from_str('ff00ffff')),
                    (67,  ckb.ARGBColor.from_str('ff0000ff')),
                    (83,  ckb.ARGBColor.from_str('ffff00ff')),
                    (100, ckb.ARGBColor.from_str('ffff0000'))
                ]),
                'duration': 2.0
            })
        ]

        super().__init__(guid='{62909e5a-5f3e-4720-8638-f89c32367fd1}',
                         name='Python Gradient',
                         version='0.0.0',
                         year='2017',
                         author='Jonas Auer',
                         license='MIT',
                         description='Transition between two colours',
                         params=params,
                         presets=presets)
        self.animations = {}

    def keypress(self, key, state):
        anim = self.animations.get(key.name, Animation())
        # Play gradient forwards if the key was pressed; backwards otherwise.
        anim.target = 1.0 if state else 0.0
        self.animations[key.name] = anim

    def advance_time(self, delta_t):
        finished_animations = []
        for key_name, animation in self.animations.items():
            if animation.target < animation.phase:
                animation.phase = max(0, animation.phase - delta_t)
            elif animation.target > animation.phase:
                animation.phase = min(1, animation.phase + delta_t)
            elif animation.target == 0.0:
                finished_animations.append(key_name)
        for key in finished_animations:
            del self.animations[key]

    def update_colors(self):
        gradient = self.params['gradient']
        for key_name, animation in self.animations.items():
            key_color = gradient.get_color_for_phase(animation.phase)
            self.keys[key_name].color = key_color


if __name__ == '__main__':
    GradientEffect().run(sys.argv)
