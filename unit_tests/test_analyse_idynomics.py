from nose.tools import *
from analyse_idynomics import *
from os.path import join, dirname, realpath

class TestAnalyseiDynomics:
    expected_solutes = ['MyAtmos', 'pressure']
    expected_species = ['MyBact']
    expected_reaction_rates = ['MyGrowth-rate']
    expected_biomass_name = "totalBiomass"
    expected_timesteps = 2
    expected_dimensions = (20.0, 20.0, 2.0)
    
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

    def test_reaction_rate_names(self):
        actual_reaction_rates = self.analysis.reaction_rate_names
        assert_list_equal(self.expected_reaction_rates, actual_reaction_rates)

    def test_all_env_names(self):
        expected_names = self.expected_solutes + self.expected_reaction_rates + self.expected_species + [self.expected_biomass_name]
        actual_names = self.analysis.all_env_names
        assert_list_equal(expected_names, actual_names)

    def test_total_timesteps(self):
        actual_timesteps = self.analysis.total_timesteps
        assert_equals(self.expected_timesteps, actual_timesteps)

    def test_world_dimensions(self):
        actual_dimensions = self.analysis.world_dimensions
        assert_equal(self.expected_dimensions, actual_dimensions)

        
