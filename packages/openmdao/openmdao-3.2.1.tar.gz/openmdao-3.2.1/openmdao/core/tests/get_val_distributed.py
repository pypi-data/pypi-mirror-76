#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openmdao.api as om
import numpy as np

from openmdao.utils.assert_utils import assert_near_equal
from openmdao.utils.array_utils import evenly_distrib_idxs
import mpi4py.MPI as MPI

def main():
    N = 3

    class DistribComp(om.ExplicitComponent):

        def initialize(self):
            self.options['distributed'] = True

        def setup(self):
            rank = self.comm.rank
            sizes, offsets = evenly_distrib_idxs(self.comm.size, N)

            self.add_input('x', shape=1)  # , src_indices=[0])
            self.add_output('y', shape=sizes[rank])

        def compute(self, inputs, outputs):
            rank = self.comm.rank
            sizes, offsets = evenly_distrib_idxs(self.comm.size, N)

            outputs['y'] = inputs['x']*np.ones((sizes[rank],))
            if rank == 0:
                outputs['y'][0] = 2.

    class MyModel(om.Group):

        def setup(self):
            self.add_subsystem('ivc', om.IndepVarComp('x', 0.), promotes_outputs=['*'])
            self.add_subsystem('dst', DistribComp(), promotes_inputs=['x'])
            self.add_subsystem('sum', om.ExecComp('z = sum(y)', y=np.zeros((N,)), z=0.0))
            self.connect('dst.y', 'sum.y')

            self.add_subsystem('par', om.ParallelGroup(), promotes_inputs=['*'])
            self.par.add_subsystem('c1', om.ExecComp(['y=2.0*x']), promotes_inputs=['*'])
            self.par.add_subsystem('c2', om.ExecComp(['y=5.0*x']), promotes_inputs=['*'])

    prob = om.Problem(model=MyModel())
    prob.setup(mode='fwd')

    prob['x'] = 7.0
    prob.run_model()

    # get_remote=True
    assert_near_equal(prob.get_val('dst.x', get_remote=True), [7.])
    # assert_near_equal(prob.get_val('dst.y', get_remote=True), [2., 7., 7.])
    # assert_near_equal(prob.get_val('par.c1.x', get_remote=True), [7.])
    # assert_near_equal(prob.get_val('par.c1.y', get_remote=True), [14.])
    # assert_near_equal(prob.get_val('par.c2.x', get_remote=True), [7.])
    # assert_near_equal(prob.get_val('par.c2.y', get_remote=True), [35.])

    if prob.comm.rank == 0:
        # get_remote=False
        assert_near_equal(prob.get_val('dst.x', get_remote=False), [7.])
        # print(prob.get_val('dst.y', get_remote=False))
        # assert_near_equal(prob.get_val('dst.y', get_remote=False), [2., 7.])

        # assert_near_equal(prob.get_val('par.c1.x', get_remote=False), [7.])
        # assert_near_equal(prob.get_val('par.c1.y', get_remote=False), [14.])

        # assert_near_equal(prob.get_val('par.c2.x', get_remote=False), [7.])
        # with self.assertRaises(RuntimeError) as cm:
        #     prob.get_val('par.c2.y', get_remote=False)
        # self.assertEqual(str(cm.exception),
        #                  ("Problem: Variable 'par.c2.y' is not local to rank 0. "
        #                   "You can retrieve values from  other processes using "
        #                   "`problem.get_val(<name>, get_remote=True)`."))

        # get_remote=None
        assert_near_equal(prob['x'], [7.])
        # with self.assertRaises(RuntimeError) as cm:
        #     prob['dst.y']
        # self.assertEqual(str(cm.exception),
        #                  ("MyModel (<model>): dst.y is a distributed variable, "
        #                  "You can retrieve values from all processes using "
        #                  "`get_val(<name>, get_remote=True)' or from the local "
        #                  "process using `get_val(<name>, get_remote=False)'."))

        assert_near_equal(prob['par.c1.x'], [7.])
        assert_near_equal(prob['par.c1.y'], [14.])

        # with self.assertRaises(RuntimeError) as cm:
        #     prob['par.c2.x']
        # self.assertEqual(str(cm.exception),
        #                  ("MyModel (<model>): par.c2.x is not local to rank 0, "
        #                   "You can retrieve values from other processes using "
        #                   "get_val(<name>, get_remote=True)`."))
        # with self.assertRaises(RuntimeError) as cm:
        #     prob['par.c2.y']
        # self.assertEqual(str(cm.exception),
        #                  ("Problem: Variable 'par.c2.y' is not local to rank 0. "
        #                   "You can retrieve values from  other processes using "
        #                   "`problem.get_val(<name>, get_remote=True)`."))
    else:
        # get_remote=False
        assert_near_equal(prob.get_val('dst.x', get_remote=False), [7.])
        assert_near_equal(prob.get_val('dst.y', get_remote=False), [7.])

        assert_near_equal(prob['par.c1.x'], [7.])
        # with self.assertRaises(RuntimeError) as cm:
        #     prob.get_val('par.c1.y', get_remote=False)
        # self.assertEqual(str(cm.exception),
        #                  ("Problem: Variable 'par.c1.y' is not local to rank 1. "
        #                   "You can retrieve values from  other processes using "
        #                   "`problem.get_val(<name>, get_remote=True)`."))

        assert_near_equal(prob.get_val('par.c2.x', get_remote=False), [7.])
        assert_near_equal(prob.get_val('par.c2.y', get_remote=False), [35.])

        # get_remote=None
        assert_near_equal(prob['x'], [7.])
        # with self.assertRaises(RuntimeError) as cm:
        #     prob['dst.y']
        # self.assertEqual(str(cm.exception),
        #                  ("MyModel (<model>): dst.y is a distributed variable, "
        #                  "You can retrieve values from all processes using "
        #                  "`get_val(<name>, get_remote=True)' or from the local "
        #                  "process using `get_val(<name>, get_remote=False)'."))

        assert_near_equal(prob['par.c1.x'], [7.])
        # with self.assertRaises(RuntimeError) as cm:
        #     prob['par.c1.y']
        # self.assertEqual(str(cm.exception),
        #                  ("Problem: Variable 'par.c1.y' is not local to rank 1. "
        #                   "You can retrieve values from  other processes using "
        #                   "`problem.get_val(<name>, get_remote=True)`."))

        assert_near_equal(prob['par.c2.x'], [7.])
        assert_near_equal(prob['par.c2.y'], [35.])


if __name__ == "__main__":
    main()
