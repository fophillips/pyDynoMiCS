from nose.tools import *
from analyse_idynomics import *
from os.path import join, dirname, realpath

class TestAnalyseiDynomics:
    expected_solutes = ['MyAtmos', 'pressure']
    expected_species = ['MyBact']
    
    def setUp(self):
        self.directory = join(dirname(realpath(__file__)), 'test_data')
        self.analysis = AnalyseiDynomics(self.directory)

    def test_init(self):
        assert_is(self.directory, self.analysis.directory)

    def test_solute_names(self):
        actual_solutes = self.analysis.solute_names
        assert_list_equal(self.expected_solutes, actual_solutes)

    def test_species_names(self):
        actual_species = self.analysis.species_names
        assert_list_equal(self.expected_species, actual_species)
