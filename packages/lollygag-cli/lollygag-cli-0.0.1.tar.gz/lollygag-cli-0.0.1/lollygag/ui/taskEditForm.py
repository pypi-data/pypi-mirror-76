from lollygag.vendor import npyscreen
from lollygag.data.models import Task
import curses

class TaskEditForm(npyscreen.ActionFormV2):

    _DESCRIPTION_DEFAULT_TEXT = """Additional Context"""

    def __init__(self, *args, **keywords):
        super(TaskEditForm, self).__init__(*args, **keywords)
        
        self.add_handlers({
            "^S": self.on_ok,
            155: self.on_cancel,
            curses.ascii.ESC: self.on_cancel,
            "^W": self.on_cancel
        })

    def create(self):

        self.task = None
        self.title  = self.add(npyscreen.TitleText, name = "Task:",)
        self.due = self.add(npyscreen.TitleDateCombo, name = "Due:")
        self.description = self.add(npyscreen.MultiLineEdit,
               value = self._DESCRIPTION_DEFAULT_TEXT, name="Description: ",
               max_height=5, rely=5)
        self.priority = self.add(npyscreen.TitleSelectOne, max_height=4, value = [0,], name="Priority: ",
                values = Task._PRIORITIES, scroll_exit=True)
        self.status = self.add(npyscreen.TitleSelectOne, max_height=4, value = [0,], name="Status: ",
                values = Task._STATUS, scroll_exit=True)
        self.tags = self.add(npyscreen.TitleMultiSelect, max_height =-2, value = [], name="Tags: ",
                values = [], scroll_exit=True)

    def beforeEditing(self):
        if self.task:
            self.title.value = self.task.title
            self.due.value = self.task.due
            self.description.value = self.task.description
            self.priority.value = [self.task.priority,]
            self.status.value = [self.task.status,]
            self.tags.value = []
        else:
            self.title.value = ""
            self.due.value = None
            self.description.value = TaskEditForm._DESCRIPTION_DEFAULT_TEXT
            self.priority.value = [0,]
            self.status.value = [0,]
            self.tags.value = []
    
    def on_ok(self, *args, **keywords):
        descr = self.description.value if self.description.value != self._DESCRIPTION_DEFAULT_TEXT else ""
        if self.task and self.task.id:
            self.task.title = self.title.value
            if self.due.value:
                self.task.due = self.due.value
            self.task.description = descr 
            self.task.priority = self.priority.value[0]
            self.task.status = self.status.value[0]
            self.task.save()
        else:
            t = Task(
                title=self.title.value,
                description=descr, 
                priority=self.priority.value[0],
                status=self.status.value[0])
            if self.due.value:
                t.due = self.due.value
            t.save()
        self.parentApp.queue_event(npyscreen.Event("event_complete_task_editing"))
        
    
    def on_cancel(self, *args, **keywords):
        self.parentApp.switchFormPrevious()
    
    @property
    def readable_tags(self):
        return [self.tags.values[x] for x in self.tags.value]