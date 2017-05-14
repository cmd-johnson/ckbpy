import ckbpy as ckb


def test_default_effect_info(capsys):
    effect = ckb.Effect(guid='{9c1c97d5-c2e1-45a7-aba1-b059cfe9a0f6}',
                        name='Test',
                        version='1.0.0',
                        year='2017',
                        author='Test',
                        license='MIT')
    effect.run(['', '--ckb-info'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '\n'.join([
        'guid %7B9c1c97d5-c2e1-45a7-aba1-b059cfe9a0f6%7D',
        'name Test',
        'version 1.0.0',
        'year 2017',
        'author Test',
        'license MIT',
        'description ',
        'kpmode name',
        'time duration',
        'repeat off',
        'preempt off',
        'parammode live',
        'preset Test ',
        ''
    ])


def test_configured_effect_info(capsys):
    params = [
        ckb.Long('LONG', 'pre', 'post', 0, -1, 1),
        ckb.Double('DOUBLE', 'pre', 'post', 0.0, -1.0, 1.0),
        ckb.Bool('BOOL', 'text', True),
        ckb.RGB('RGB', 'pre', 'post', ckb.RGBColor.from_str('facade')),
        ckb.ARGB('ARGB', 'pre', 'post', ckb.ARGBColor.from_str('deadbeef')),
        ckb.Gradient('GRADIENT', 'pre', 'post',
                     ckb.GradientColorStops.from_str('0:000000 100:facade')),
        ckb.AGradient('AGRADIENT', 'pre', 'post',
                      ckb.AGradientColorStops.from_str('0:00000000 '
                                                       '100:deadbeef')),
        ckb.Angle('ANGLE', 'pre', 'post', 137),
        ckb.String('STRING', 'pre', 'post', 'ckb-next is awesome.'),
        ckb.Label('LABEL', 'text')
    ]

    presets = [
        ckb.Preset('test1', {'LONG': 1, 'BOOL': False}),
        ckb.Preset('test2', {'LONG': -1, 'BOOL': True}),
    ]

    effect = ckb.Effect(guid='{9c1c97d5-c2e1-45a7-aba1-b059cfe9a0f6}',
                        name='Test',
                        version='1.0.0',
                        year='2017',
                        author='Test',
                        license='MIT',
                        description='Some fancy description!',
                        kpmode=ckb.Keypress.POSITION,
                        time=ckb.Time.ABSOLUTE,
                        repeat=True,
                        preempt=True,
                        live_params=False,
                        params=params,
                        presets=presets)
    effect.run(['', '--ckb-info'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '\n'.join([
        'guid %7B9c1c97d5-c2e1-45a7-aba1-b059cfe9a0f6%7D',
        'name Test',
        'version 1.0.0',
        'year 2017',
        'author Test',
        'license MIT',
        'description Some%20fancy%20description%21',
        'kpmode position',
        'time absolute',
        'repeat on',
        'preempt on',
        'parammode static',
        'param long LONG pre post 0 -1 1',
        'param double DOUBLE pre post 0.0 -1.0 1.0',
        'param bool BOOL text  1',
        'param rgb RGB pre post facade',
        'param argb ARGB pre post deadbeef',
        'param gradient GRADIENT pre post 0%3A000000%20100%3Afacade',
        'param agradient AGRADIENT pre post 0%3A00000000%20100%3Adeadbeef',
        'param angle ANGLE pre post 137',
        'param string STRING pre post ckb-next%20is%20awesome.',
        'param label LABEL text ',
        'preset test1 LONG=1 BOOL=0',
        'preset test2 LONG=-1 BOOL=1',
        ''
    ])
