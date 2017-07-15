# coding: utf-8
# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

# noinspection PyPackageRequirements
import wx
from logbook import Logger
from eos.saveddata.cargo import Cargo
from eos.saveddata.implant import Implant
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.module import Module, Slot, Rack
from eos.saveddata.fit import Fit
from service.fit import Fit as FitSvc
from gui.viewColumn import ViewColumn
import gui.mainFrame

pyfalog = Logger(__name__)


class BaseName(ViewColumn):
    name = "Base Name"

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.columnText = "Name"
        self.shipImage = fittingView.imageList.GetImageIndex("ship_small", "gui")
        self.mask = wx.LIST_MASK_TEXT
        self.projectedView = isinstance(fittingView, gui.builtinAdditionPanes.projectedView.ProjectedView)

    def try_chs_name(self, item):
        if getattr(item, "chs_name", None):
            return "%s(%s)" % (item.name, item.chs_name)
        else:
            return item.name

    def getText(self, stuff):
        if isinstance(stuff, Drone):
            # return "%dx %s" % (stuff.amount, stuff.item.name)
            return "%dx %s" % (stuff.amount, self.try_chs_name(stuff.item))
        elif isinstance(stuff, Fighter):
            return "%d/%d %s" % \
                   (stuff.amountActive, 
                    stuff.getModifiedItemAttr("fighterSquadronMaxSize"),
                    self.try_chs_name(stuff.item))
        elif isinstance(stuff, Cargo):
            # return "%dx %s" % (stuff.amount, stuff.item.name)
            return "%dx %s" % (stuff.amount, self.try_chs_name(stuff.item))
        elif isinstance(stuff, Fit):
            if self.projectedView:
                # we need a little more information for the projected view
                fitID = self.mainFrame.getActiveFit()
                info = stuff.getProjectionInfo(fitID)

                if info:
                    return "%dx %s (%s)" % (stuff.getProjectionInfo(fitID).amount, stuff.name, stuff.ship.item.name)

                pyfalog.warning("Projected View trying to display things that aren't there. stuff: {}, info: {}", repr(stuff),
                                info)
                return "<unknown>"
            else:
                return "%s (%s)" % (stuff.name, stuff.ship.item.name)
        elif isinstance(stuff, Rack):
            if FitSvc.getInstance().serviceFittingOptions["rackLabels"]:
                if stuff.slot == Slot.MODE:
                    return u'─ Tactical Mode ─'
                else:
                    return u'─ {} Slots ─'.format(Slot.getName(stuff.slot).capitalize())
            else:
                return ""
        elif isinstance(stuff, Module):
            if stuff.isEmpty:
                return "%s Slot" % Slot.getName(stuff.slot).capitalize()
            else:
                # return stuff.item.name
                return self.try_chs_name(stuff.item)
        elif isinstance(stuff, Implant):
            # return stuff.item.name
            return self.try_chs_name(stuff.item)
        else:
            item = getattr(stuff, "item", stuff)

            # hack chs name
            ret_name = self.try_chs_name(item)

            if FitSvc.getInstance().serviceFittingOptions["showMarketShortcuts"]:
                marketShortcut = getattr(item, "marketShortcut", None)

                if marketShortcut:
                    # use unicode subscript to display shortcut value
                    shortcut = unichr(marketShortcut + 8320) + u" "
                    del item.marketShortcut
                    return shortcut + ret_name
                    # return shortcut + item.name

            # return item.name
            return ret_name


BaseName.register()
