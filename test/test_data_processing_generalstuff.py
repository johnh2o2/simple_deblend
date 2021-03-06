'''test_data_processing_generalstuff.py - Joshua Wallace - Mar 2019

This tests classes and methods in the data_processing.py file,
using the Lomb-Scargle method.
'''

import unittest
import sys, os
sys.path.insert(1,os.path.abspath('../src'))
import data_processing as dproc
import numpy as np


class test_data_processing_init(unittest.TestCase):

    def setUp(self):
        pass

    def test_lc_collection_setup(self):
        # Test initialization of the lc_collection_for_processing class
        self.assertIsInstance(dproc.lc_collection_for_processing(1.),
                                dproc.lc_collection_for_processing)

    def test_periodsearch_results_setup(self):
        #Test initialization of the periodsearch_results class
        self.assertIsInstance(dproc.periodsearch_results('1'),
                                  dproc.periodsearch_results)


class test_warning_median_filter(unittest.TestCase):

    def setUp(self):
        self.col = dproc.lc_collection_for_processing(1.,n_control_workers=1)
        sample_len_1 = 3000
        t1 = np.linspace(0,1200,sample_len_1)
        self.col.add_object(t1,[10.]*sample_len_1,[1.]*sample_len_1,0.,0.,'o1')
        self.col.add_object(t1,[11.]*sample_len_1,[1.]*sample_len_1,0.,1.,'o2')

        ## LS run
        with self.assertWarns(UserWarning):
            col.run_ls(startp=10.,endp=11.,stepsize=0.1,autofreq=False,
                       medianfilter=False,
                       freq_window_epsilon_mf=1)

        with self.assertWarns(UserWarning):
            col.run_ls(startp=10.,endp=11.,stepsize=0.1,autofreq=False,
                       medianfilter=False,median_filter_size=1)

        # PDM run
        with self.assertWarns(UserWarning):
            col.run_pdm(startp=10.,endp=11.,stepsize=0.1,autofreq=False,
                        medianfilter=False,
                        freq_window_epsilon_mf=1)

        with self.assertWarns(UserWarning):
            col.run_pdm(startp=10.,endp=11.,stepsize=0.1,autofreq=False,
                        medianfilter=False,median_filter_size=1)

        # BLS run
        with self.assertWarns(UserWarning):
            col.run_bls(startp=10.,endp=11.,stepsize=0.1,autofreq=False,
                        medianfilter=False,
                        freq_window_epsilon_mf=1)

        with self.assertWarns(UserWarning):
            col.run_bls(startp=10.,endp=11.,stepsize=0.1,autofreq=False,
                        medianfilter=False,median_filter_size=1)








if __name__ == '__main__':
    unittest.main()

