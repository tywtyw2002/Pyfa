# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxTractorVelocity", module.getModifiedItemAttr("subsystemBonusMinmatarElectronic2"),
                                  skill="Minmatar Electronic Systems")
