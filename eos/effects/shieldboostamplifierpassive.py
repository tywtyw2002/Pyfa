# shieldBoostAmplifierPassive
#
# Used by:
# Implants named like: Agency Tank Booster (3 of 3)
# Implants named like: grade Crystal (15 of 18)
type = "passive"


def handler(fit, container, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", container.getModifiedItemAttr("shieldBoostMultiplier"))
