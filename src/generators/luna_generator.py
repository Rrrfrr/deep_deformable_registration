import os
import sys
import random
import numpy as np

base_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..")
sys.path.append(base_dir)
from utils.LungsLoader import LungsLoader


loader = LungsLoader()


def scan_generator(scans_ids, width, height, depth, loop, shuffle):
    scan_gen = loader.preprocess_scans(scans_ids, width, height, depth, loop, shuffle)
    zeros = np.zeros((1,) + (width, height, depth) + (3,))
    try:
        while True:
                src_scan = next(scan_gen)[0]
                tgt_scan = next(scan_gen)[0]
                src_scan = src_scan[np.newaxis, :, :, :, np.newaxis]
                tgt_scan = tgt_scan[np.newaxis, :, :, :, np.newaxis]
                zeros = np.zeros((1,) + (width, height, depth) + (3,))
                yield ([src_scan, tgt_scan], [tgt_scan, zeros, zeros])
    except StopIteration:
        raise StopIteration(f"Completed iteration over the f{len(scans_ids)} scans")


def scan_and_seg_generator(scans_ids, width, height, depth, loop, shuffle):
    if shuffle:
        random.shuffle(scans_ids)
    scan_gen = loader.preprocess_scans(scans_ids, width, height, depth, loop, shuffle=False)
    seg_gen = loader.preprocess_segmentations(scans_ids, width, height, depth, loop, shuffle=False)
    zeros = np.zeros((1,) + (width, height, depth) + (3,))

    try:
        while True:
            src_scan = next(scan_gen)[0]
            tgt_scan = next(scan_gen)[0]
            src_scan = src_scan[np.newaxis, :, :, :, np.newaxis]
            tgt_scan = tgt_scan[np.newaxis, :, :, :, np.newaxis]

            src_seg = next(seg_gen)[0]
            tgt_seg = next(seg_gen)[0]
            src_seg = src_seg[np.newaxis, :, :, :, np.newaxis]
            tgt_seg = tgt_seg[np.newaxis, :, :, :, np.newaxis]

            yield ([src_scan, tgt_scan, src_seg], [tgt_scan, tgt_seg, zeros, zeros])
    except StopIteration:
        raise StopIteration(f"Completed iteration over the f{len(scans_ids)} scans")