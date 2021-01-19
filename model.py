import json
import random


class Worker(object):
    def __init__(self, worker_id):
        self.id = worker_id

    def __str__(self):
        return "\n\tWorker id: {}".format(self.id)

    def __repr__(self):
        return self.__str__()

    def get_dump(self):
        return self.id


class Resource(object):
    def __init__(self, parsed_resource):
        self.id = parsed_resource['id']
        self.max_tasks_simultaneously = parsed_resource['max_tasks']
        self.available_at_init = bool(parsed_resource['available_at_init'])

    def __str__(self):
        return "\n\tResource id: {}\n" \
               "\t\tmax_tasks: {}\n" \
               "\t\tavailable_at_init: {}".format(self.id,
                                                  self.max_tasks_simultaneously,
                                                  self.available_at_init)

    def __repr__(self):
        return self.__str__()

    def get_dump(self):
        return {'id': self.id,
                'max_tasks': self.max_tasks_simultaneously,
                'available_at_init': self.available_at_init}


class Task(object):
    def __init__(self, parsed_task):
        self.id = 0
        self.estimated_time = 0
        self.pre_requirement_tasks = []
        self.num_of_workers_needed = 0
        self.required_workers = []
        self.required_resources = []
        self.output_resources = []

        self.id = parsed_task['id']
        self.estimated_time = parsed_task['time']
        self.pre_requirement_tasks = parsed_task['pre_tasks']
        self.num_of_workers_needed = parsed_task['num_of_workers_needed']
        self.required_workers = parsed_task['req_workers']
        self.required_resources = parsed_task['req_resources']
        self.output_resources = parsed_task['output_resources']

    def __str__(self):
        return "\n\tTask id: {}\n" \
               "\t\testimated_time: {}\n" \
               "\t\tpre_requirement_tasks: {}\n" \
               "\t\tnum_of_workers_needed: {}\n" \
               "\t\trequired_workers: {}\n" \
               "\t\trequired_resources: {}\n" \
               "\t\toutput_resources: {}".format(self.id,
                                                 self.estimated_time,
                                                 self.pre_requirement_tasks,
                                                 self.num_of_workers_needed,
                                                 self.required_workers,
                                                 self.required_resources,
                                                 self.output_resources)

    def __repr__(self):
        return self.__str__()

    def get_dump(self):
        return {'id': self.id,
                'time': self.estimated_time,
                'pre_tasks': self.pre_requirement_tasks,
                'num_of_workers_needed': self.num_of_workers_needed,
                'req_workers': self.required_workers,
                'req_resources': self.required_resources,
                'output_resources': self.output_resources}


class InitialState(object):
    def __init__(self, json_path=""):
        self.workers = []
        self.resources = []
        self.tasks = []

        if json_path == "":
            return
        else:
            with open(json_path, "rb") as f:
                parsed_json = json.load(f)

            for worker_id in parsed_json['Workers']:
                self.workers.append(Worker(worker_id))

            for resource in parsed_json['Resources']:
                self.resources.append(Resource(resource))

            for task in parsed_json['Tasks']:
                self.tasks.append(Task(task))

    def __str__(self):
        return "Workers: {}\n" \
               "Resources: {}\n" \
               "Tasks: {}\n".format(str(self.workers),
                                    str(self.resources),
                                    str(self.tasks))

    def save_as_json(self, path):
        data = dict()
        data["Workers"] = [worker.get_dump() for worker in self.workers]
        data["Resources"] = [res.get_dump() for res in self.resources]
        data["Tasks"] = [task.get_dump() for task in self.tasks]

        with open(path, 'w') as f:
            json.dump(data, f)
