from lollygag.vendor import npyscreen
from lollygag.vendor.npyscreen.wgmultiline import MultiLineAction
from lollygag.data.models import View

class ViewBoxMultiLine(MultiLineAction):

    def __init__(self, *args, **keywords):
        super(ViewBoxMultiLine, self).__init__(*args, **keywords)
    
    def display_value(self, view):
        return f'> {view.title}'

    def update_views(self):
        self.values = View.get_all()

    def actionHighlighted(self, selected_view, key_press):
        e = npyscreen.Event("event_selected_view")
        e.selected_view = selected_view
        self.parent.parentApp.queue_event(e)
    
    def cur_highlighted_view(self):
        return self.values[self.cursor_line]

class ViewsBox(npyscreen.BoxTitle):

    _contained_widget = ViewBoxMultiLine

    def __init__(self, *args, **keywords):
        super(ViewsBox, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^E": self.when_edit_record
        })

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDIT_VIEW_FORM').task = None
        self.parent.parentApp.switchForm('EDIT_VIEW_FORM')
    
    def when_edit_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDIT_VIEW_FORM').view = self.entry_widget.cur_highlighted_view()
        self.parent.parentApp.switchForm('EDIT_VIEW_FORM')

    def update_view(self):
        self.entry_widget.update_views()