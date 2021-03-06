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


from pyjamas.dnd.util import StringUtil



"""*
* Common implementation class for {@link DragStartEvent} and {@link DragEndEvent}.
"""
abstract class DragEvent extends EventObject:
    transient DragContext context
    
    def __init__(self, context):
        super(context.draggable)
        self.context = context
    
    
    """*
    * Get the drag context for the drag operation.
    *
    * @return the drag context
    """
    def getContext(self):
        return context
    
    
    def getSourceShortTypeName(self):
        return StringUtil.getShortTypeName(getSource())
    


