from abc import ABC, abstractmethod
from argparse import _SubParsersAction

from app.json_manager import read_file, write_file
from app.task import Task


class BaseCommand(ABC):
    name = "Base Command"
    description = "Base Command Description"
    help_text = "Base Command Help Text"
    success_message = "Base Command Success Message"
    error_message = "Base Command Error Message"

    def __init__(self, data: dict = {}):
        self.data = data
        self.parser = None

    @abstractmethod
    def install(self, parser: _SubParsersAction):
        pass

    def validate(self):
        """Return True or Raise Exception"""
        return True

    def add_data(self, data: dict):
        self.data.update(data)

    @abstractmethod
    def _run(self):
        pass

    def print_success_message(self):
        print(self.success_message)

    def print_error_message(self):
        print(self.error_message)

    def run(self):
        self.validate()
        try:
            self._run()
            self.print_success_message()
        except Exception as e:
            print(f"Error: {e}")
            self.print_error_message()
            return


class AddCommand(BaseCommand):
    name = "add"
    description = "Add Tasks"
    help_text = "You can add tasks using this command"
    success_message = "Task Added Successfully"
    error_message = "Error Adding Task"

    def install(self, parser: _SubParsersAction):
        self.parser = parser.add_parser(self.name, help=self.help_text)
        self.parser.add_argument("name", type=str, help="Task to be added")
        self.parser.add_argument("-d", "--description", help="Description of the task")

    def _run(self):
        objs = read_file() or []
        task = Task.create(**self.data)
        objs.append(task.model_dump())
        write_file(objs)


class ListCommand(BaseCommand):
    name = "list"
    description = "List Tasks"
    help_text = "You can list tasks using this command"
    success_message = "Task List"
    error_message = "Error Listing Tasks"

    def install(self, parser: _SubParsersAction):
        self.parser = parser.add_parser(self.name, help=self.help_text)
        self.parser.add_argument("-s", "--status", help="Filter tasks by status")

    def _run(self):
        objs = read_file() or []
        count = 0
        for obj in objs:
            task = Task(**obj)
            if task.status == self.data.get("status", task.status):
                print(task)
                count += 1
        if count == 0:
            print("No tasks found")


class UpdateCommand(BaseCommand):
    name = "update"
    description = "Update Task"
    help_text = "You can update tasks using this command"

    def install(self, parser: _SubParsersAction):
        self.parser = parser.add_parser(self.name, help=self.help_text)
        self.parser.add_argument("id", type=int, help="Task to be updated")
        self.parser.add_argument("-t", "--task", help="New task name")
        self.parser.add_argument(
            "-d", "--description", help="New description of the task"
        )
        self.parser.add_argument(
            "-s",
            "--status",
            help="New status of the task",
            choices=["todo", "done", "doing"],
        )

    def _run(self):
        task_list = read_file() or []
        old = None
        for task in task_list:
            if task["id"] == self.data["id"]:
                task_obj = Task(**task)
                task_obj.update(
                    new_name=self.data["task"],
                    new_description=self.data["description"],
                    new_status=self.data["status"],
                )
                old = task

        # delete the old task
        # add the new task
        print(task_list)
        if old:
            task_list.remove(old)
            task_list.append(task_obj.model_dump())
        else:
            print("Task not found")

        print(task_list)
        write_file(task_list)


class DeleteCommand(BaseCommand):
    name = "delete"
    description = "Delete Task"
    help_text = "You can delete tasks using this command"
    success_message = "Task Deleted Successfully"
    error_message = "Error Deleting Task"

    def install(self, parser: _SubParsersAction):
        self.parser = parser.add_parser(self.name, help=self.help_text)
        self.parser.add_argument("id", type=int, help="Task to be deleted")

    def _run(self):
        task_list = read_file() or []
        old = None
        for task in task_list:
            if task["id"] == self.data["id"]:
                old = task

        # delete the old task
        if old:
            task_list.remove(old)

        write_file(task_list)


class MarkDoneCommand(BaseCommand):
    name = "mark-done"
    description = "Mark Task as Done"
    help_text = "You can mark tasks as done using this command"
    success_message = "Task Marked as Done Successfully"
    error_message = "Error Marking Task as Done"

    def install(self, parser: _SubParsersAction):
        self.parser = parser.add_parser(self.name, help=self.help_text)
        self.parser.add_argument("id", type=int, help="Task to be marked as done")

    def _run(self):
        task_list = read_file() or []
        old = None
        for task in task_list:
            if task["id"] == self.data["id"]:
                task_obj = Task(**task)
                task_obj.update(new_status="done")
                old = task

        # delete the old task
        # add the new task
        if old:
            task_list.remove(old)
            task_list.append(task_obj.model_dump())

        write_file(task_list)


class MarkDoingCommand(BaseCommand):
    name = "mark-doing"
    description = "Mark Task as Doing"
    help_text = "You can mark tasks as doing using this command"
    success_message = "Task Marked as Doing Successfully"
    error_message = "Error Marking Task as Doing"

    def install(self, parser: _SubParsersAction):
        self.parser = parser.add_parser(self.name, help=self.help_text)
        self.parser.add_argument("id", type=int, help="Task to be marked as doing")

    def _run(self):
        task_list = read_file() or []
        old = None
        for task in task_list:
            if task["id"] == self.data["id"]:
                task_obj = Task(**task)
                task_obj.update(new_status="doing")
                old = task

        # delete the old task
        # add the new task
        if old:
            task_list.remove(old)
            task_list.append(task_obj.model_dump())

        write_file(task_list)
