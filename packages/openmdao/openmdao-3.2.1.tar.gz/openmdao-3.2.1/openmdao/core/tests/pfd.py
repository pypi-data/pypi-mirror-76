import openmdao.api as om
from openmdao.components.tests.test_external_code_comp import ParaboloidExternalCodeCompFD

prob = om.Problem()
model = prob.model

model.add_subsystem('p', ParaboloidExternalCodeCompFD(), promotes_inputs=['x', 'y'])

# find optimal solution with SciPy optimize
# solution (minimum): x = 6.6667; y = -7.3333
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'

prob.model.add_design_var('x', lower=-50, upper=50)
prob.model.add_design_var('y', lower=-50, upper=50)

prob.model.add_objective('p.f_xy')

prob.driver.options['tol'] = 1e-9
prob.driver.options['disp'] = True

prob.setup()

# Set input values
prob.set_val('x', 3.0)
prob.set_val('y', -4.0)

prob.run_driver()
print(prob.get_val('x'))
print(prob.get_val('y'))
