from lollygag.vendor import npyscreen
from lollygag.data.models import View
import curses

class ViewEditForm(npyscreen.ActionFormV2):

    __DEFAULT_QUERY = "select * from tasks"

    def __init__(self, *args, **keywords):
        super(ViewEditForm, self).__init__(*args, **keywords)
        
        self.add_handlers({
            "^S": self.on_ok,
            155: self.on_cancel,
            curses.ascii.ESC: self.on_cancel,
            "^W": self.on_cancel
        })

    def create(self):

        self.view = None
        self.title  = self.add(npyscreen.TitleText, name = "View Title:",)
        self.query = self.add(npyscreen.TitleText, name = "View Query:")
        self.sort_order = self.add(npyscreen.TitleText, name = "Sort Order:")

    def beforeEditing(self):
        if self.view:
            self.title.value = self.view.title
            self.query.value = self.view.query
            self.sort_order.value = str(self.view.sort_order)
        else:
            self.title.value = ""
            self.query.value = ""
            self.sort_order.value = "0"
    
    def on_ok(self, *args, **keywords):
        query = self.query.value if len(self.query.value) else __DEFAULT_QUERY
        if self.view and self.view.id:
            self.view.title = self.title.value
            self.view.query = query
            self.view.sort_order = self.sort_order.value
            self.view.save()
        else:
            v = View(
                title=self.title.value,
                query=query,
                sort_order=self.sort_order.value)
            v.save()
        self.parentApp.queue_event(npyscreen.Event("event_complete_view_editing"))
        
    
    def on_cancel(self, *args, **keywords):
        self.parentApp.switchFormPrevious()