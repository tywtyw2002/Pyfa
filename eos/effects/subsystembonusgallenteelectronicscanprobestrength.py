# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Scanner Probe",
                                    "baseSensorStrength",
                                    module.getModifiedItemAttr("subsystemBonusGallenteElectronic"),
                                    skill="Gallente Electronic Systems")
