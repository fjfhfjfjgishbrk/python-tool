
def reactioncalc(em):
    return 1808.57 * (2.25 + (5 * em) / (em + 1200))


mainval = [46.6, 46.6, 58.3, 186.5, 31.1, 62.2, 58.3, 4780, 311, 46.6, 35.9]
mainname = ["Hp", "Atk", "Def", "Em", "Cr", "Cd", "Er", "Flower", "Feather", "Dmg", "Heal"]
maindict = {mainname[i]: mainval[i] for i in range(len(mainname))}

subval = [253.94, 16.535, 19.675, 4.955, 4.955, 6.195, 19.815, 3.305, 6.605, 5.505]
subname = ["Fhp", "Fatk", "Fdef", "Hp", "Atk", "Def", "Em", "Cr", "Cd", "Er"]
subdict = {subname[i]: subval[i] for i in range(len(subname))}

basestat = [10164, 313, 607, 0, 0, 0, 50, 28.8, 0]
basename = ["Hp", "Atk", "Def", "Em", "Er", "Cr", "Cd", "Ele", "Heal"]
basedict = {basename[i]: basestat[i] for i in range(len(basename))}

#---------------------------------Insert data here tank u-------------------------------------------

naOptiGoal = [("Atk", 1552.9), ("Em", 1680)]
skillOptiGoal = [("Atk", 3004.1), ("Em", 7386.6)]
burstOptiGoal = [("Atk", 826), ("Em", 661.6)]

naOptiBuff = {"Dmg": 0, "Cr": 0, "Cd": 0}
skillOptiBuff = {"Dmg": 0, "Cr": 0, "Cd": 0}
burstOptiBuff = {"Dmg": 0, "Cr": 0, "Cd": 0}

naReactionTime = 6
skillReactionTime = 9
burstReactionTime = 2

#-----------------------------------Weapon data here------------------------------------------------

weaponstat = [542, 0, 0, 0, 0, 0, 0, 88.2]
weaponname = ["Atk", "Hp", "Atkp", "Def", "Em", "Er", "Cr", "Cd"]
weapon = {weaponname[i]: weaponstat[i] for i in range(len(weaponname))}
weaponbuff = [("Cr", 4), ("Dmg", 0), ("Fatk", 0), ("Atk", 0)]

#---------------------------------Artifact data here------------------------------------------------

artibuff = [("Dmg", 0), ("Atk", 14), ("Em", 180)]

mainstat = ["Em", "Em", "Cr"]

subbal = ["Atk", "Cr", "Cd", "Em"]
subcount = 28

#--------------------------------------------Other stufff--------------------------------------------

resis = 10
plevel = 90
elevel = 90

defShred = 0
defmulti = (100 + plevel) / ((1 - defShred / 100) * (elevel + 100) + plevel + 100)

otherbuff = [("Em", 100), ("Cr", 0), ("Cd", 0), ("Dmg", 0)]

optidict = {}
for i in range(20):
    optidict[i] = [0, 0, 0, 0]
eachsub = [0] * len(subbal)
eachsub[-1] = subcount


statdict = {"Atk": weapon["Atkp"], "Def": 0, "Hp": 0, "BAtk": weapon["Atk"] + basedict["Atk"], "BDef": basedict["Def"],
            "BHp": basedict["Hp"], "Em": basedict["Em"] + weapon["Em"], "Er": basedict["Er"] + weapon["Er"],
            "Cr": basedict["Cr"] + weapon["Cr"], "Cd": basedict["Cd"] + weapon["Cd"], "Dmg": basedict["Ele"], "Fatk": 311, "FHp": 4780}

for buff in weaponbuff:
    statdict[buff[0]] += buff[1]

for buff in artibuff:
    statdict[buff[0]] += buff[1]

for buff in otherbuff:
    statdict[buff[0]] += buff[1]

for name in mainstat:
    statdict[name] += maindict[name]



