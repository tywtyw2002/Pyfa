import wx

from gui.cachingImageList import CachingImageList
import gui.builtinMarketBrowser.events as events

from logbook import Logger

pyfalog = Logger(__name__)


class MarketTree(wx.TreeCtrl):
    def __init__(self, parent, marketBrowser):
        wx.TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
        pyfalog.debug("Initialize marketTree")
        self.root = self.AddRoot("root")

        self.imageList = CachingImageList(16, 16)
        self.SetImageList(self.imageList)

        self.sMkt = marketBrowser.sMkt
        self.marketBrowser = marketBrowser

        # Form market tree root
        sMkt = self.sMkt
        for mktGrp in sMkt.getMarketRoot():
            iconId = self.addImage(sMkt.getIconByMarketGroup(mktGrp))
            mkt_name = "%s(%s)" % (mktGrp.name, mktGrp.chs_name)
            childId = self.AppendItem(self.root, mkt_name, iconId, data=wx.TreeItemData(mktGrp.ID))
            # childId = self.AppendItem(self.root, mktGrp.name, iconId, data=wx.TreeItemData(mktGrp.ID))
            # All market groups which were never expanded are dummies, here we assume
            # that all root market groups are expandable
            self.AppendItem(childId, "dummy")
        self.SortChildren(self.root)

        # Add recently used modules node
        rumIconId = self.addImage("market_small", "gui")
        self.AppendItem(self.root, "Recently Used Modules", rumIconId, data=wx.TreeItemData(events.RECENTLY_USED_MODULES))

        # Bind our lookup method to when the tree gets expanded
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)

    def addImage(self, iconFile, location="icons"):
        if iconFile is None:
            return -1
        return self.imageList.GetImageIndex(iconFile, location)

    def expandLookup(self, event):
        """Process market tree expands"""
        root = event.Item
        child = self.GetFirstChild(root)[0]
        # If child of given market group is a dummy
        if self.GetItemText(child) == "dummy":
            # Delete it
            self.Delete(child)
            # And add real market group contents
            sMkt = self.sMkt
            currentMktGrp = sMkt.getMarketGroup(self.GetPyData(root), eager="children")
            for childMktGrp in sMkt.getMarketGroupChildren(currentMktGrp):
                # If market should have items but it doesn't, do not show it
                if sMkt.marketGroupValidityCheck(childMktGrp) is False:
                    continue
                iconId = self.addImage(sMkt.getIconByMarketGroup(childMktGrp))
                try:
                    # childId = self.AppendItem(root, childMktGrp.name, iconId, data=wx.TreeItemData(childMktGrp.ID))
                    mkt_name = "%s(%s)" % (childMktGrp.name, childMktGrp.chs_name)
                    childId = self.AppendItem(root, mkt_name, iconId, data=wx.TreeItemData(childMktGrp.ID))
                except Exception as e:
                    pyfalog.debug("Error appending item.")
                    pyfalog.debug(e)
                    continue
                if sMkt.marketGroupHasTypesCheck(childMktGrp) is False:
                    self.AppendItem(childId, "dummy")

            self.SortChildren(root)

    def jump(self, item):
        """Open market group and meta tab of given item"""
        self.marketBrowser.searchMode = False
        sMkt = self.sMkt
        mg = sMkt.getMarketGroupByItem(item)

        jumpList = []
        while mg is not None:
            jumpList.append(mg.ID)
            mg = mg.parent

        for id in sMkt.ROOT_MARKET_GROUPS:
            if id in jumpList:
                jumpList = jumpList[:jumpList.index(id) + 1]

        item = self.root
        for i in range(len(jumpList) - 1, -1, -1):
            target = jumpList[i]
            child, cookie = self.GetFirstChild(item)
            while self.GetItemPyData(child) != target:
                child, cookie = self.GetNextChild(item, cookie)

            item = child
            self.Expand(item)

        self.SelectItem(item)
        self.marketBrowser.itemView.selectionMade()
