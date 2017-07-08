def try_chs_name(item):
    if getattr(item, "chs_name", None):
        return "%s(%s)" % (item.name, item.chs_name)
    else:
        return item.name


def try_chs_skillname(item, lvl):
    if getattr(item, "chs_name", None):
        return "%s %s (%s %s)" % (item.name, lvl, item.chs_name, lvl)
    else:
        return "%s %s" % (item.name, lvl)