#!/usr/bin/env python3

import unittest
import os

import numpy as np

import openmdao.api as om
from openmdao.drivers.genetic_algorithm_driver import GeneticAlgorithm
from openmdao.test_suite.components.branin import Branin, BraninDiscrete
from openmdao.test_suite.components.paraboloid import Paraboloid
from openmdao.test_suite.components.paraboloid_distributed import DistParab
from openmdao.test_suite.components.sellar_feature import SellarMDA
from openmdao.test_suite.components.three_bar_truss import ThreeBarTruss

from openmdao.utils.assert_utils import assert_near_equal
from openmdao.utils.mpi import MPI

try:
    from openmdao.vectors.petsc_vector import PETScVector
except ImportError:
    PETScVector = None

import openmdao.api as om
from openmdao.test_suite.components.branin import Branin

prob = om.Problem()
model = prob.model

par = model.add_subsystem('par', om.ParallelGroup(),
                          promotes_inputs=['*'])

par.add_subsystem('comp1', Branin(),
                  promotes_inputs=[('x0', 'xI'), ('x1', 'xC')])
par.add_subsystem('comp2', Branin(),
                  promotes_inputs=[('x0', 'xI'), ('x1', 'xC')])

model.add_subsystem('comp', om.ExecComp('f = f1 + f2'))
model.connect('par.comp1.f', 'comp.f1')
model.connect('par.comp2.f', 'comp.f2')

model.add_design_var('xI', lower=-5.0, upper=10.0)
model.add_design_var('xC', lower=0.0, upper=15.0)
model.add_objective('comp.f')

prob.driver = om.SimpleGADriver()
prob.driver.options['bits'] = {'xC': 8}
prob.driver.options['max_gen'] = 10
prob.driver.options['pop_size'] = 25
prob.driver.options['run_parallel'] = True
prob.driver.options['procs_per_model'] = 2

prob.driver._randomstate = 1

prob.setup()

prob.set_val('xC', 7.5)
prob.set_val('xI', 0.0)

prob.run_driver()

prob.model.list_outputs(list_autoivcs=True)
prob.model.list_inputs()

# Optimal solution
assert_near_equal(prob.get_val('comp.f'), 0.98799098, 1e-6)

assert_near_equal(prob.get_val('xI', get_remote=True),-3.0, 1e-6)
assert_near_equal(prob.get_val('xC', get_remote=True), 11.94117647, 1e-6)

assert_near_equal(prob.get_val('xI'),-3.0, 1e-6)
assert_near_equal(prob.get_val('xC'), 11.94117647, 1e-6)
