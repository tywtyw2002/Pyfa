#===============================================================================
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
#===============================================================================

import wx
import wx.lib.newevent
import controller
import gui.mainFrame
import gui.builtinViewColumns.display as d
import sys
from eos.types import Slot

FitChanged, FIT_CHANGED = wx.lib.newevent.NewEvent()

class FittingView(d.Display):
    DEFAULT_COLS = ["Module state",
                    "Module name/slot",
                    "attr:power",
                    "attr:cpu",
                    "attr:capacitorNeed",
                    "attr:trackingSpeed",
                    "Max range"]

    def __init__(self, parent):
        d.Display.__init__(self, parent)
        self.mainFrame.Bind(FIT_CHANGED, self.fitChanged)
        self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.Hide() #Don't show ourselves at start
        self.activeFitID = None
        self.ignore = False

    #Gets called from the fitMultiSwitch when it decides its time
    def changeFit(self, fitID):
        self.activeFitID = fitID
        if fitID == None:
            self.Hide()
        else:
            self.Show()

        self.ignore = True
        wx.PostEvent(self.mainFrame, FitChanged(fitID=fitID))
        self.ignore = False
        self.slotsChanged()

    def appendItem(self, itemID):
        fitID = self.activeFitID
        if fitID != None:
            cFit = controller.Fit.getInstance()
            cFit.appendModule(fitID, itemID)
            self.ignore = True
            wx.PostEvent(self.mainFrame, FitChanged(fitID=fitID))
            self.ignore = False
            self.slotsChanged()

    def removeItem(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            cFit = controller.Fit.getInstance()
            trigger = cFit.removeModule(self.activeFitID, self.mods[self.GetItemData(row)].position)

            if trigger:
                self.ignore = True
                wx.PostEvent(self.mainFrame, FitChanged(fitID=self.activeFitID))
                self.ignore = False
                self.slotsChanged()

    def generateMods(self):
        cFit = controller.Fit.getInstance()
        fit = cFit.getFit(self.activeFitID)

        slotOrder = [Slot.SUBSYSTEM, Slot.HIGH, Slot.MED, Slot.LOW, Slot.RIG]

        if fit is not None:
            self.mods = fit.modules[:]
            self.mods.sort(key=lambda mod: (slotOrder.index(mod.slot), mod.position))
        else:
            self.mods = None

    def slotsChanged(self):
        self.generateMods()
        self.populate(self.mods)

    def fitChanged(self, event):
        if self.ignore:
            return

        self.generateMods()
        self.refresh(self.mods)
        event.Skip()
