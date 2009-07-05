from pyjamas.ui.Button import Button
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.PopupPanel import PopupPanel
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.HTML import HTML
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui.DialogBox import DialogBox
from pyjamas.ui.Frame import Frame
from pyjamas.ui import HasAlignment
from pyjamas.ui.Composite import Composite
from pyjamas.ui.Panel import Panel
from pyjamas.ui.SimplePanel import SimplePanel
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.FlexTable import FlexTable
from pyjamas.ui import HasHorizontalAlignment
from pyjamas.ui import HasVerticalAlignment
from pyjamas.ui.Image import Image
from pyjamas import Window
from pyjamas import DOM

modal_popups = {}

def ModalPopupActive(title):
    global modal_popups
    return modal_popups.has_key(title)

def ModalPopupCloseAll():
    global modal_popups
    while len(modal_popups) > 0:
        k = modal_popups.keys()[0]
        modal_popups[k].hide()

class DialogBoxModal(PopupPanel):
    def __init__(self, identifier, autoHide=None, modal=False, rootpanel=None):
        PopupPanel.__init__(self, autoHide, modal, rootpanel)

        self.identifier = identifier
        self.caption = HTML()
        self.child = None
        self.showing = False
        self.dragging = False
        self.dragStartX = 0
        self.dragStartY = 0
        self.panel = FlexTable()
        
        self.closeButton = Image("images/cancel.png")
        self.closeButton.addClickListener(self)
        dock = DockPanel()
        dock.setSpacing(0)
        
        dock.add(self.closeButton, DockPanel.EAST)
        dock.add(self.caption, DockPanel.WEST)
        
        dock.setCellHorizontalAlignment(self.closeButton, HasAlignment.ALIGN_RIGHT)
        dock.setCellHorizontalAlignment(self.caption, HasAlignment.ALIGN_LEFT)
        dock.setCellWidth(self.caption, "100%")
        dock.setWidth("100%")

        self.panel.setWidget(0, 0, dock)
        self.panel.setHeight("100%")
        self.panel.setBorderWidth(0)
        self.panel.setCellPadding(0)
        self.panel.setCellSpacing(0)
        self.panel.getCellFormatter().setHeight(1, 0, "100%")
        self.panel.getCellFormatter().setWidth(1, 0, "100%")
        #self.panel.getCellFormatter().setAlignment(1, 0, HasHorizontalAlignment.ALIGN_CENTER, HasVerticalAlignment.ALIGN_MIDDLE)
        PopupPanel.setWidget(self, self.panel)

        self.setStyleName("gwt-DialogBox")
        self.caption.setStyleName("Caption")
        self.closeButton.setStyleName("Close")
        dock.setStyleName("Header")
        self.caption.addMouseListener(self)

    def getHTML(self):
        return self.caption.getHTML()

    def getText(self):
        return self.caption.getText()

    def onMouseDown(self, sender, x, y):
        self.dragging = True
        DOM.setCapture(self.caption.getElement())
        self.dragStartX = x
        self.dragStartY = y

    def onMouseEnter(self, sender):
        pass

    def onMouseLeave(self, sender):
        pass

    def onMouseMove(self, sender, x, y):
        if self.dragging:
            absX = x + self.getAbsoluteLeft()
            absY = y + self.getAbsoluteTop()
            self.setPopupPosition(absX - self.dragStartX, absY - self.dragStartY)

    def onMouseUp(self, sender, x, y):
        self.dragging = False
        DOM.releaseCapture(self.caption.getElement())

    def remove(self, widget):
        if self.child != widget:
            return False

        self.panel.remove(widget)
        self.child = None
        return True

    def setHTML(self, html):
        self.caption.setHTML(html)

    def setText(self, text):
        self.caption.setText(text)

    def doAttachChildren(self):
        PopupPanel.doAttachChildren(self)
        self.caption.onAttach()

    def doDetachChildren(self):
        PopupPanel.doDetachChildren(self)
        self.caption.onDetach()

    def setWidget(self, widget):
        if self.child is not None:
            self.panel.remove(self.child)

        if widget is not None:
            self.panel.setWidget(1, 0, widget)

        self.child = widget

    def createElement(self):
        return DOM.createDiv()

    def setPopupPosition(self, left, top):
        if left < 0:
            left = 0
        if top < 0:
            top = 0

        element = self.getElement()
        DOM.setStyleAttribute(element, "left", "%dpx" % left )
        DOM.setStyleAttribute(element, "top", "%dpx" % top)

    def show(self):
        if self.showing:
            return

        global modal_popups
        if modal_popups.has_key(self.identifier) and \
           modal_popups[self.identifier] != self:
            return
        modal_popups[self.identifier] = self

        PopupPanel.show(self)

    def hide(self, autoClosed=False):
        if not self.showing:
            return

        global modal_popups
        if modal_popups.has_key(self.identifier):
            del modal_popups[self.identifier]

        PopupPanel.hide(self)

    def onEventPreview(self, event):
        # preventDefault on mousedown events, outside of the
        # dialog, to stop text-selection on dragging
        type = DOM.eventGetType(event)
        if type == 'mousedown':
            target = DOM.eventGetTarget(event)
            elem = self.caption.getElement()
            event_targets_popup = target and DOM.isOrHasChild(elem, target)
            if event_targets_popup:
                DOM.eventPreventDefault(event)
        return PopupPanel.onEventPreview(self, event)

class PopupFrame(DialogBoxModal):

    def __init__(self, identifier, title, iframe):

        global modal_popups
        if modal_popups.has_key(identifier):
            return
        modal_popups[identifier] = self

        DialogBoxModal.__init__(self, identifier)

        self.setText(title)

        self.iframe = iframe
        #closeButton = Button("Close", self)
        #msg = HTML("<center>IFRAME:</center>", True)
        self.iframe.setStyleName("gwt-DialogFrame")
        
        self.dock = DockPanel()
        self.dock.setSpacing(4)
        
        #dock.add(closeButton, DockPanel.SOUTH)
        #dock.add(msg, DockPanel.NORTH)
        self.dock.add(self.iframe, DockPanel.CENTER)
        
        #dock.setCellHorizontalAlignment(closeButton, HasAlignment.ALIGN_RIGHT)
        self.dock.setCellWidth(self.iframe, "100%")
        self.dock.setWidth("100%")
        #self.iframe.setWidth("320px")
        #self.iframe.setHeight("200px")
        self.setWidget(self.dock)

    def setUrl(self, url):
        self.iframe.setUrl(url)

    def onClick(self, sender):
        self.hide()

    def set_width(self, width):

        self.iframe.setWidth("%dpx" % width) 

    def set_height(self, height):
        self.iframe.setHeight("%dpx" % height)


class Popup(PopupFrame):

    def __init__(self, identifier, title, frame_page=""):
        PopupFrame.__init__(self, identifier, title, Frame(frame_page))

