'''test_lc_class_initialization.py - Joshua Wallace - Feb 2019

This tests the class definitions in lightcurve_class.py.
'''

import unittest
import sys, os
sys.path.insert(1,os.path.abspath('../src'))
import light_curve_class as lcclass

class test_light_curve_objects(unittest.TestCase):

    # Some constructed light curve data, for later convenience
    def setUp(self):
        self.t1 = [1,2.,3,4,5.1,6,7,8,9,10.]
        self.t2 = [-3,-2,0,88.2,89.23432123,5]
        self.mag1 = [5.,6.,7,8,9.,10.,11,12,3.,7.283423]
        self.mag2 = [1,2,3,4,5,6]
        self.err1 = [1.]*len(self.mag1)
        self.err2 = [1.]*len(self.mag2)

    # Test initialization of the light_curve() class
    def test_light_curve_setup(self):

        # Test two initializations
        self.assertIsInstance(lcclass.light_curve(self.t1,self.mag1,
                                                      self.err1),
                                  lcclass.light_curve)
        self.assertIsInstance(lcclass.light_curve(self.t2,self.mag2,
                                                      self.err2),
                                  lcclass.light_curve)

        # Test that different length time, mag, err data raise exceptions
        with self.assertRaises(ValueError):
            lcclass.light_curve(self.t1+[1.],self.mag1,self.err1)
            
        with self.assertRaises(ValueError):
            lcclass.light_curve(self.t1,self.mag1,self.err1+[1.])

        with self.assertRaises(AttributeError):
            lcclass.light_curve(1,self.mag2,self.err2)

            
    # Test initialization of the single_lc_object() class
    def test_single_lc_object_setup(self):

        # Test an initialization
        self.assertIsInstance(lcclass.single_lc_object(self.t1,
                                                           self.mag1,
                                                           self.err1,
                                                           1.,
                                                           2.,
                                                           '123'),
                                  lcclass.single_lc_object)

    def test_lc_objects_setup(self):
        all_objects = lcclass.lc_objects(5.)

        # Test that passing incorrect and wrong number of arguments
        # Raises an error
        with self.assertRaises(TypeError):
            all_objects.add_object('foo')
        with self.assertRaises(TypeError):
            all_objects.add_object(1.,27.,'bar',True)
        with self.assertRaises(ValueError):
            all_objects.add_object([1.,2.],[3.],[4.,5.],0,0,'hi')
        with self.assertRaises(AttributeError):
            all_objects.add_object([1.,2.,3.],[1.,2.,3.],1.,0,0,'bye')

        # Add light curves to all_objects
        all_objects.add_object(self.t1,self.mag1,self.err1,
                                   4.,4.,'1')
        all_objects.add_object(self.t2,self.mag2,self.err2,
                                   4.,8.999,'2')

        # Make sure the neighbors are getting assessed and added correctly
        self.assertListEqual(all_objects.objects[all_objects.index_dict['1']].neighbors,
                             ['2'])
        self.assertListEqual(all_objects.objects[all_objects.index_dict['2']].neighbors,
                             ['1'])

        # Add another object
        all_objects.add_object([1.],[1.],[1.], 4.,9.000001,'3')
        # Make sure the neighbors are correct
        self.assertListEqual(all_objects.objects[all_objects.index_dict['1']].neighbors,
                             ['2'])
        self.assertListEqual(all_objects.objects[all_objects.index_dict['2']].neighbors,
                             ['1','3'])
        self.assertListEqual(all_objects.objects[all_objects.index_dict['3']].neighbors,
                             ['2'])

        # Make sure exception is raised when a duplicate ID is added
        with self.assertRaises(ValueError):
            all_objects.add_object([1.],[1.],[1.],1.,1.,'3')
                                                            



if __name__ == '__main__':
    unittest.main()
