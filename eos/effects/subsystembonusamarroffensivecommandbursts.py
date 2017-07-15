# subSystemBonusAmarrOffensiveCommandBursts
#
# Used by:
# Subsystem: Legion Offensive - Support Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "buffDuration", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Skirmish Command"),
                                  "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                  "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                  "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                  "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                  "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Armored Command"),
                                  "buffDuration", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")

    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                  "warfareBuff3Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                  "warfareBuff1Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                  "warfareBuff2Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                  "buffDuration", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"),
                                  "warfareBuff4Value", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
