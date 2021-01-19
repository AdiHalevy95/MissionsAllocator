from itertools import groupby

import model


class WorkerState(object):
    def __init__(self, worker):
        """
        :type worker: model.Worker
        """
        self.worker_details = worker
        self.is_available = True
        self.tasks = []
        self.start_time = []

    def __str__(self):
        return "\n\tDetails: {}" \
               "\n\tis available: {}" \
               "\n\ttasks: {}" \
               "\n\tstart time: {}".format(str(self.worker_details),
                                           str(self.is_available),
                                           str(self.tasks),
                                           str(self.start_time))

    def __repr__(self):
        return self.__str__()


class ResourceState(object):
    def __init__(self, resource):
        """
        :type resource: model.Resource
        """
        self.resource_details = resource
        self.current_using_tasks = 0
        self.is_available = resource.available_at_init

    def __str__(self):
        return "\n\tDetails: {}" \
               "\n\tcurrent using tasks: {}" \
               "\n\tis available: {}".format(str(self.resource_details),
                                             str(self.current_using_tasks),
                                             str(self.is_available))

    def __repr__(self):
        return self.__str__()


class TaskState(object):
    def __init__(self, task):
        """
        :type task: model.Task
        """
        self.task_details = task
        self.is_on_work = False
        self.current_workers = []
        self.time_remaining = task.estimated_time
        self.is_finished = False

    def __str__(self):
        return "\n\tDetails: {}" \
               "\n\tis on work: {}" \
               "\n\tcurrent workers: {}" \
               "\n\ttime remaining: {}" \
               "\n\tis finished: {}".format(str(self.task_details),
                                            str(self.is_on_work),
                                            str(self.current_workers),
                                            str(self.time_remaining),
                                            str(self.is_finished))

    def __repr__(self):
        return self.__str__()


class OutputResult(object):
    def __init__(self, workers, time):
        self.workers = workers
        self.time = time

    def __str__(self):
        result = "All the tasks can be finished in {} time units.\n".format(self.time)
        for worker in self.workers:
            result += "\nWorker {}:\n".format(worker.worker_details.id)
            for i in range(len(worker.tasks)):
                result += "\tTask number {} at time {}\n".format(worker.tasks[i], worker.start_time[i])
        return result

    def __repr__(self):
        return self.__str__()


class PriorityDict(object):
    def __init__(self, req_workers, req_resources, worker_number, time):
        self.prio_dict = dict()
        self.prio_dict["REQ_WORKERS"] = req_workers
        self.prio_dict["REQ_RESOURCES"] = req_resources
        self.prio_dict["WORKERS_NUMBER"] = worker_number
        self.prio_dict["TIME"] = time

    def get_prio_dict(self):
        return self.prio_dict


class Priority(object):
    MAX_VALUE = 100.0

    def __init__(self, tasks, prio_dict):
        """
        :type tasks list[model.Task]
        :param tasks:
        """
        try:
            self.req_workers_scale = self.MAX_VALUE / self.find_max(tasks, lambda t: len(t.required_workers))
        except ZeroDivisionError:
            self.req_workers_scale = 0
        try:
            self.req_resources_scale = self.MAX_VALUE / self.find_max(tasks, lambda t: len(t.required_resources))
        except ZeroDivisionError:
            self.req_resources_scale = 0
        try:
            self.workers_number_scale = self.MAX_VALUE / self.find_max(tasks, lambda t: t.num_of_workers_needed)
        except ZeroDivisionError:
            self.workers_number_scale = 0
        try:
            self.time_scale = self.MAX_VALUE / self.find_max(tasks, lambda t: t.estimated_time)
        except ZeroDivisionError:
            self.time_scale = 0

        self.prio_dict = prio_dict

    @staticmethod
    def find_max(tasks, key):
        max_val = 0
        for task in tasks:
            if key(task) > max_val:
                max_val = key(task)
        return max_val

    def get_priority(self, task_details):
        """
        :type task_details model.Task
        :param task_details:
        :return:
        """
        return (self.prio_dict.get_prio_dict()["REQ_WORKERS"] * len(task_details.required_workers) * self.req_workers_scale +
                self.prio_dict.get_prio_dict()["REQ_RESOURCES"] * len(task_details.required_resources) * self.req_resources_scale +
                self.prio_dict.get_prio_dict()["WORKERS_NUMBER"] * task_details.num_of_workers_needed * self.workers_number_scale +
                self.prio_dict.get_prio_dict()["TIME"] * task_details.estimated_time * self.time_scale)


