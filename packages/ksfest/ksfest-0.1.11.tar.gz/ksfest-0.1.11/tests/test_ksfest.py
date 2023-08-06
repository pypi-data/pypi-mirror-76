#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ksfest` package."""


import unittest
import click
from click.testing import CliRunner
#from ksfest import ksfest


class TestKsfest(unittest.TestCase):
    """Tests for `ksfest` package."""


    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    #def test_ks_fest(self):
    #    import pandas as pd
    #    import seaborn as sns

    #    iris = sns.load_dataset('iris')
    #    gks= ksfest.ks_fest()
    #   output= gks.get_ks(iris, var_dim='species', sample=0.3, na_number=-1)
    #   num_cols=output.shape[1]
    #   self.assertEqual(num_cols, len(gks.cols) +1) # assert number of columns