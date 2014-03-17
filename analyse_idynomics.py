import numpy as np
import xml.etree.ElementTree as ET
from os.path import join
from zipfile import ZipFile
from io import StringIO

def lazy_property(fn):
    '''
    Decorator that makes a property lazy-evaluated
    From http://stevenloria.com/lazy-evaluated-properties-in-python/
    '''
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property

class AnalyseiDynomics:
    biomass_name = "totalBiomass"
    
    def __init__(self, directory):
        self.directory = directory

    @lazy_property
    def solute_sum_files(self):
        return ZipFile(join(self.directory, 'env_Sum.zip'))

    @lazy_property
    def solute_state_files(self):
        return ZipFile(join(self.directory, 'env_State.zip'))

    @lazy_property
    def agent_sum_files(self):
        return ZipFile(join(self.directory, 'agent_Sum.zip'))

    @lazy_property
    def agent_state_files(self):
        return ZipFile(join(self.directory, 'agent_State.zip'))

    @lazy_property
    def solute_names(self):
        sum_file = self.solute_sum_files.open(self.solute_sum_files.namelist()[0])
        return [solute.get('name')
                for solute in ET.parse(sum_file).getroot().find('simulation/bulk').findall('solute')]
    @lazy_property
    def species_names(self):
        sum_file = self.agent_sum_files.open(self.agent_sum_files.namelist()[0])
        return [species.get('name')
                for species in ET.parse(sum_file).getroot().find('simulation').findall('species')]

    @lazy_property
    def all_env_names(self):
        state_file = self.solute_state_files.open(self.solute_state_files.namelist()[0])
        return [solute.get('name')
                for solute in ET.parse(state_file).getroot().find('simulation').findall('solute')]
        
    @lazy_property
    def reaction_rate_names(self):        
        return [r for r in self.all_env_names if r not in
                (self.species_names + self.solute_names + [self.biomass_name])]

    @lazy_property
    def total_timesteps(self):
        return len(self.solute_sum_files.namelist())

    @lazy_property
    def world_dimensions(self):
        f = self.agent_sum_files.open(self.agent_sum_files.namelist()[0])
        grid = ET.parse(f).getroot().find('simulation/grid')
        r = float(grid.get('resolution'))
        i = int(grid.get('nI'))
        j = int(grid.get('nJ'))
        k = int(grid.get('nK'))
        return (k,j,i,r)

    @lazy_property
    def solute_sum_data(self):
        names = self.solute_names
        files = [self.solute_sum_files.open(f) for f in  self.solute_sum_files.namelist()[::-1]]
        sum_data = np.zeros(self.total_timesteps,
                            dtype={'names': names, 'formats': len(names) * ['3f4']})
        for i, f in enumerate(files):
            root = ET.parse(f).getroot()
            for name in names:
                sum_data[name][i,0] = float(root.find('simulation/bulk/solute[@name="%s"]' % name).text)
                sum_data[name][i,1] = float(root.find('simulation/globalProductionRate/solute[@name="%s"]' % name).text)
                sum_data[name][i,2] = float(root.find('simulation/bulk/uptake_rate[@name="%s"]' % name).text)
        return sum_data

    
    def load_solute_state_data(self, solute_name):
        files = [self.solute_state_files.open(f) for f in
                 self.solute_state_files.namelist()[::-1]]
        dimensions = self.world_dimensions[0:3]
        data = np.zeros(self.total_timesteps, dtype=('(%d,%d,%d)float32' % dimensions))
        for i, f in enumerate(files):
            text = ET.parse(f).getroot().find('simulation/solute[@name="%s"]' % solute_name).text
            data[i] = np.fromstring(text, sep=";\n").reshape(dimensions)
        return data

    def load_agent_state_data(self, species_name):
        files = [self.agent_state_files.open(f) for f in
                 self.agent_state_files.namelist()[::-1]]
        structure = {'names':
                     ['family','genealogy','generation','birthday',
                      'biomass','inert','capsule','growthRate','volumeRate',
                      'locationX','locationY','locationZ','radius','totalRadius'],
                     'formats': (['i4'] * 3 + ['f4'] * 11)}
        data = []
        for f in files:
            text = ET.parse(f).getroot().find('simulation/species[@name="%s"]' % species_name).text
            data.append(np.loadtxt(StringIO(text.replace(';','')), delimiter=',', dtype=structure))
        return data