class MissionState(object):
    def __init__(self, init_state, prio_dict=None):
        """
        :type init_state: model.InitialState
        :param init_state:
        """
        self.current_time = 0
        self.workers_state = {}
        self.resources_state = {}
        self.tasks_state = {}

        self.pending_workers = 0

        for worker in init_state.workers:
            self.workers_state[worker.id] = WorkerState(worker)

        for resource in init_state.resources:
            self.resources_state[resource.id] = ResourceState(resource)

        for task in init_state.tasks:
            self.tasks_state[task.id] = TaskState(task)

        if prio_dict is None:
            prio_dict = PriorityDict(1, 1, 1, 1)

        self.priority_calculator = Priority(init_state.tasks, prio_dict)

    def __str__(self):
        def print_dict(dic):
            data = ""
            for key in dic.keys():
                data += ("\n\t" + str(key) + ":")
                data += ("\t" + str(dic[key]))
            return data

        return "Workers state: {}\n" \
               "Resources state: {}\n" \
               "Tasks state: {}\n".format(print_dict(self.workers_state),
                                          print_dict(self.resources_state),
                                          print_dict(self.tasks_state))

    def __repr__(self):
        return self.__str__()

    def calc_priority(self):
        pass

    def is_finished(self):
        for id, task in self.tasks_state.items():
            if not task.is_finished:
                return False
        return True

    def calculate_allocation(self, show=True):
        if show:
            print("Total of {} tasks with total time of {} time units.".format(len(self.tasks_state),
                                                                               sum(t.task_details.estimated_time for _, t in
                                                                                   self.tasks_state.items())))
            print("Total of {} workers.\n".format(len(self.workers_state)))
            print("Calculate allocation....\n".format(len(self.workers_state)))
        while not self.is_finished():
            self.check_for_new_allocation()
            self.current_time += 1
            self.advance_time()

        return OutputResult([val for _, val in self.workers_state.items()], self.current_time)

    def advance_time(self):
        # Check for finished tasks
        for id, task in self.tasks_state.items():
            if not task.is_finished:
                if task.is_on_work:
                    task.time_remaining -= 1
                    if task.time_remaining == 0:
                        # Mark as finished
                        task.is_finished = True
                        # Update workers availability
                        for worker_id in task.current_workers:
                            self.workers_state[worker_id].is_available = True
                        task.current_workers = []
                        # Update resources availability
                        for resource_id in task.task_details.required_resources:
                            self.resources_state[resource_id].current_using_tasks -= 1
                        # Update new resources
                        for resource_id in task.task_details.output_resources:
                            self.resources_state[resource_id].is_available = True
        if self.is_finished():
            return

    def is_resources_available(self, task):
        if all(self.resources_state[res].is_available and
               self.resources_state[res].current_using_tasks < self.resources_state[
                   res].resource_details.max_tasks_simultaneously
               for res in task.task_details.required_resources):
            return True
        return False

    def is_workers_available(self, task):
        if all(self.workers_state[worker].is_available for worker in task.task_details.required_workers) and \
                len([worker for _, worker in self.workers_state.items() if worker.is_available]) - \
                self.pending_workers >= task.task_details.num_of_workers_needed:
            return True
        return False

    def allocate_task(self, task):
        if not (self.is_resources_available(task) and self.is_workers_available(task)):
            return False

        for worker in task.task_details.required_workers:
            self.workers_state[worker].is_available = False
            self.workers_state[worker].tasks.append(task.task_details.id)
            self.workers_state[worker].start_time.append(self.current_time)
            task.current_workers.append(worker)

        # Do not allocate the rest of workers yet
        self.pending_workers += task.task_details.num_of_workers_needed - len(task.task_details.required_workers)

        for resource in task.task_details.required_resources:
            self.resources_state[resource].current_using_tasks += 1

        task.is_on_work = True

        return True

    def allocate_rest_workers(self, task):
        for _, worker in self.workers_state.items():
            if len(task.current_workers) >= task.task_details.num_of_workers_needed:
                break
            if worker.is_available:
                worker.is_available = False
                worker.tasks.append(task.task_details.id)
                worker.start_time.append(self.current_time)
                task.current_workers.append(worker.worker_details.id)
                self.pending_workers -= 1

    def check_for_new_allocation(self):
        # check for dependence
        independent_tasks = []
        for (tid, task) in self.tasks_state.items():
            if task.is_finished:
                continue
            if task.is_on_work:
                continue
            if all([self.tasks_state[req_task].is_finished for req_task in task.task_details.pre_requirement_tasks]):
                independent_tasks.append(task)

        # check for resources and workers
        task_with_available_resources_and_workers = []
        for task in independent_tasks:
            if self.is_resources_available(task) and self.is_workers_available(task):
                task_with_available_resources_and_workers.append(task)

        ordered_tasks = sorted(task_with_available_resources_and_workers,
                               key=lambda t: self.priority_calculator.get_priority(t.task_details), reverse=True)
        # ordered_tasks = self.sort_by_priority(task_with_available_resources_and_workers)

        allocated_tasks = []
        for task in ordered_tasks:
            if self.allocate_task(task):
                allocated_tasks.append(task)

        # finish the workers allocation
        for task in allocated_tasks:
            self.allocate_rest_workers(task)

    def sort_by_priority(self, tasks):
        # sort by specific required workers number in decreasing order
        grouped_list = self.sort_and_group(tasks,
                                           key=lambda task: len(task.task_details.required_workers), reverse=True)

        # sort by resources number in decreasing order
        grouped_list_2 = []
        for lst in grouped_list:
            grouped_list_2 += self.sort_and_group(lst, key=lambda task: len(task.task_details.required_resources),
                                                  reverse=True)

        # sort by total workers number in decreasing order
        grouped_list_3 = []
        for lst in grouped_list:
            grouped_list_3 += self.sort_and_group(lst, key=lambda task: task.task_details.num_of_workers_needed,
                                                  reverse=True)

        # sort by estimated time in decreasing order
        grouped_list_4 = []
        for lst in grouped_list_3:
            grouped_list_4 += self.sort_and_group(lst, key=lambda task: task.task_details.estimated_time, reverse=True)

        ordered_tasks = [item for sublist in grouped_list_3 for item in sublist]
        return ordered_tasks

    @staticmethod
    def sort_and_group(lst, key, reverse=False):
        lst.sort(key=key, reverse=reverse)
        sorted_grouped_list = []
        for (_, item) in groupby(lst, key):
            new_lst = []
            for x in item:
                new_lst.append(x)
            sorted_grouped_list.append(new_lst)
        return sorted_grouped_list
