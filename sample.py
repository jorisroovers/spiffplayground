from SpiffWorkflow.specs import *
from SpiffWorkflow import Workflow
from SpiffWorkflow.Task import *

class MyTask(Simple):

    # This is the method to implement to execute custom code
    def _update_state_hook(self, my_task):
        print "Executing custom code"
        # Make sure we call the super's (i.e. Simple) _update_state_hook to fix
        # the state stuff etc
        super(MyTask, self)._update_state_hook(my_task)


def sequential_tasks():
    wspec = WorkflowSpec()

    t1 = Simple(wspec, 'task_t1')
    wspec.start.connect(t1)

    t2 = MyTask(wspec, 'task_t2')
    t1.connect(t2)


    # Create workflow from the spec
    workflow = Workflow(wspec)

    while not workflow.is_completed():
       tasks = workflow.get_tasks(Task.READY)

       for task in tasks:
            print task.id, task.task_spec.name
            workflow.complete_task_from_id(task.id)


if __name__ == "__main__":
    sequential_tasks()
