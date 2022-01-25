import json
import time
import uuid
from utils import get_random_number, get_pubsub
from concurrent.futures import ThreadPoolExecutor


class System1:

    def __init__(self, no_of_tasks_to_produce, thread_pool_size=4):
        self.no_of_tasks_to_produce = no_of_tasks_to_produce
        self.executor = ThreadPoolExecutor(thread_pool_size)
        self.pubsub = get_pubsub()
        self._task_channel = "task"
        self._solution_channel = "solution"
        self._continuous_loop_sleep_interval = 0.01

        # in a thread
        self.executor.submit(self.listen_for_solutions)

    # def generate_tasks(self, random_no_min=10_000_000, random_no_max=100_000_000, sleep_interval=0.5):
    def generate_tasks(self, random_no_min=10_000, random_no_max=100_000, sleep_interval=0.5):
        for task_counter in range(1, self.no_of_tasks_to_produce + 1):
            if task_counter > 0 and task_counter % 10 == 0:
                print("Produced task : {}".format(task_counter))

            random_number = get_random_number(random_no_min, random_no_max)
            task_id = str(uuid.uuid4())
            # publish problem
            task = {'id': task_id, 'number': random_number}
            self.pubsub.publish(self._task_channel, json.dumps(task))
            sleep_interval = get_random_number(0, sleep_interval)
            time.sleep(sleep_interval)

    def release_resources(self):
        self.pubsub.close()
        self.executor.shutdown()

    def listen_for_solutions(self):
        solutions = []
        subscriber = self.pubsub.pubsub()
        subscriber.subscribe(self._solution_channel)
        min_task_started_at = None
        max_task_started_at = None
        while len(solutions) != 100:
            message = subscriber.get_message()

            if message and not message['data'] == 1:
                solution = json.loads(message['data'])
                solutions.append(solution)
                st_time = solution['st_time']
                end_time = solution['end_time']

                if not min_task_started_at or st_time < min_task_started_at:
                    min_task_started_at = st_time

                if not max_task_started_at or end_time > max_task_started_at:
                    max_task_started_at = end_time

                if len(solutions) % 10 == 0:
                    print("Consumed solution : {}".format(len(solutions)))
            else:
                self._continuous_loop_sleep_interval = 0.01
        print("Score : {}".format(1.0 / (max_task_started_at - min_task_started_at)))

        self.release_resources()


if __name__ == '__main__':
    configs = None
    with open('configs.json', 'r') as f:
        data = json.load(f)
    if not data:
        raise Exception("Invalid configuration")

    no_of_tasks = data["system_1"]["task_count"]
    random_no_min = data["system_1"]["random_no_min"]
    random_no_max = data["system_1"]["random_no_max"]

    system1 = System1(no_of_tasks_to_produce=no_of_tasks)
    system1.generate_tasks(random_no_min=random_no_min, random_no_max=random_no_max)