while True:
    if eachsub[-1] < 0:
        break
    sumsubc = sum(eachsub)
    if sumsubc > subcount:
        for i, e in enumerate(eachsub):
            if e == 0:
                continue
            else:
                if i == len(eachsub) - 2:
                    eachsub[-1] -= 1
                    eachsub[0] = subcount - eachsub[-1]
                    for j in range(1, len(eachsub)):
                        if j != len(eachsub) - 1:
                            eachsub[j] = 0
                    break
                else:
                    eachsub[i+1] += 1
                    eachsub[i] = max(0, subcount - sum([eachsub[j] for j in range(1, len(eachsub))]))
                    break
    elif sumsubc < subcount:
        eachsub[0] += 1
        continue
    else:
        tempdict = statdict.copy()
        for i, name in enumerate(subbal):
            tempdict[name] += subdict[name] * eachsub[i]

        tempdict["Atk"] = tempdict["BAtk"] * (100 + tempdict["Atk"]) / 100 + tempdict["Fatk"]
        tempdict["Def"] = tempdict["BDef"] * (100 + tempdict["Def"]) / 100
        tempdict["Hp"] = tempdict["BHp"] * (100 + tempdict["Hp"]) / 100 + tempdict["FHp"]

        damageOut = 0

        naDamageOut = 0
        skillDamageOut = 0
        burstDamageOut = 0

        reactionOut = 0

        skillOptiBuff["Dmg"] = min(100, (tempdict["Em"] - 0) * 0.1)
        burstOptiBuff["Dmg"] = min(100, (tempdict["Em"] - 0) * 0.1)

        for i in naOptiGoal:
            naDamageOut += tempdict[i[0]] * i[1] / 100
        naDamageOut += reactioncalc(tempdict["Em"]) * naReactionTime
        naDamageOut *= (1 + (tempdict["Dmg"] + naOptiBuff["Dmg"]) / 100) * (
                1 + min(100, tempdict["Cr"] + naOptiBuff["Cr"]) * (tempdict["Cd"] + naOptiBuff["Cd"]) / 10000) * (1 - resis / 100) * defmulti

        for i in skillOptiGoal:
            skillDamageOut += tempdict[i[0]] * i[1] / 100
        skillDamageOut += reactioncalc(tempdict["Em"]) * skillReactionTime
        skillDamageOut *= (1 + (tempdict["Dmg"] + skillOptiBuff["Dmg"]) / 100) * (
                    1 + min(100, tempdict["Cr"] + skillOptiBuff["Cr"]) * (tempdict["Cd"] + skillOptiBuff["Cd"]) / 10000) * (1 - resis / 100) * defmulti

        for i in burstOptiGoal:
            burstDamageOut += tempdict[i[0]] * i[1] / 100
        burstDamageOut += reactioncalc(tempdict["Em"]) * burstReactionTime
        burstDamageOut *= (1 + (tempdict["Dmg"] + burstOptiBuff["Dmg"]) / 100) * (
                    1 + min(100, tempdict["Cr"] + burstOptiBuff["Cr"]) * (tempdict["Cd"] + burstOptiBuff["Cd"]) / 10000) * (1 - resis / 100) * defmulti

        damageOut = naDamageOut + skillDamageOut + burstDamageOut

        for k, v in optidict.items():
            if k < damageOut:
                del optidict[k]
                optidict[damageOut] = [eachsub.copy(), [naDamageOut, skillDamageOut, burstDamageOut]]
                break
        eachsub[0] += 1

sortedres = dict(sorted(optidict.items()))
for k, v in sortedres.items():
    print("Damage: {}".format(round(k)))
    print("Subs: ", end="")
    for i in range(len(subbal)):
        print("{0}: {1}".format(subbal[i], v[0][i]), end="")
        if i != len(subbal) - 1:
            print(" / ", end="")
        else:
            print("")
            print("NA damage: {0} \nSkill damage: {1} \nBurst damage: {2}".format(round(v[1][0]), round(v[1][1]), round(v[1][2])))
            print("---------------------------------------------")

