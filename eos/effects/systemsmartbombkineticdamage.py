# systemSmartBombKineticDamage
#
# Used by:
# Celestials named like: Red Giant Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "passive")


def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Smart Bomb",
                                     "kineticDamage", module.getModifiedItemAttr("smartbombDamageMultiplier"))
