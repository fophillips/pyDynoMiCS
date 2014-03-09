from nose.tools import *
from analyse_idynomics import *

class TestAnalyseiDynomics:
    def setUp(self):
        self.directory = 'test_data'
        self.analysis = AnalyseiDynomics(self.directory)

    def test_init(self):
        assert_is(self.directory, self.analysis.directory)
