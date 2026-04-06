# This acts as your temporary database for Week 1
tasks_db = []

class TaskCounter:
    def __init__(self):
        self.count = 0

    def next_id(self):
        self.count += 1
        return self.count

counter = TaskCounter()