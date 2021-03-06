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




"""*
* Shared String utility methods.
"""
class StringUtil:
    """*
    * Return short classname of <code>obj</code> based on
    * string returned by {@link GWT#getTypeName(Object)}.
    *
    * @param obj the object whose name is to be determined
    * @return the short class name
    """
    def getShortTypeName(self, obj):
        typeName = GWT.getTypeName(obj)
        return typeName.substring(typeName.lastIndexOf('.') + 1)
    


