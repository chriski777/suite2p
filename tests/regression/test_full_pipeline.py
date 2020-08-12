"""
Class that tests common use cases for pipeline.
"""

from suite2p import io
from pathlib import Path
import numpy as np
import suite2p
import utils


def get_outputs_to_check(n_channels):
    outputs_to_check = ['F', 'Fneu', 'iscell', 'spks', 'stat']
    if n_channels == 2:
        outputs_to_check.extend(['F_chan2', 'Fneu_chan2'])
    return outputs_to_check


def test_2plane_2chan_with_batches(test_ops):
    """
    Tests for case with 2 planes and 2 channels with multiple batches.
    """
    test_ops.update({
        'tiff_list': ['input_1500.tif'],
        'batch_size': 200,
        'nplanes': 2,
        'nchannels': 2,
        'reg_tif': True,
        'reg_tif_chan2': True,
    })
    suite2p.run_s2p(ops=test_ops)
    assert all(utils.check_output(
        test_ops['save_path0'],
        get_outputs_to_check(test_ops['nchannels']) + ['reg_tif', 'reg_tif_chan2'],
        test_ops['data_path'][0],
        test_ops['nplanes'],
        test_ops['nchannels'],
        added_tag='1500'
    ))


