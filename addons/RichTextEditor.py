"""
    A rich text editor using FCKeditor.
    
    Pass "-j fckeditor/fckeditor.js" to build.py in order to include the FCKeditor
    javascript.
"""
from pyjamas import Window
from pyjamas import DOM
from __pyjamas__ import console
from BoundMethod import BoundMethod
from pyjamas.ui.Widget import Widget

from __pyjamas__ import JS

def createFCK(name):
    JS("""
    return new FCKeditor(name);
    """)

JS("""
    $wnd.FCKeditor_OnComplete = function(editorInstance )
    {
        pyjsObject = $doc.getElementById(editorInstance.Name.substr(3)).__listener;
        console.log("pyjsObject is %o", pyjsObject);
        if(pyjsObject)
            pyjsObject.onFCKLoaded(editorInstance);
    }
""")
class RichTextEditor(Widget):
    def __init__(self, initialValue="", target="", method="POST"):
        Widget.__init__(self);
        self.id = "rte"+hash(self)
        fck = createFCK("fck"+self.id)
        fck.Height = "600px"
        self.setElement(DOM.createForm())
        DOM.setAttribute(self.element, "method", "POST")
        DOM.setAttribute(self.element, "target", target)
        JS("""
        var rte = this;
        this.element.onsubmit = function() {
            $wnd.setTimeout(function() { rte.onSave.call(rte) }, 0);
            return false;
        }
        """)
        self.setID(self.id)
        self.addStyleName("gwt-RichTextEditor")
        fck.Value = initialValue
        fck.BasePath = "fckeditor/"
        fck.Config.CustomConfigurationsPath = "../../fckconfig.js"
        fck.pyjsObject = self
        self.loaded = False
        self.saveListeners = []
        self.pendingHTML = None
        html = fck.CreateHtml()
        #console.log("fck html = %s", html)
        html = html
        DOM.setInnerHTML(self.getElement(), html)
    
    def addSaveListener(self, listener):
        """
        When the user clicks the save button, your listener will be notified.
        
        Either pass a function (e.g. a BoundMethod) or an object with an onSave()
        method.  Either will be passed the RichtTextEditor instance.
        """
        self.saveListeners.append(listener)
        
    def removeSaveListener(self, listener):
        """
        Remove a previously added listener
        """
        self.saveListeners.remove(listener)
    
    def onFCKLoaded(self, fck):
        """
        Called when the FCK editor has loaded, and it is ready for use
        """
        self.loaded = True
        self.fck = fck
        fck.Events.AttachEvent('OnSelectionChange', BoundMethod(self, self.onSelectionChange))
        fck.Events.AttachEvent('OnBlur', BoundMethod(self, self.onBlur))
        fck.Events.AttachEvent('OnFocus', BoundMethod(self, self.onFocus))
        fck.Events.AttachEvent('OnPaste', BoundMethod(self, self.onPaste))
        if self.pendingHTML:
            fck.SetHTML(self.pendingHTML)
            self.pendingHTML = None
            
    def onSelectionChange(self, sender):
        pass#console.log("onSelectionChange!")
        
    def onBlur(self, sender):
        pass#console.log("onBlur!")
        
    def onFocus(self, sender):
        pass#console.log("onFocus!")
        
    def onPaste(self, sender):
        pass#console.log("onPaste!")
        
    def onSave(self):
        """
        Handle the save click and pass it onto the listeners
        """
        console.log("onSave() in %s", Window.getLocation().getHref())
        for listener in self.saveListeners:
            if listener.onSave: listener.onSave(self)
            else: listener(self)
        return False
    
    def setHTML(self, html):
        """
        Call this to change the html showing in the editor
        """
        if self.loaded:
            self.fck.SetHTML(html);
        else:
            self.pendingHTML = html
    
    def getHTML(self):
        """
        Call this to retrieve the HTML showing in the editor (e.g. to save/preview it)
        """
        return self.fck.GetXHTML(True)

    def getDOM(self):
        return self.fck.EditorDocument()
    
    def getWindow(self):
        return self.fck.EditorWindow()
    

