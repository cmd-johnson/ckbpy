#!/usr/bin/env python

import sys
import logging
import ckbpy as ckb


class GradientEffect(ckb.Effect):
    def __init__(self):
        super(ckb.GradientEffect, self).__init__(
            guid='{3872d62d-b2cb-4fa0-9e6a-e7ed3149e247}',
            name='Python Test',
            version='0.0.0',
            year='2017',
            author='Jonas Auer <jonas.auer.94@gmail.com>',
            license='GPL-2.0',
            description='Description?',
            params=[
                ckb.Long('long', '<', '>', 0, -2, 2),
                ckb.Double('double', '<', '>', 0., -2., 2.),
                ckb.Bool('bool', 'text'),
                ckb.RGB('rgb', '<', '>'),
                ckb.ARGB('argb', '<', '>'),
                ckb.Gradient('gradient', '<', '>'),
                ckb.AGradient('agradient', '<', '>'),
                ckb.Angle('angle', '<', '>'),
                ckb.String('string', '<', '>', 'asdf'),
                ckb.Label('label1', 'doesn\'t do much now, does it.')
            ],
            presets=[ckb.Preset('GradientEffect?')]
        )

    def start(self):
        for key in self.keys:
            key.color = ckb.ARGBColor(255, 255, 255, 0)

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
