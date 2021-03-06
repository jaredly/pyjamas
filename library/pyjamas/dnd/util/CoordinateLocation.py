"""
* Copyright 2007 Fred Sauer
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

import AbstractLocation

"""*
* A position represented by a left (x) and top (y) coordinate.
"""
class CoordinateLocation(AbstractLocation):
    
    def __init__(self, left, top):
        self.left = left
        self.top = top
    
    
    """
    * (non-Javadoc)
    *
    * @see com.allen_sauer.gwt.dnd.client.util.Location#getLeft()
    """
    def getLeft(self):
        return left
    
    
    """
    * (non-Javadoc)
    *
    * @see com.allen_sauer.gwt.dnd.client.util.Location#getTop()
    """
    def getTop(self):
        return top
    


