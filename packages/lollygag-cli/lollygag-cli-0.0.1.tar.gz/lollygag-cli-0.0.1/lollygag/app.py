from lollygag.vendor import npyscreen

from lollygag.ui.mainForm import MainForm
from lollygag.ui.taskEditForm import TaskEditForm
from lollygag.ui.viewEditForm import ViewEditForm

class LollygagApplication(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="My Tasks")
        self.addForm("EDIT_TASK_FORM", TaskEditForm, name="Create Task")
        self.addForm("EDIT_VIEW_FORM", ViewEditForm, name="Create View")