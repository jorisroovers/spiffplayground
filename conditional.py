from SpiffWorkflow.specs import *
from SpiffWorkflow import Workflow
from SpiffWorkflow.Task import *
from SpiffWorkflow.operators import *

import logging
# Uncomment the following line for Spiff debugging

#logging.basicConfig(level=logging.DEBUG)

class ApprovalTask(ExclusiveChoice):

    def _update_state_hook(self, my_task):
        print "TEST"
        my_task.data['a'] = 123
        my_task.data['b'] = 13
        super(ApprovalTask, self)._update_state_hook(my_task)


def conditional_tasks():
    wspec = WorkflowSpec()

    excl_choice_1 = ApprovalTask(wspec, 'approval')
    wspec.start.connect(excl_choice_1)

    c1 = Simple(wspec, 'on default (else)')
    excl_choice_1.connect(c1) # else: default choice

    c2 = Simple(wspec, 'condition met')
    cond = Equal(Attrib('a'), Attrib('b'))
    excl_choice_1.connect_if(cond, c2)

    # Create workflow from the spec
    workflow = Workflow(wspec)

    while not workflow.is_completed():
       tasks = workflow.get_tasks(Task.READY)
       for task in tasks:
            print task.id, task.task_spec.name, task.data
            workflow.complete_task_from_id(task.id)


if __name__ == "__main__":
    conditional_tasks()
