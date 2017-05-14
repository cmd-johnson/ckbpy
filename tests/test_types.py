import ckbpy as ckb


def test_rgb_color():
    color = ckb.RGBColor(1, 2, 3)
    assert color.r == 1
    assert color.g == 2
    assert color.b == 3

    color.r = 10
    color.g = 20
    color.b = 30
    assert color.rgb == (10, 20, 30)

    color.rgb = (40, 50, 60)
    assert color.r == 40
    assert color.g == 50
    assert color.b == 60
    assert str(color) == '28323c'

    color = ckb.RGBColor.from_str('facade')
    assert color.rgb == (250, 202, 222)

    color = ckb.RGBColor.from_str('invalid')
    assert color is None


def test_argb_color():
    color = ckb.ARGBColor(1, 2, 3, 4)
    assert color.a == 1
    assert color.r == 2
    assert color.g == 3
    assert color.b == 4

    color.a = 0
    color.r = 10
    color.g = 20
    color.b = 30
    assert color.argb == (0, 10, 20, 30)

    color.argb = (40, 50, 60, 70)
    assert color.a == 40
    assert color.r == 50
    assert color.g == 60
    assert color.b == 70
    assert str(color) == '28323c46'

    color = ckb.ARGBColor.from_str('deadbeef')
    assert color.argb == (222, 173, 190, 239)

    color = ckb.ARGBColor.from_str('invalid')
    assert color is None


def test_gradient_color_stop():
    color_stops = ckb.GradientColorStops([
        (0, ckb.RGBColor.from_str('00ff00')),
        (100, ckb.RGBColor.from_str('ff0000'))
    ])
    assert color_stops.color_stops[0][0] == 0
    assert color_stops.color_stops[0][1].rgb == (0, 255, 0)
    assert color_stops.color_stops[1][0] == 100
    assert color_stops.color_stops[1][1].rgb == (255, 0, 0)

    color_stops = ckb.GradientColorStops.from_str('0:0000ff 50:ff00ff '
                                                  '100:ff0000')
    assert len(color_stops.color_stops) == 3
    assert color_stops.color_stops[0][0] == 0
    assert color_stops.color_stops[0][1].rgb == (0, 0, 255)
    assert color_stops.color_stops[1][0] == 50
    assert color_stops.color_stops[1][1].rgb == (255, 0, 255)
    assert color_stops.color_stops[2][0] == 100
    assert color_stops.color_stops[2][1].rgb == (255, 0, 0)

    color_stops = ckb.GradientColorStops.from_str('invalid')
    assert color_stops is None


def test_agradient_color_stop():
    color_stops = ckb.AGradientColorStops([
        (0, ckb.ARGBColor.from_str('0000ff00')),
        (100, ckb.ARGBColor.from_str('ffff0000'))
    ])
    assert color_stops.color_stops[0][0] == 0
    assert color_stops.color_stops[0][1].argb == (0, 0, 255, 0)
    assert color_stops.color_stops[1][0] == 100
    assert color_stops.color_stops[1][1].argb == (255, 255, 0, 0)

    color_stops = ckb.AGradientColorStops.from_str('0:000000ff 50:80ff00ff '
                                                   '100:ffff0000')
    assert len(color_stops.color_stops) == 3
    assert color_stops.color_stops[0][0] == 0
    assert color_stops.color_stops[0][1].argb == (0, 0, 0, 255)
    assert color_stops.color_stops[1][0] == 50
    assert color_stops.color_stops[1][1].argb == (128, 255, 0, 255)
    assert color_stops.color_stops[2][0] == 100
    assert color_stops.color_stops[2][1].argb == (255, 255, 0, 0)

    color_stops = ckb.AGradientColorStops.from_str('invalid')
    assert color_stops is None
