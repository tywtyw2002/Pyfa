# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("agility", module.getModifiedItemAttr("subsystemBonusAmarrPropulsion"),
                           skill="Amarr Propulsion Systems")
