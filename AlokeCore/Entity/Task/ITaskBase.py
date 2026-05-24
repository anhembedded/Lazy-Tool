class ITaskBase:
    def __init__(self, task_name: str, *args, **kwargs):
        self.task_name = task_name

    def execute(self):
        ...
    def __str__(self):
        return self.task_name