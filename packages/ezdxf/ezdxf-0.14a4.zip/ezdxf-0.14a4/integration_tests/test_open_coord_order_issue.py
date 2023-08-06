# Copyright (c) 2018-2019, Manfred Moitzi
# License: MIT License
import os
import pytest
import ezdxf


BASEDIR = 'integration_tests' if os.path.exists('integration_tests') else '.'
DATADIR = 'data'


@pytest.fixture(params=['AC1003_LINE_Example.dxf'])
def filename(request):
    filename = os.path.join(BASEDIR, DATADIR, request.param)
    if not os.path.exists(filename):
        pytest.skip('File {} not found.'.format(filename))
    return filename


def test_coordinate_order_problem(filename):
    try:
        dwg = ezdxf.readfile(filename, legacy_mode=True)
    except ezdxf.DXFError as e:
        pytest.fail(str(e))
    else:
        msp = dwg.modelspace()
        lines = msp.query('LINE')
        assert lines[0].dxf.start == (1.5, 0, 0)
