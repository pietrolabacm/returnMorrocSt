from math import floor
import numpy as np
import pandas as pd

prettyNamesDict = {'int':'Int',
                   'dex':'Dex',
                   'luk':'Luk',
                   'weapon':'Weapon Matk',
                   'flatBonus':'Flat Matk bonus',
                   'race':'Race %',
                   'matkPerc':'Matk %',
                   'mproperty':'Monster element %',
                   'skillBonus':'Skill %',
                   'size':'Size %',
                   'elementBonus':'Damage with element %',
                   'mdefPierce':'Mdef Pierce %'}


class Matk():
    def __init__(self, level, int, dex, luk, weapon, flatBonus, race,
                 mproperty, size, matkPerc, skillBonus, elementBonus,
                 elementMulti,
                 skillPerc, skillHits, skillScale, enemyMdef, 
                 mdefPierce):
        self.level = level
        self.int = int
        self.dex = dex
        self.luk = luk
        self.weapon = weapon
        self.flatBonus = flatBonus

        self.race = race
        self.mproperty = mproperty
        self.size = size
        self.matkPerc = matkPerc
        self.skillBonus = skillBonus
        self.elementBonus = elementBonus
        self.elementMulti = elementMulti

        self.skillPerc = skillPerc
        self.skillHits = skillHits
        self.skillScale = skillScale
        self.enemyMdef = enemyMdef
        self.mdefPierce = mdefPierce

        self.prettyNamesDict = {'int':'Int',
                                'dex':'Dex',
                                'luk':'Luk',
                                'weapon':'Weapon Matk',
                                'flatBonus':'Flat Matk bonus',
                                'race':'Race %',
                                'matkPerc':'Matk %',
                                'mproperty':'Monster element %',
                                'skillBonus':'Skill %',
                                'size':'Size %',
                                'elementBonus':'Damage with element %',
                                'mdefPierce':'Mdef Pierce %'}

    def statusMatk(self):
        statusMatk = floor(floor(self.level/4)+
                           self.int+
                           floor(self.int/2)+floor(self.dex/5)+
                           floor(self.luk/3))
        bonusInt = floor(self.int/10)
        bonusDex = floor(self.dex/10)
        statusMatk = statusMatk+bonusInt+bonusDex
        return statusMatk
    
    def weaponMatk(self):
        return self.weapon
    
    def totalMatk(self):
        matk = (
            (self.statusMatk() + self.weaponMatk() + self.flatBonus)*
            (1+(self.race/100))*
            (1+(self.mproperty/100))*
            (1+(self.size/100))*
            (1+(self.matkPerc/100))*
            (1+(self.skillBonus/100))*
            (1+(self.elementBonus/100))*
            (self.elementMulti/100)
        )
        return matk
    
    def final(self):
        dmg = (self.totalMatk()*((self.skillPerc/100)+(self.skillScale/100)))
        finalMdef = self.enemyMdef*(1-(self.mdefPierce/100))
        finalDamage = dmg*((1000+finalMdef)/(1000+finalMdef*10))
        finalDamage = finalDamage*self.skillHits
        return floor(finalDamage)
    
    def vary(self,value,attribute):
        return self.__dict__[attribute]+value

    def graphDf(self,value,optionsList):
        linesDict = {}
        indexDict = {}
        array = np.linspace(0, value, value+1,dtype=int)
        indexDict['x'] = array

        for attribute in optionsList:
            lineList = []
            originalAttribute = self.__dict__[attribute]
            varyArray = self.vary(array,attribute)
            for i in varyArray:
                self.__dict__[attribute] = i
                lineList.append(self.final())
            self.__dict__[attribute] = originalAttribute
            linesDict[self.prettyNamesDict[attribute]] = np.array(lineList)        

        df = pd.DataFrame(linesDict, index=indexDict['x'])
        return(df)
        