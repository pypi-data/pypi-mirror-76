from lollygag.vendor import npyscreen
from lollygag.vendor.npyscreen.wgmultiline import MultiLineAction
from lollygag.data.models import Task
import curses

class TaskBoxMultiLine(MultiLineAction):

    def __init__(self, *args, **keywords):
        super(TaskBoxMultiLine, self).__init__(*args, **keywords)
        self.add_handlers({
            "^X": self.when_delete_record,
            "^S": self.change_sort_status,
        })
    
    def display_value(self, task):
        return f'{task.title} ({task.readable_priority}) [{task.readable_status}]'

    def actionHighlighted(self, selected_task, key_press):
        self.parent.parentApp.getForm('EDIT_TASK_FORM').task = selected_task
        self.parent.parentApp.switchForm('EDIT_TASK_FORM')

    def when_delete_record(self, *args, **keywords):
        Task.delete(self.values[self.cursor_line])
        self.parent.parentApp.queue_event(npyscreen.Event("event_update_view"))

    def update_tasks(self, tasks):
        self.values = tasks

    def change_sort_status(self):
        pass

class TasksBox(npyscreen.BoxTitle):

    _contained_widget = TaskBoxMultiLine

    def __init__(self, *args, **keywords):
        super(TasksBox, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record
        })
        self.current_view = None

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDIT_TASK_FORM').task = None
        self.parent.parentApp.switchForm('EDIT_TASK_FORM')
    
    def update_view(self):
        if not self.current_view:
            self.name = "ALL"
            self.footer = "select * from tasks"
            self.entry_widget.update_tasks(Task.get_all())
        else:
            self.name = self.current_view.title
            self.footer = self.current_view.cropped_query
            self.entry_widget.update_tasks(self.current_view.get_tasks_for_view())