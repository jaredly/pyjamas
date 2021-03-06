"""
* Copyright 2008 Fred Sauer
*
* Licensed under the Apache License, Version 2.0 (the "License"); you may not
* use this file except in compliance with the License. You may obtain a copy of
* the License at
*
* http:#www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
* License for the specific language governing permissions and limitations under
* the License.
"""




"""*
* {@link com.allen_sauer.gwt.dnd.client.util.DOMUtil} implementation for
* IE.
"""
class DOMUtilImplIE6(DOMUtilImpl):
    def cancelAllDocumentSelections(self):
        JS("""
        try {
            $doc.selection.empty();
        } catch(e) {
            // ignore 'Unknown runtime error'
        }
        """)
    
    
    def getBorderLeft(self, elem):
        JS("""
        return elem.clientLeft;
        """)
    
    
    def getBorderTop(self, elem):
        JS("""
        return elem.clientTop;
        """)
    
    
    def getClientHeight(self, elem):
        JS("""
        return elem.clientHeight;
        """)
    
    
    def getClientWidth(self, elem):
        JS("""
        return elem.clientWidth;
        """)
    
    
    def isOrContains(self, parent, child):
        JS("""
        return (parent.uniqueID == child.uniqueID) || parent.contains(child);
        """)
    


