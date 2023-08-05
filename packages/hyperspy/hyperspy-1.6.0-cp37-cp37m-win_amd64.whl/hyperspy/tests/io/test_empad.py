
import os
import struct

import numpy as np
import numpy.testing as nt
import pytest
import traits.api as t

import hyperspy.api as hs

DATA_DIR = os.path.join(os.path.dirname(__file__), 'empad_data')
FILENAME_STACK_RAW = os.path.join(DATA_DIR, 'series_x10.raw')
FILENAME_MAP_RAW = os.path.join(DATA_DIR, 'scan_x4_y4.raw')


def _create_raw_data(filename, shape):
    size = np.prod(shape)
    data = np.arange(size).reshape(shape).astype('float32')
    data.tofile(filename)


def setup_module():
    _create_raw_data(FILENAME_STACK_RAW, (166400,))
    _create_raw_data(FILENAME_MAP_RAW, (4*4*130*128))


def teardown_module():
    if os.path.exists(FILENAME_STACK_RAW):
        os.remove(FILENAME_STACK_RAW)
    if os.path.exists(FILENAME_MAP_RAW):
        os.remove(FILENAME_MAP_RAW)


@pytest.mark.parametrize("lazy", (False, True))
def test_read_stack(lazy):
    s = hs.load(os.path.join(DATA_DIR, 'stack_images.xml'), lazy=lazy)
    assert s.data.dtype == 'float32'
    ref_data = np.arange(166400).reshape((10, 130, 128))[..., :128, :]
    nt.assert_allclose(s.data, ref_data.astype('float32'))
    signal_axes = s.axes_manager.signal_axes
    assert signal_axes[0].name == 'width'
    assert signal_axes[1].name == 'height'
    for axis in signal_axes:
        assert axis.units == t.Undefined
        assert axis.scale == 1.0
        assert axis.offset == -64
    navigation_axes = s.axes_manager.navigation_axes
    assert navigation_axes[0].name == 'series_count'
    assert navigation_axes[0].units == 'ms'
    assert navigation_axes[0].scale == 1.0
    assert navigation_axes[0].offset == 0.0

    assert s.metadata.General.date == '2019-06-07'
    assert s.metadata.General.time == '13:17:22.590279'
    assert s.metadata.Signal.signal_type == 'electron_diffraction'


@pytest.mark.skipif(8 * struct.calcsize("P") == 32,
                    reason="Not enough memory on appveyor x86.")
@pytest.mark.parametrize("lazy", (False, True))
def test_read_map(lazy):
    s = hs.load(os.path.join(DATA_DIR, 'map4x4.xml'), lazy=lazy)
    assert s.data.dtype == 'float32'
    ref_data = np.arange(266240).reshape((4, 4, 130, 128))[..., :128, :]
    nt.assert_allclose(s.data, ref_data.astype('float32'))
    signal_axes = s.axes_manager.signal_axes
    assert signal_axes[0].name == 'width'
    assert signal_axes[1].name == 'height'
    for axis in signal_axes:
        assert axis.units == '1/nm'
        nt.assert_allclose(axis.scale, 0.1826537)
        nt.assert_allclose(axis.offset, -11.689837)
    navigation_axes = s.axes_manager.navigation_axes
    assert navigation_axes[0].name == 'scan_y'
    assert navigation_axes[1].name == 'scan_x'
    for axis in navigation_axes:
        assert axis.units == 'µm'
        nt.assert_allclose(axis.scale, 1.1415856)
        nt.assert_allclose(axis.offset, 0.0)

    assert s.metadata.General.date == '2019-06-06'
    assert s.metadata.General.time == '13:30:00.164675'
    assert s.metadata.Signal.signal_type == 'electron_diffraction'
