from DBFields import DBFields

# We access with d[] so throws error if typo
def key_val_dict(g):
    d = dict.fromkeys(DBFields)
    del d["game_ID"]
    d["date_time"] = g._date_time
    d["duration"] = g._duration
    d["stage"] = g._stage
    d["gametype"] = g._type

    d["p1_name"] = g._p1._name
    d["p1_num"] = g._p1._num
    d["p1_race"] = g._p1._race
    d["p1_lvl"] = g._p1._lvl
    d["p1_exp"] = g._p1._exp
    d["p1_win"] = g._p1._win
    d["p1_dexp"] = g._p1._dexp

    d["p1_scores_unit"] = g._p1._scores["Unit"]
    d["p1_scores_hero"] = g._p1._scores["Heroes"]
    d["p1_scores_resource"] = g._p1._scores["Resource"]
    d["p1_scores_total"] = g._p1._scores["Total"]

    d["p1_unit_unitsproduced"] = g._p1._unit_score["UnitsProduced"]
    d["p1_unit_unitskilled"] = g._p1._unit_score["UnitsKilled"]
    d["p1_unit_buildingsproduced"] = g._p1._unit_score["BuildingsProduced"]
    d["p1_unit_buildingsrazed"] = g._p1._unit_score["BuildingsRazed"]
    d["p1_unit_largestarmy"] = g._p1._unit_score["LargestArmy"]

    d["p1_hero_heroeskilled"] = g._p1._hero_score["HeroesKilled"]
    d["p1_hero_itemsobtained"] = g._p1._hero_score["ItemsObtained"]
    d["p1_hero_mercenarieshired"] = g._p1._hero_score["MercenariesHired"]
    d["p1_hero_experiencegained"] = g._p1._hero_score["ExperienceGained"]

    d["p1_resource_goldmined"] = g._p1._resource_score["GoldMined"]
    d["p1_resource_lumberharvested"] = g._p1._resource_score["LumberHarvested"]
    d["p1_resource_resourcesgiven"] = (g._p1._resource_score["ResourcesTraded"])[0]
    d["p1_resource_resourcesreceived"] = (g._p1._resource_score["ResourcesTraded"])[1]
    d["p1_resource_techpercentage"] = g._p1._resource_score["TechPercentage"]
    d["p1_resource_goldlosttoupkeep"] = g._p1._resource_score["GoldLosttoUpkeep"]

    d["p1_hero_h1_id"] = g._p1._h1_name
    d["p1_hero_h1_lvl"] = g._p1._h1_lvl
    d["p1_hero_h2_id"] = g._p1._h2_name
    d["p1_hero_h2_lvl"] = g._p1._h2_lvl
    d["p1_hero_h3_id"] = g._p1._h3_name
    d["p1_hero_h3_lvl"] = g._p1._h3_lvl

    d["p2_name"] = g._p2._name
    d["p2_num"] = g._p2._num
    d["p2_race"] = g._p2._race
    d["p2_lvl"] = g._p2._lvl
    d["p2_exp"] = g._p2._exp
    d["p2_win"] = g._p2._win
    d["p2_dexp"] = g._p2._dexp

    d["p2_scores_unit"] = g._p2._scores["Unit"]
    d["p2_scores_hero"] = g._p2._scores["Heroes"]
    d["p2_scores_resource"] = g._p2._scores["Resource"]
    d["p2_scores_total"] = g._p2._scores["Total"]

    d["p2_unit_unitsproduced"] = g._p2._unit_score["UnitsProduced"]
    d["p2_unit_unitskilled"] = g._p2._unit_score["UnitsKilled"]
    d["p2_unit_buildingsproduced"] = g._p2._unit_score["BuildingsProduced"]
    d["p2_unit_buildingsrazed"] = g._p2._unit_score["BuildingsRazed"]
    d["p2_unit_largestarmy"] = g._p2._unit_score["LargestArmy"]

    d["p2_hero_heroeskilled"] = g._p2._hero_score["HeroesKilled"]
    d["p2_hero_itemsobtained"] = g._p2._hero_score["ItemsObtained"]
    d["p2_hero_mercenarieshired"] = g._p2._hero_score["MercenariesHired"]
    d["p2_hero_experiencegained"] = g._p2._hero_score["ExperienceGained"]

    d["p2_resource_goldmined"] = g._p2._resource_score["GoldMined"]
    d["p2_resource_lumberharvested"] = g._p2._resource_score["LumberHarvested"]
    d["p2_resource_resourcesgiven"] = (g._p2._resource_score["ResourcesTraded"])[0]
    d["p2_resource_resourcesreceived"] = (g._p2._resource_score["ResourcesTraded"])[1]
    d["p2_resource_techpercentage"] = g._p2._resource_score["TechPercentage"]
    d["p2_resource_goldlosttoupkeep"] = g._p2._resource_score["GoldLosttoUpkeep"]

    d["p2_hero_h1_id"] = g._p2._h1_name
    d["p2_hero_h1_lvl"] = g._p2._h1_lvl
    d["p2_hero_h2_id"] = g._p2._h2_name
    d["p2_hero_h2_lvl"] = g._p2._h2_lvl
    d["p2_hero_h3_id"] = g._p2._h3_name
    d["p2_hero_h3_lvl"] = g._p2._h3_lvl
    return d


def InitDB(c):
    sql_command = "CREATE TABLE IF NOT EXISTS games\n(\n  "
    for i in DBFields:
        if i == "game_ID":
            sql_command += i + " INTEGER PRIMARY KEY,\n  "
        elif i == "date_time" or i == "p1_name" or i == "p2_name":
            sql_command += i + " TEXT NOT NULL,\n  "
        else:
            sql_command += i + " INTEGER NOT NULL,\n  "
    sql_command += (
        """unique(p1_name,p2_name,date_time),\n  CHECK(p1_name <> ''),\n  CHECK(p2_name <> '')\n)"""
    )
    # print(sql_command)
    c.execute(sql_command)
    return c


def InsertGame(g, connection, cursor):
    with connection:
        d = key_val_dict(g)
        # print("\n", d, "\n")
        columns = ", ".join(d.keys())
        placeholders = ":" + ", :".join(d.keys())
        sql_command = "INSERT INTO games (\n%s\n)\nVALUES\n(\n%s\n)" % (
            columns,
            placeholders,
        )
        # print(sql_command)
    cursor.execute(sql_command, d)
