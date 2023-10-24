from math import floor
import numpy as np
import pandas as pd

matk_prettyNamesDict = {'str':'Str',
                        'agi':'Agi',
                        'vit':'Vit',
                        'int':'Int',
                        'dex':'Dex',
                        'luk':'Luk',
                        'weapon':'Weapon Matk',
                        'flatBonusMatk':'Flat Matk bonus',
                        'race':'Race %',
                        'matkPerc':'Matk %',
                        'mproperty':'Monster element %',
                        'skillBonus':'Skill %',
                        'size':'Size %',
                        'elementBonus':'Damage with element %',
                        'mdefPierce':'Mdef Pierce %'
                        }

atk_prettyNamesDict = {'str':'Str',
                        'agi':'Agi',
                        'vit':'Vit',
                        'int':'Int',
                        'dex':'Dex',
                        'luk':'Luk',
                        'weapon':'Weapon Atk',
                        'mastery':'Weapon Mastery',
                        'flatBonusAtk':'Flat Atk bonus',
                        'race':'Race %',
                        'atkPerc':'Atk %',
                        'mproperty':'Monster element %',
                        'skillBonus':'Skill %',
                        'size':'Size %',
                        'elementBonus':'Damage with element %',
                        'mdefPierce':'Def Pierce %'
                        }

defaultDict = {
    'level':1,
    'astr':1,
    'aagi':1,
    'avit':1,
    'aint':1,
    'adex':1,
    'aluk':1,
    'weapon':0,
    'mastery':0,
    'flatBonusMatk':0,
    'flatBonusAtk':0,
    'race':0,
    'mproperty':0,
    'size':0,
    'atkPerc':0,
    'matkPerc':0,
    'elementBonus':0,
    'elementMulti':100,
    'skillBonus':0,
    'skillPerc':100,
    'skillHits':1,
    'skillScale':0,
    'enemyMdef':0,
    'enemyDef':0,
    'mdefPierce':0,
    'defPierce':0
    }


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

        self.prettyNamesDict = matk_prettyNamesDict

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
    

class Atk():
    def __init__(self,level,astr,agi,vit,aint,dex,luk,weapon,flatBonusAtk,
                 mastery,race,
                 mproperty,size,atkPerc,skillbonus,elementBonus, elementMulti,
                 skillPerc,skillHits,skillScale,enemyDef,defPierce):
        self.level = level
        self.str = astr
        self.agi = agi
        self.vit = vit
        self.int = aint
        self.dex = dex
        self.luk = luk
        self.weapon = weapon
        self.flatBonusAtk = flatBonusAtk
        self.mastery = mastery

        self.race = race
        self.mproperty = mproperty
        self.size = size
        self.atkPerc = atkPerc
        self.skillBonus = skillbonus
        self.elementBonus = elementBonus
        self.elementMulti = elementMulti

        self.skillPerc = skillPerc
        self.skillHits = skillHits
        self.skillScale = skillScale
        self.enemyDef = enemyDef
        self.defPierce = defPierce

        self.prettyNamesDict = atk_prettyNamesDict

        
    def statusAtk(self):
        statusAtk = floor(floor(floor(self.level/4)+
                          self.str)+
                          floor(self.dex/5)+
                          floor(self.luk/3))
        bonusStr = floor(self.str/10)
        bonusDex = floor(self.dex/10)
        statusAtk = statusAtk+bonusStr+bonusDex
        return statusAtk
    
    def weaponAtk(self):
        statBonus = (self.weapon*self.str)/200
        weaponAtk = self.weapon + statBonus
        return weaponAtk
    
    def totalAtk(self):
        atk=(
            (self.statusAtk()*(1+self.elementMulti/100)*2)+
            ((self.weaponAtk()+self.flatBonusAtk)*self.atkPerc)+
            (
                (self.weaponAtk()+self.flatBonusAtk)*
                (1+(self.race/100))*
                (1+(self.mproperty/100))*
                (1+(self.size/100))*
                (1+(self.skillBonus/100))*
                (1+(self.elementBonus/100))
            )
            +self.mastery
        )
        return atk
    
    def final(self):
        dmg = (self.totalAtk()*((self.skillPerc/100)+self.skillScale/100))
        finalDef = self.enemyDef*(1-(self.defPierce/100))
        finalDamage = dmg*((4000+finalDef)/(4000+finalDef*10))
        finalDamage = finalDamage * self.skillHits
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