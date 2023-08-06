# Copyright 2016 - 2018  Ternaris.
# SPDX-License-Identifier: AGPL-3.0-only

import unittest

from marv_api import DatasetInfo as DSI
from marv_robotics.bag import scan


class TestCase(unittest.TestCase):
    maxDiff = None

    def test_nonbag(self):
        rv = scan('/', [''], ['a', 'b'])
        self.assertEqual(rv, [])

    def test_single_bags(self):
        rv = scan('/', [''], ['foo.bag', 'bar.bag'])
        self.assertEqual(rv, [DSI(name='foo', files=['foo.bag']),
                              DSI(name='bar', files=['bar.bag'])])

    def test_rosbag_sets(self):
        rv = scan('/', [''], ['set0_0000-00-00-00-00-00_0.bag',
                              'set0_0000-01-00-00-00-00_1.bag',
                              'set0_0000-02-00-00-00-00_2.bag',
                              'set1_0000-00-00-00-00-00_0.bag',
                              'set1_0000-01-00-00-00-00_1.bag',
                              'set1_0000-02-00-00-00-00_2.bag',
                              'set2.bag',
                              'set2_0000-00-00-00-00-00_0.bag',
                              'set2_0000-00-00-00-00-00_1.bag',
                              'set2_0000-00-00-00-00-00_2.bag'])
        self.assertEqual(rv, [
            DSI(name='set0', files=['set0_0000-00-00-00-00-00_0.bag',
                                    'set0_0000-01-00-00-00-00_1.bag',
                                    'set0_0000-02-00-00-00-00_2.bag']),
            DSI(name='set1', files=['set1_0000-00-00-00-00-00_0.bag',
                                    'set1_0000-01-00-00-00-00_1.bag',
                                    'set1_0000-02-00-00-00-00_2.bag']),
            DSI(name='set2', files=['set2.bag']),
            DSI(name='set2', files=['set2_0000-00-00-00-00-00_0.bag',
                                    'set2_0000-00-00-00-00-00_1.bag',
                                    'set2_0000-00-00-00-00-00_2.bag']),
        ])

    def test_scan_broken_set_edge_cases(self):
        rv = scan('/', [''], ['set0_0000-00-00-00-00-00_0.bag',
                              'set0_0000-00-00-00-00-00_2.bag',
                              'set1_0000-00-00-00-00-00_1.bag',
                              'set1_0000-00-00-00-00-00_2.bag',
                              'set2.bag',
                              'set2_0000-00-00-00-00-00_1.bag',
                              'set2_0000-00-00-00-00-00_2.bag'])
        self.assertEqual(rv, [
            DSI(name='set0', files=['set0_0000-00-00-00-00-00_0.bag']),
            DSI(name='set0_0000-00-00-00-00-00_2', files=['set0_0000-00-00-00-00-00_2.bag']),
            DSI(name='set1_0000-00-00-00-00-00_1', files=['set1_0000-00-00-00-00-00_1.bag']),
            DSI(name='set1_0000-00-00-00-00-00_2', files=['set1_0000-00-00-00-00-00_2.bag']),
            DSI(name='set2', files=['set2.bag']),
            DSI(name='set2_0000-00-00-00-00-00_1', files=['set2_0000-00-00-00-00-00_1.bag']),
            DSI(name='set2_0000-00-00-00-00-00_2', files=['set2_0000-00-00-00-00-00_2.bag']),
        ])

    def test_without_timestamp(self):
        rv = scan('/', [''], ['foo_0.bag', 'foo_1.bag', 'foo_3.bag', 'foo_4.bag'])
        self.assertEqual(rv, [DSI(name='foo', files=['foo_0.bag', 'foo_1.bag']),
                              DSI(name='foo_3', files=['foo_3.bag']),
                              DSI(name='foo_4', files=['foo_4.bag'])])

    def test_without_prefix(self):
        rv = scan('/', [''], [
            '0000-00-00-00-00-00.bag',
            '0000-00-00-00-00-00_0.bag',
            '0000-01-00-00-00-00_1.bag',
            '0000-02-00-00-00-00_2.bag',
            '0000-03-00-00-00-00_0.bag',
            '0000-04-00-00-00-00_1.bag',
            '0000-05-00-00-00-00_2.bag',
            '0000-06-00-00-00-00.bag',
            '0000-07-00-00-00-00.bag',
            '0000-08-00-00-00-00_0.bag',
            '0000-09-00-00-00-00_1.bag',
            '0000-10-00-00-00-00_2.bag',
        ])
        self.assertEqual(rv, [
            DSI(name='0000-00-00-00-00-00', files=['0000-00-00-00-00-00.bag']),
            DSI(name='0000-00-00-00-00-00', files=[
                '0000-00-00-00-00-00_0.bag',
                '0000-01-00-00-00-00_1.bag',
                '0000-02-00-00-00-00_2.bag',
            ]),
            DSI(name='0000-03-00-00-00-00', files=[
                '0000-03-00-00-00-00_0.bag',
                '0000-04-00-00-00-00_1.bag',
                '0000-05-00-00-00-00_2.bag',
            ]),
            DSI(name='0000-06-00-00-00-00', files=['0000-06-00-00-00-00.bag']),
            DSI(name='0000-07-00-00-00-00', files=['0000-07-00-00-00-00.bag']),
            DSI(name='0000-08-00-00-00-00', files=[
                '0000-08-00-00-00-00_0.bag',
                '0000-09-00-00-00-00_1.bag',
                '0000-10-00-00-00-00_2.bag',
            ]),
        ])

    def test_mixed_edge_cases(self):
        rv = scan('/', [''], ['set0_0000-00-00-00-00-00_0.bag',
                              'set0_1.bag',
                              'set0_1000-00-00-00-00-00_2.bag'])
        self.assertEqual(rv, [
            DSI(name='set0', files=['set0_0000-00-00-00-00-00_0.bag']),
            DSI(name='set0_1', files=['set0_1.bag']),
            DSI(name='set0_1000-00-00-00-00-00_2', files=['set0_1000-00-00-00-00-00_2.bag']),
        ])

    def test_missing_index(self):
        rv = scan('/', [''], ['foo_0000-11-00-00-00-00.bag',
                              'foo_0000-22-00-00-00-00.bag'])
        self.assertEqual(rv, [
            DSI(name='foo_0000-11-00-00-00-00', files=['foo_0000-11-00-00-00-00.bag']),
            DSI(name='foo_0000-22-00-00-00-00', files=['foo_0000-22-00-00-00-00.bag']),
        ])
