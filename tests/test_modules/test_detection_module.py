"""
Tests for the Suite2p Detection module.
"""

import numpy as np
import utils
from suite2p import detection


def prepare_for_detection(op, input_file_name_list, dimensions):
    """
    Prepares for detection by filling out necessary ops parameters. Removes dependence on
    other modules. Creates pre_registered binary file.
    """
    # Set appropriate ops parameters
    op['Lx'], op['Ly'] = dimensions
    op['nframes'] = 500 // op['nplanes'] // op['nchannels']
    op['frames_per_file'] = 500 // op['nplanes'] // op['nchannels']
    op['xrange'], op['yrange'] = [[2, 402], [2, 358]]
    ops = []
    for plane in range(op['nplanes']):
        curr_op = op.copy()
        plane_dir = utils.get_plane_dir(op, plane)
        bin_path = utils.write_data_to_binary(
            str(plane_dir.joinpath('data.bin')), str(input_file_name_list[plane][0])
        )
        curr_op['reg_file'] = bin_path
        if plane == 1: # Second plane result has different crop.
            curr_op['xrange'], curr_op['yrange'] = [[1, 403], [1, 359]]
        if curr_op['nchannels'] == 2:
            bin2_path = utils.write_data_to_binary(
                str(plane_dir.joinpath('data_chan2.bin')), str(input_file_name_list[plane][1])
            )
            curr_op['reg_file_chan2'] = bin2_path
        curr_op['save_path'] = plane_dir
        curr_op['ops_path'] = plane_dir.joinpath('ops.npy')
        ops.append(curr_op)
    return ops


def detect_wrapper(ops):
    """
    Calls the main_detect function and compares output dictionaries (cell_pix, cell_masks,
    neuropil_masks, stat) with prior output dicts.
    """
    for i in range(len(ops)):
        op = ops[i]
        cell_pix, cell_masks, neuropil_masks, stat = detection.main_detect(op, None)
        output_check = np.load(
            op['data_path'][0].joinpath(
                'detection',
                'detect_output_{0}p{1}c{2}.npy'.format(op['nplanes'], op['nchannels'], i)),
            allow_pickle=True
        )[()]
        assert np.array_equal(output_check['cell_pix'], cell_pix)
        utils.check_lists_of_arr_equal(cell_masks, output_check['cell_masks'])
        utils.check_lists_of_arr_equal(neuropil_masks, output_check['neuropil_masks'])
        utils.check_dict_dicts_all_close(stat, output_check['stat'])


def test_detection_output_1plane1chan(default_ops):
    ops = prepare_for_detection(
        default_ops,
        [[default_ops['data_path'][0].joinpath('detection', 'pre_registered.npy')]],
        (404, 360)
    )
    detect_wrapper(ops)


def test_detection_output_2plane2chan(default_ops):
    default_ops['nchannels'] = 2
    default_ops['nplanes'] = 2
    detection_dir = default_ops['data_path'][0].joinpath('detection')
    ops = prepare_for_detection(
        default_ops,
        [
            [detection_dir.joinpath('pre_registered01.npy'), detection_dir.joinpath('pre_registered02.npy')],
            [detection_dir.joinpath('pre_registered11.npy'), detection_dir.joinpath('pre_registered12.npy')]
        ]
        , (404, 360),
    )
    detect_wrapper(ops)