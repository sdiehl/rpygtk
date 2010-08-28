import unittest
import os
from ui import main

print os.getcwd()

class TestMain(unittest.TestCase):
    def setUp(self):
        self.m = main.MainWindow()
    
    def test_mainWindow(self):
        assert(self.m)
    
    def test_dataframe(self):
        import numpy
        #Random 25x4 Numpy Matrix
        self.m.render_dataframe(numpy.random.rand(25,4) ,name='devel',rownames=xrange(0,25))
        assert(self.m.active_robject)
        assert(self.m.active_robject.columns)
        assert(self.m.active_robject.column_data)
        
    def test_imports(self):
        datasets = ['iris','Nile','morley','freeny','sleep','mtcars']
        for a in datasets:
            main.rsession.r('%s=%s' % (a,a))
            self.m.sync_with_r()
            assert(a in self.m.robjects)
                
unittest.main()