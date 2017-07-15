# Not used by any item
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff3Value",
                                  src.getModifiedItemAttr("subsystemBonusAmarrDefensive"),
                                  skill="Amarr Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff2Value",
                                  src.getModifiedItemAttr("subsystemBonusAmarrDefensive"),
                                  skill="Amarr Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff4Value",
                                  src.getModifiedItemAttr("subsystemBonusAmarrDefensive"),
                                  skill="Amarr Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "buffDuration",
                                  src.getModifiedItemAttr("subsystemBonusAmarrDefensive"),
                                  skill="Amarr Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"), "warfareBuff1Value",
                                  src.getModifiedItemAttr("subsystemBonusAmarrDefensive"),
                                  skill="Amarr Defensive Systems")
