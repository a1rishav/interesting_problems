import json
import time
from concurrent.futures import ThreadPoolExecutor
import ray
from utils import get_pubsub, get_random_number

class System2:
    def __init__(self):
        self._task_channel = "task"
        self._solution_channel = "solution"
        self.executor = ThreadPoolExecutor(1)
        self.solution_ids = []
        self._continuous_loop_sleep_interval = 0.01
        time.sleep(self._continuous_loop_sleep_interval)
        self.init()
        print("System 2 has started")

    def publish_solutions(self):
        solution_counter = 0
        while True:
            try:
                if len(self.solution_ids) > 0:
                    done_id, not_done_ids = ray.wait(self.solution_ids)
                    if done_id:
                        solution_counter += 1
                        solution = ray.get(done_id)[0]
                        if solution_counter % 10 == 0:
                            print("Published solutions : {}".format(solution_counter))
                        self.pubsub.publish(self._solution_channel, json.dumps(solution))
                        self.solution_ids.remove(done_id[0])
                    else:
                        time.sleep(self._continuous_loop_sleep_interval)
            except Exception as e:
                print(e)

    def solve(self, random_min, random_max):
        subscriber = self.pubsub.pubsub()
        subscriber.subscribe(self._task_channel)
        task_counter = 0
        while True:
            message = subscriber.get_message()
            if message and not message['data'] == 1:
                task_counter += 1
                if task_counter > 0 and task_counter % 10 == 0:
                    print("Received task : {}".format(task_counter))

                task = json.loads(message['data'])
                task_id = task['id']
                task_number = task['number']
                self.solution_ids.append(solve_task.remote(task_id, task_number, random_min, random_max))
            else:
                time.sleep(self._continuous_loop_sleep_interval)

    def init(self):
        self.pubsub = get_pubsub()
        ray.init()
        self.executor.submit(self.publish_solutions)


# def solve_task(self, task_id, random_no_count, random_min=1, random_max=1000_000_000):
@ray.remote
def solve_task(task_id, random_no_count, random_min, random_max):
    print("Solving task : {}, random_no_count : {}".format(task_id, random_no_count))
    task_start_time = time.time()
    sum = 0
    for counter in range(random_no_count):
        random_number = get_random_number(random_min, random_max)
        sum += random_number
    task_finish_time = time.time()
    solution = {"id": task_id, "st_time": task_start_time, "end_time": task_finish_time,
                "sum": sum}
    print("Solved task : {}".format(task_id))
    return solution


if __name__ == '__main__':
    configs = None
    with open('configs.json', 'r') as f:
        data = json.load(f)
    if not data:
        raise Exception("Invalid configuration")

    random_no_min = data["system_2"]["random_no_min"]
    random_no_max = data["system_2"]["random_no_max"]
    System2().solve(random_min=random_no_min, random_max=random_no_max)
