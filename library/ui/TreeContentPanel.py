# Copyright 2006 James Tauber and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pyjamas import DOM
from pyjamas.ui.SimplePanel import SimplePanel

class TreeContentPanel(SimplePanel):
    def __init__(self, element):
        SimplePanel.__init__(self, element)
        self.tree_item = None

    def getTreeItem(self):
        return self.tree_item

    def setTreeItem(self, tree_item):
        self.tree_item = tree_item

    def setParent(self, widget):
        # throw new UnsupportedOperationException("Cannot directly setParent on a WidgetTreeItem's ContentPanel");
        console.error("Cannot directly setParent on a WidgetTreeItem's ContentPanel")

    def treeSetParent(self, widget):
        SimplePanel.setParent(self, widget)


