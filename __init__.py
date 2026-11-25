import os
from cudatext import *

class Command:
    def __init__(self):
        self.saved_ed_titles = {}

    def on_start2(self, ed_self):
        app_proc(PROC_EVENTS_SUB, 'cuda_tab_pin;on_state_ed;;')

    def on_state_ed(self, ed_self, state):
        if state == EDSTATE_PINNED:
            self.set_index_tab(ed_self)
            self.update_title(ed_self)

    def set_index_tab(self, ed_self):
        ed_self.set_prop(PROP_INDEX_TAB, self.get_tab_index(ed_self))

    def get_tab_index(self, ed_self):
        for h in ed_handles():
            e = Editor(h)
            if not e.get_prop(PROP_TAB_PINNED) or (e.get_prop(PROP_TAB_PINNED) and e == ed_self):
                return e.get_prop(PROP_INDEX_TAB)

    def update_title(self, ed_self):
        fn = ed_self.get_filename()
        if not fn:
            return

        h = ed_self.get_prop(PROP_HANDLE_SELF)
        pinned = ed_self.get_prop(PROP_TAB_PINNED)
        title = ed_self.get_prop(PROP_TAB_TITLE)

        if pinned:
            if title not in ['', ' ']:
                self.saved_ed_titles[h] = title
                new_title = ' '
            else:
                new_title = title
        else:
            new_title = self.saved_ed_titles.get(h, os.path.basename(fn))

        ed_self.set_prop(PROP_TAB_TITLE, new_title)
