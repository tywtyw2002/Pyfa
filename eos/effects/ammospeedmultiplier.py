# ammoSpeedMultiplier
#
# Used by:
# Charges from group: Festival Charges (10 of 10)
# Charges from group: Interdiction Probe (2 of 2)
# Charges from group: Survey Probe (3 of 3)
type = "passive"


def handler(fit, module, context):
    module.multiplyItemAttr("speed", module.getModifiedChargeAttr("speedMultiplier") or 1)
