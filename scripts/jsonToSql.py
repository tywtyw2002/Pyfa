#!/usr/bin/env python
#======================================================================
# Copyright (C) 2012 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with eos.  If not, see <http://www.gnu.org/licenses/>.
#======================================================================

import os
import sys
import re

# Add eos root path to sys.path so we can import ourselves
path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))
sys.path.append(os.path.realpath(os.path.join(path, "..")))

import json
import argparse

def main(db, json_path):

    jsonPath = os.path.expanduser(json_path)

    # Import eos.config first and change it
    import eos.config
    eos.config.gamedata_connectionstring = db
    eos.config.debug = False

    # Now thats done, we can import the eos modules using the config
    import eos.db
    import eos.gamedata

    # Create the database tables
    eos.db.gamedata_meta.create_all()

    # Config dict
    tables = {
        "clonegrades": eos.gamedata.AlphaCloneSkill,
        "dgmattribs": eos.gamedata.AttributeInfo,
        "dgmeffects": eos.gamedata.Effect,
        "dgmtypeattribs": eos.gamedata.Attribute,
        "dgmtypeeffects": eos.gamedata.ItemEffect,
        "dgmunits": eos.gamedata.Unit,
        "icons": eos.gamedata.Icon,
        "evecategories": eos.gamedata.Category,
        "evegroups": eos.gamedata.Group,
        "invmetagroups": eos.gamedata.MetaGroup,
        "invmetatypes": eos.gamedata.MetaType,
        "evetypes": eos.gamedata.Item,
        "phbtraits": eos.gamedata.Traits,
        "phbmetadata": eos.gamedata.MetaData,
        "mapbulk_marketGroups": eos.gamedata.MarketGroup,
    }

    fieldMapping = {
        "dgmattribs": {
            "displayName_en-us": "displayName"
        },
        "dgmeffects": {
            "displayName_en-us": "displayName",
            "description_en-us": "description"
        },
        "dgmunits": {
            "displayName_en-us": "displayName"
        },
        #icons???
        "evecategories": {
            "categoryName_en-us": "categoryName"
        },
        "evegroups": {
            "groupName_en-us": "groupName"
        },
        "invmetagroups": {
            "metaGroupName_en-us": "metaGroupName"
        },
        "evetypes": {
            "typeName_en-us": "typeName",
            "description_en-us": "description"
        },
        #phbtraits???
        "mapbulk_marketGroups": {
            "marketGroupName_en-us": "marketGroupName",
            "description_en-us": "description"
        }

    }

    rowsInValues = (
        "evetypes",
        "evegroups",
        "evecategories"
    )

    def convertIcons(data):
        new = []
        for k, v in data.items():
            v["iconID"] = k
            new.append(v)
        return new

    def convertClones(data):
        newData = []

        for ID in data:
            for skill in data[ID]["skills"]:
                newData.append({
                    "alphaCloneID": int(ID),
                    "alphaCloneName": data[ID]["internalDescription"],
                    "typeID": skill["typeID"],
                    "level": skill["level"]})

        return newData

    def convertTraits(data):

        def convertSection(sectionData):
            sectionLines = []
            headerText = u"<b>{}</b>".format(sectionData["header"])
            sectionLines.append(headerText)
            for bonusData in sectionData["bonuses"]:
                prefix = u"{} ".format(bonusData["number"]) if "number" in bonusData else ""
                bonusText = u"{}{}".format(prefix, bonusData["text"].replace(u"\u00B7", u"\u2022 "))
                sectionLines.append(bonusText)
            sectionLine = u"<br />\n".join(sectionLines)
            return sectionLine

        newData = []
        for row in data:
            typeLines = []
            typeId = row["typeID"]
            traitData = row["traits"]
            for skillData in sorted(traitData.get("skills", ()), key=lambda i: i["header"]):
                typeLines.append(convertSection(skillData))
            if "role" in traitData:
                typeLines.append(convertSection(traitData["role"]))
            if "misc" in traitData:
                typeLines.append(convertSection(traitData["misc"]))
            traitLine = u"<br />\n<br />\n".join(typeLines)
            newRow = {"typeID": typeId, "traitText": traitLine}
            newData.append(newRow)
        return newData

    def convertTypes(typesData):
        """
        Add factionID column to evetypes table.
        """
        factionMap = {}
        with open(os.path.join(jsonPath, "fsdTypeOverrides.json")) as f:
            overridesData = json.load(f)
        for typeID, typeData in overridesData.items():
            factionID = typeData.get("factionID")
            if factionID is not None:
                factionMap[int(typeID)] = factionID
        for row in typesData:
            row['factionID'] = factionMap.get(int(row['typeID']))
        return typesData

    data = {}

    # Dump all data to memory so we can easely cross check ignored rows
    for jsonName, cls in tables.iteritems():
        with open(os.path.join(jsonPath, "{}.json".format(jsonName))) as f:
            tableData = json.load(f)
        if jsonName in rowsInValues:
            tableData = list(tableData.values())
        if jsonName == "icons":
            tableData = convertIcons(tableData)
        if jsonName == "phbtraits":
            tableData = convertTraits(tableData)
        if jsonName == "evetypes":
            tableData = convertTypes(tableData)
        if jsonName == "clonegrades":
            tableData = convertClones(tableData)
        data[jsonName] = tableData

    # Set with typeIDs which we will have in our database
    # Sometimes CCP unpublishes some items we want to have published, we
    # can do it here - just add them to initial set
    eveTypes = set()
    for row in data["evetypes"]:
        if (row["published"]
            or row['groupID'] == 1306  # group Ship Modifiers, for items like tactical t3 ship modes
            or row['typeID'] in (3638, 3634, 3636, 3640)  # Civilian weapons
            or row['typeID'] in (41549, 41548, 41551,41550)  # Micro Bombs (Fighters)
        ):
            eveTypes.add(row["typeID"])

    # ignore checker
    def isIgnored(file, row):
        if file in ("evetypes", "dgmtypeeffects", "dgmtypeattribs", "invmetatypes") and row['typeID'] not in eveTypes:
            return True
        return False

    # Loop through each json file and write it away, checking ignored rows
    for jsonName, table in data.iteritems():
        fieldMap = fieldMapping.get(jsonName, {})
        tmp = []

        print "processing {}".format(jsonName)

        for row in table:
            # We don't care about some kind of rows, filter it out if so
            if not isIgnored(jsonName, row):
                instance = tables[jsonName]()
                # fix for issue 80
                if jsonName is "icons" and "res:/ui/texture/icons/" in str(row["iconFile"]).lower():
                    row["iconFile"] = row["iconFile"].lower().replace("res:/ui/texture/icons/", "").replace(".png", "")
                    # with res:/ui... references, it points to the actual icon file (including it's size variation of #_size_#)
                    # strip this info out and get the identifying info
                    split = row['iconFile'].split('_')
                    if len(split) == 3:
                        row['iconFile'] = "{}_{}".format(split[0], split[2])
                if jsonName is "icons" and "modules/" in str(row["iconFile"]).lower():
                    row["iconFile"] = row["iconFile"].lower().replace("modules/", "").replace(".png", "")

                if jsonName is "clonegrades":
                    if (row["alphaCloneID"] not in tmp):
                        cloneParent = eos.gamedata.AlphaClone()
                        setattr(cloneParent, "alphaCloneID", row["alphaCloneID"])
                        setattr(cloneParent, "alphaCloneName", row["alphaCloneName"])
                        eos.db.gamedata_session.add(cloneParent)
                        tmp.append(row['alphaCloneID'])

                for k, v in row.iteritems():
                    if (isinstance(v, basestring)):
                        v = v.strip()
                    setattr(instance, fieldMap.get(k, k), v)

                eos.db.gamedata_session.add(instance)

    eos.db.gamedata_session.commit()

    # CCP still has 5 subsystems assigned to T3Cs, even though only 4 are available / usable. They probably have some
    # old legacy requirement or assumption that makes it difficult for them to change this value in the data. But for
    # pyfa, we can do it here as a post-processing step
    eos.db.gamedata_engine.execute("UPDATE dgmtypeattribs SET value = 4.0 WHERE attributeID = ?", (1367,))

    print("done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This scripts dumps effects from an sqlite cache dump to mongo")
    parser.add_argument("-d", "--db", required=True, type=str, help="The sqlalchemy connectionstring, example: sqlite:///c:/tq.db")
    parser.add_argument("-j", "--json", required=True, type=str, help="The path to the json dump")
    args = parser.parse_args()

    main(args.db, args.json)
