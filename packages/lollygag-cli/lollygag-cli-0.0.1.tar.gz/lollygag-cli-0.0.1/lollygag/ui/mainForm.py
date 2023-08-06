from lollygag.vendor import npyscreen
from lollygag.ui.tasksBox import TasksBox
from lollygag.ui.viewsBox import ViewsBox

class MainForm(npyscreen.FormBaseNew):

    def create(self):

        self.current_view = None

        self.add_event_hander("event_complete_task_editing", self.did_complete_editing)
        self.add_event_hander("event_complete_view_editing", self.did_complete_editing)
        self.add_event_hander("event_selected_view", self.did_select_view)

        y, x = self.useable_space()

        self.viewsBoxComponent = self.add(
            ViewsBox, 
            name="Views", 
            value=0, 
            relx=1, 
            max_width=x // 5, 
            rely=2,
        )

        self.tasksBoxComponent = self.add(
            TasksBox, 
            name="Tasks",
            footer = "sort: [id desc], filters: []",
            value=0,
            rely=2, 
            relx=(x // 5) + 1,
        )
        
        self.update_views()

    def did_complete_editing(self, event):
        self.parentApp.switchFormPrevious()
        self.update_views()

    def did_select_view(self, event):
        self.tasksBoxComponent.current_view = event.selected_view
        self.update_views()

    def update_views(self):
        self.tasksBoxComponent.update_view()
        self.tasksBoxComponent.display()
        self.viewsBoxComponent.update_view()
        self.viewsBoxComponent.display()
        