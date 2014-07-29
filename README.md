pyDynoMiCS
==========
[![Build Status](https://travis-ci.org/fophillips/pyDynoMiCS.svg?branch=master)](https://travis-ci.org/fophillips/pyDynoMiCS)

A bunch of methods for analysing data created with [iDynomics](https://github.com/kreft/iDynoMiCS), aiming to replace the preexisting `matlab` functions.

## Usage
Open up iPython with `ipython qtconsole --pylab=inline`

```python
In [1]: %run path/to/pydynomics.py

In [2]: data = pyDynoMiCS('path/to/results_files/something(20140729_1234)')

In [3]: data.solute_names
Out[3]: ['O2', 'Glucose','pressure']

In [4]: data.species_names
Out[4]: ['MyBact']

In [5]: data.reaction_rate_names
Out[5]: ['BacteriaGrowth-rate']

In [6]: data.all_env_names # names of everything there is solute_state data for
Out[6]: ['O2',
         'Glucose',
         'pressure',
         'BacteriaGrowth-rate',
         'MyBact',
         'totalBiomass']

In [7]: data.total_timesteps
Out[7]: 50

In [8]: data.world_dimensions # (k, j, i, resolution)
Out[8]: (1, 129, 129, 2.0)

In [9]: data.solute_sum['Glucose'].shape # one row for each timestep
                                         # one field for: concentration
                                         #                global production rate
                                         #                uptake rate
Out[9]: (50, 3)

In [10]: data.solute_sum['Glucose'][2] # timestep 2
Out[10]: array([  0.00000000e+00,   3.43684992e+08,   0.00000000e+00], dtype=float32)

In [11]: data.agent_sum['MyBact'].shape # one row for each timestep
                                        # one field for: population
                                        #                mass
                                        #                growth rate
Out[11]: (50, 3)

In [12]: data.agent_sum['MyBact'][2] # timestep 2
Out[12]: array([  1.86000000e+02,   8.29317266e+04,   7.27687378e+01], dtype=float32)

In [13]: data.solute_state('Glucose').shape # note round brackets!
                                         # (timestep, z, y, x)
Out[13]: (50, 1, 129, 129)

In [14]: data.agent_state('MyBact')[2].shape # timestep 2, length is number of agents
Out[14]: (186,)

In [15]: data.agent_state('MyBact')[2][10]['locationX'] # x coordinate of agent 10 at timestep 2
Out[15]: 132.36357

In [16]: data.agent_state('MyBact')[0]['locationX'].shape # x coord of all agents at timestep 2
Out[16]: (186,)

In [17]: plot(data.agent_sum['MyBact'][:,1]) # total mass of MyBact over all time
Out[17]: [<matplotlib.lines.Line2D at 0x10eb1a550>]
```
![Mass over time](http://i.imgur.com/bTgV6As.png)
```python
In [18]: contourf(data.solute_state('Glucose')[1,0], cmap=cm.OrRd) # timestep 1, z=0
    ...: colorbar() # press ctrl-return to get new line

Out[18]: <matplotlib.colorbar.Colorbar at 0x10e0e4940>
```
![Contour plot](http://i.imgur.com/imPfmZL.png)
