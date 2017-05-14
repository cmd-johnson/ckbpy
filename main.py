#!/usr/bin/env python

import sys
import logging
import ckbpy.params as cp
import ckbpy.types as ct
from ckbpy.effect import Effect, Preset


class GradientEffect(Effect):
    def __init__(self):
        super(GradientEffect, self).__init__(
            guid='{3872d62d-b2cb-4fa0-9e6a-e7ed3149e247}',
            name='Python Test',
            version='0.0.0',
            year='2017',
            author='Jonas Auer <jonas.auer.94@gmail.com>',
            license='GPL-2.0',
            description='Description?',
            params=[
                cp.Long('long', '<', '>', 0, -2, 2),
                cp.Double('double', '<', '>', 0., -2., 2.),
                cp.Bool('bool', 'text'),
                cp.RGB('rgb', '<', '>'),
                cp.ARGB('argb', '<', '>'),
                cp.Gradient('gradient', '<', '>'),
                cp.AGradient('agradient', '<', '>'),
                cp.Angle('angle', '<', '>'),
                cp.String('string', '<', '>', 'asdf'),
                cp.Label('label1', 'doesn\'t do much now, does it.')
            ],
            presets=[Preset('GradientEffect?')]
        )

    def start(self):
        for key in self.keys:
            key.color = ct.ARGBColor(255, 255, 255, 0)

    def param_changed(self, name, value):
        logging.debug(self.param_values)


if __name__ == '__main__':
    logfile = 'debug.log'
    logging.basicConfig(
        filename=logfile,
        level=logging.DEBUG,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    )

    GradientEffect().run(sys.argv)
