import random

import model


class MissionGenerator(object):
    def __init__(self, path=""):
        self.initial_state = model.InitialState()
        self.randomize_initial_state()
        if path != "":
            self.initial_state.save_as_json(path)

    def get_state(self):
        return self.initial_state

    def randomize_initial_state(self):
        self.randomize_workers()
        self.randomize_resources()
        self.randomize_tasks()

    def randomize_workers(self):
        for i in range(random.randint(3, 8)):
            self.initial_state.workers.append(model.Worker(i + 1))

    def randomize_resources(self):
        for i in range(random.randint(5, 10)):
            self.initial_state.resources.append(model.Resource({'id': i + 1,
                                                                'max_tasks': random.randint(1, 3),
                                                                'available_at_init': 'True'}))

    def randomize_tasks(self):
        initial_resources_number = len(self.initial_state.resources)
        for i in range(random.randint(8, 30)):
            num_of_workers_needed = random.randint(1, int(len(self.initial_state.workers) * 0.75))
            req_workers = random.sample(range(1, len(self.initial_state.workers) + 1),
                                        k=random.randint(0, num_of_workers_needed))
            req_resources = random.sample(range(1, len(self.initial_state.resources) + 1),
                                          k=random.randint(0, int(initial_resources_number * 0.5)))
            output_resources_number = random.choices([0, 1, 2, 3], weights=[8, 4, 2, 1], k=1)
            output_resources = []
            for x in range(output_resources_number[0]):
                res_id = len(self.initial_state.resources) + 1
                output_resources.append(res_id)
                self.initial_state.resources.append(model.Resource({'id': res_id,
                                                                    'max_tasks': random.randint(1, 3),
                                                                    'available_at_init': False}))

            pre_task_number = random.choices([0, 1, 2, 3], weights=[8, 4, 2, 1], k=1)[0]
            if pre_task_number > i:
                pre_task_number = i
            pre_tasks = random.sample(range(1, i + 1), k=pre_task_number)

            self.initial_state.tasks.append(model.Task({'id': i + 1,
                                                        'time': random.randint(1, 12),
                                                        'pre_tasks': pre_tasks,
                                                        'num_of_workers_needed': num_of_workers_needed,
                                                        'req_workers': req_workers,
                                                        'req_resources': req_resources,
                                                        'output_resources': output_resources}))
