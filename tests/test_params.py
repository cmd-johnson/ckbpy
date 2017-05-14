import ckbpy as ckb


def test_long():
    param = ckb.Long('LONG', '<', '>', 0, -1, 1)
    assert param.param_string == 'long LONG %3C %3E 0 -1 1'
    assert param.value == 0

    param.set_value_from_str('1')
    assert param.value == 1


def test_double():
    param = ckb.Double('DOUBLE', '<', '>', 0.0, -1.0, 1.0)
    assert param.param_string == 'double DOUBLE %3C %3E 0.0 -1.0 1.0'
    assert param.value == 0.0

    param.set_value_from_str('1')
    assert param.value == 1.0


def test_bool():
    param = ckb.Bool('BOOL', 'text', False)
    assert param.param_string == 'bool BOOL text  0'
    assert not param.value

    param.set_value_from_str('1')
    assert param.value


def test_rgb():
    param = ckb.RGB('RGB', '<', '>', ckb.RGBColor(15, 31, 47))
    assert param.param_string == 'rgb RGB %3C %3E 0f1f2f'

    param.set_value_from_str('facade')
    assert param.value.rgb == (250, 202, 222)


def test_argb():
    param = ckb.ARGB('ARGB', '<', '>', ckb.ARGBColor(113, 254, 176, 167))
    assert param.param_string == 'argb ARGB %3C %3E 71feb0a7'

    param.set_value_from_str('5ab07a9e')
    assert param.value.argb == (90, 176, 122, 158)


def test_gradient(capsys):
    param = ckb.Gradient('GRADIENT', '<', '>', ckb.GradientColorStops([
        (0, ckb.RGBColor(255, 0, 0)),
        (100, ckb.RGBColor(0, 255, 0))
    ]))
    assert param.param_string == ('gradient GRADIENT %3C %3E '
                                  '0%3Aff0000%20100%3A00ff00')

    param.set_value_from_str('10:7e57ed 50:70a575 90:7001ed')
    assert len(param.value.color_stops) == 3
    assert param.value.color_stops[0][0] == 10
    assert param.value.color_stops[0][1].rgb == (126, 87, 237)
    assert param.value.color_stops[1][0] == 50
    assert param.value.color_stops[1][1].rgb == (112, 165, 117)
    assert param.value.color_stops[2][0] == 90
    assert param.value.color_stops[2][1].rgb == (112, 1, 237)

    color = param.get_color_for_phase(0.0)
    assert color.rgb == (126, 87, 237)

    color = param.get_color_for_phase(1.0)
    assert color.rgb == (112, 1, 237)

    color = param.get_color_for_phase(0.3)
    assert color.rgb == (119, 126, 177)

    color = param.get_color_for_phase(0.7)
    assert color.rgb == (112, 83, 177)


def test_agradient(capsys):
    param = ckb.AGradient('AGRADIENT', '<', '>', ckb.AGradientColorStops([
        (0, ckb.ARGBColor(0, 255, 0, 0)),
        (100, ckb.ARGBColor(255, 0, 255, 0))
    ]))
    assert param.param_string == ('agradient AGRADIENT %3C %3E '
                                  '0%3A00ff0000%20100%3Aff00ff00')

    param.set_value_from_str('10:be51e9ed 50:e5ca1a7e 90:90d2177a')
    assert len(param.value.color_stops) == 3
    assert param.value.color_stops[0][0] == 10
    assert param.value.color_stops[0][1].argb == (190, 81, 233, 237)
    assert param.value.color_stops[1][0] == 50
    assert param.value.color_stops[1][1].argb == (229, 202, 26, 126)
    assert param.value.color_stops[2][0] == 90
    assert param.value.color_stops[2][1].argb == (144, 210, 23, 122)

    color = param.get_color_for_phase(0.0)
    assert color.argb == (190, 81, 233, 237)

    color = param.get_color_for_phase(1.0)
    assert color.argb == (144, 210, 23, 122)

    color = param.get_color_for_phase(0.3)
    assert color.argb == (209, 141, 129, 181)

    color = param.get_color_for_phase(0.7)
    assert color.argb == (186, 206, 24, 124)


def test_angle():
    param = ckb.Angle('ANGLE', '<', '>', 137)
    assert param.param_string == 'angle ANGLE %3C %3E 137'
    assert param.value == 137

    param.set_value_from_str('42')
    assert param.value == 42


def test_string():
    param = ckb.String('STRING', '<', '>', 'default string')
    assert param.param_string == 'string STRING %3C %3E default%20string'
    assert param.value == 'default string'

    param.set_value_from_str('some other value')
    assert param.value == 'some other value'
