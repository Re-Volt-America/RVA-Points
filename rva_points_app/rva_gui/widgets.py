"""
Name: widgets.py
Author: https://gitlab.com/re-volt/rvgl-launcher/-/blob/master/rv_launcher/rvl_gui/widgets.py
"""

import wx
import wx.lib.scrolledpanel as scrolled
import wx.lib.mixins.listctrl as listmix
import sys

wxEVT_LIST_ITEM_CHECKED = wx.NewEventType()
wxEVT_LIST_ITEM_UNCHECKED = wx.NewEventType()
wxEVT_DROP_FILES = wx.NewEventType()

EVT_LIST_ITEM_CHECKED = wx.PyEventBinder(wxEVT_LIST_ITEM_CHECKED, 1)
EVT_LIST_ITEM_UNCHECKED = wx.PyEventBinder(wxEVT_LIST_ITEM_UNCHECKED, 1)
EVT_DROP_FILES = wx.PyEventBinder(wxEVT_DROP_FILES, 1)

class ListEvent(wx.PyCommandEvent):
    def __init__(self, event_type, item, value=None):
        wx.PyCommandEvent.__init__(self, event_type, -1)
        self.item = item
        self.value = value


class ListCtrl(wx.ListCtrl):
    def __init__(self, parent, widths, *args, **kwargs):
        wx.ListCtrl.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.default_widths = widths
        self.widths = []

        self.Bind(wx.EVT_SIZE, self.on_size)

    """ Cross-platform list scrolling functions """
    def get_scroll_pos(self):
        # return self.GetScrollPos(wx.VERTICAL)
        pos = self.GetTopItem() + self.GetCountPerPage() - 1
        return max(0, min(pos, self.GetItemCount() - 1))

    def set_scroll_pos(self, pos):
        # self.SetScrollPos(wx.VERTICAL, pos)
        if self.GetItemCount():
            pos = max(0, min(pos, self.GetItemCount() - 1))
            self.EnsureVisible(pos)

    """ Updates column widths based on item widths """
    def set_column_widths(self):
        widths = [20] * self.GetColumnCount()
        for i in range(len(widths)):
            # self.SetColumnWidth(i, wx.LIST_AUTOSIZE)
            # widths[i] = self.GetColumnWidth(i)
            for item in range(self.GetItemCount()):
                text = self.GetItemText(item, i)
                width = self.GetTextExtent(text).x + 10
                widths[i] = max(widths[i], width)

        if self.widths != widths:
            self.widths = widths
            self.on_size(None)

    """ Processes a list resize event """
    def on_size(self, e):
        # Windows requires processing the size event first before altering
        # column widths to prevent scrollbar from glitching up. Taken from
        # wx.ListCtrlAutoWidthMixin source.
        if e and sys.platform == "win32":
            wx.CallAfter(self.on_size, None)
            e.Skip()
            return

        window_width = self.GetClientSize().width
        count = min(len(self.widths), self.GetColumnCount())
        if not all([count, window_width]):
            self.on_event(e)
            return

        padding = window_width
        widths = [20] * count
        for i in range(count):
            min_width = self.default_widths[i] * 640 // 800
            max_width = self.default_widths[i] * window_width // 800
            widths[i] = min(max(self.widths[i], min_width), max_width)
            padding -= min(widths[i], padding)

        for i in range(count):
            delta = self.widths[i] - widths[i]
            delta = min(max(delta, 0), padding)
            widths[i] += delta
            padding -= delta

        widths[-1] += padding % count
        for i in range(count):
            widths[i] += padding // count
            self.SetColumnWidth(i, widths[i])

        self.on_event(e)

    """ Pass on an event after we're done """
    def on_event(self, e):
        e.Skip() if e else None


# TODO: Replace CheckListCtrlMixin with wxWidgets core functionality
# but only after version 3.1 hits stable.
class CheckListCtrl(ListCtrl, listmix.CheckListCtrlMixin):
    def __init__(self, parent, widths, *args, **kwargs):
        ListCtrl.__init__(self, parent, widths, *args, **kwargs)
        listmix.CheckListCtrlMixin.__init__(self)
        self.send_event = True

    def CheckItem(self, index, check=True, event=True):
        self.send_event = event
        listmix.CheckListCtrlMixin.CheckItem(self, index, check)
        self.send_event = True

    def OnCheckItem(self, index, flag):
        if not self.send_event:
            return

        event_types = (
            wxEVT_LIST_ITEM_UNCHECKED,
            wxEVT_LIST_ITEM_CHECKED
        )
        event = ListEvent(event_types[flag], index, flag)
        wx.PostEvent(self, event)


class TabBar(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)
        self.parent = parent


class TabPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.frame = parent.parent

    def Layout(self):
        if self.frame.GetSizer():
            wx.Panel.Layout(self)


class ScrolledTabPage(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)
        self.parent = parent
        self.frame = parent.parent

    def Layout(self):
        if self.frame.GetSizer():
            scrolled.ScrolledPanel.Layout(self)
            self.SetupScrolling(scroll_x=False)



class FileDropEvent(wx.PyCommandEvent):
    def __init__(self, event_type, x, y, filenames):
        wx.PyCommandEvent.__init__(self, event_type, -1)
        self.x = x
        self.y = y
        self.filenames = filenames


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, parent):
        wx.FileDropTarget.__init__(self)
        self.parent = parent

    """ Listener for dropped files """
    def OnDropFiles(self, x, y, filenames):
        event = FileDropEvent(wxEVT_DROP_FILES, x, y, filenames)
        wx.PostEvent(self.parent, event)
        return True

