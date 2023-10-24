import streamlit as st
from math import floor
import altair as alt
import json
from roCalc import *

##Streamlit##

st.set_page_config(page_title='ReMorroc Calc', page_icon=':crossed_swords:')

def calculate():
    if st.session_state.calculate:
        st.session_state.calculate=False
    else:
        st.session_state.calculate = True

def graph():
    if st.session_state.graph:
        st.session_state.graph=False
    else:
        st.session_state.graph = True


def load():
    if st.session_state.load:
        st.session_state.load = False
    else:
        st.session_state.load = True

def numInputWrapper(stInuputFunction):
    def wrapper(label, *args, **kwargs):
        inputWidget = stInuputFunction(label,*args,**kwargs)
        jsonValues[kwargs['key']] = inputWidget
        return inputWidget
    
    return wrapper
numInput = numInputWrapper(st.number_input)


if 'calculate' not in st.session_state:
    st.session_state.calculate = False
if 'graph' not in st.session_state:
    st.session_state.graph = False
if 'load' not in st.session_state:
    st.session_state.load = False

jsonValues = {}

st.title('Atk Calculator')

levelCol1,_,_ = st.columns(3)
with levelCol1:
    level = st.empty()
superCol1, superCol2, superCol3 = st.columns(3)
with superCol1:
    astr = st.empty()
    aagi = st.empty()
    avit = st.empty()
    weapon = st.empty()
    mastery = st.empty()
with superCol2:
    aint = st.empty()
    adex = st.empty()
    aluk = st.empty()
    flatBonusAtk = st.empty()
with superCol3:
    uploadWidget = st.empty()
    download = st.empty()

st.markdown('Bonus')
percCol1, percCol2, percCol3 = st.columns(3)
with percCol1:
    race = st.empty()
    atkPerc = st.empty()
    elementMulti = st.empty()
with percCol2:
    mproperty = st.empty()
    skillBonus = st.empty()
with percCol3:
    size = st.empty()
    elementBonus = st.empty()


st.markdown('Combat')
def1, def2 = st.columns(2)
with def1:
    enemyDef = st.empty()
with def2:
    defPierce = st.empty()

skill1, skill2 = st.columns(2)
with skill1:
    skillPerc = st.empty()
    skillHits = st.empty()
with skill2:
    skillScale = st.expander('Skill scaling',False)

but1, but2 = st.columns(2)
with but1:
    calcButton = st.empty()
    outputDmgHeader = st.empty()
    outputDmg = st.empty()
with but2:
    graphButton = st.empty()
    selectProp = st.empty()
    valueSlider = st.empty()


calcButton.button('Calculate', on_click=calculate, use_container_width=True)
graphButton.button('Graphic', on_click=graph, use_container_width=True)
with selectProp:
    propList = list(atk_prettyNamesDict.keys())
    selectProp = st.multiselect('Attributes to vary',propList,
                                format_func=lambda x : atk_prettyNamesDict[x])
with valueSlider:
    valueSlider = st.slider('Value variance',0,40,5)

#Must be checked before the definition of the inputs
upload = uploadWidget.file_uploader('Load',on_change=load,
                                    label_visibility='hidden')   

if st.session_state.load and upload is not None:
    jsonValues = json.loads(upload.getvalue())
    defaultDict = jsonValues
    #st.write(jsonValues) 

with level:
    level = numInput('Level',step=1,key='level',
            value=defaultDict['level'])
with astr:
    astr = numInput('Str',step=1,key='astr',
            value=defaultDict['astr'])
with aagi:
    aagi = numInput('Agi',step=1,key='aagi',
            value=defaultDict['aagi'])   
with avit:
    avit = numInput('Vit',step=1,key='avit',
            value=defaultDict['avit'])   
with aint:
    aint = numInput('Int',step=1,key='aint',
            value=defaultDict['aint'])    
with adex:
    adex = numInput('Dex',step=1,key='adex',
            value=defaultDict['adex'])
with aluk:
    aluk = numInput('Luk',step=1,key='aluk',
            value=defaultDict['aluk'])
with weapon:
    weapon = numInput('Weapon Atk',step=1,key='weapon',
            value=defaultDict['weapon'])
with mastery:
    mastery = numInput('Weapon Mastery',step=1,key='mastery',
                       value=defaultDict['mastery'])
with flatBonusAtk:
    flatBonusAtk = numInput('Flat Atk bonus',step=1,key='flatBonusAtk',
            value=defaultDict['flatBonusAtk'])
with race:
    race = numInput('Race %',step=1,key='race',
            value=defaultDict['race'])
with atkPerc:
    atkPerc = numInput('Atk %',step=1,key='atkPerc',
            value=defaultDict['atkPerc'])
with mproperty:
    mproperty = numInput('Monster element %',step=1,key='mproperty',
            value=defaultDict['mproperty'])
with skillBonus:
    skillBonus = numInput('Skill %',step=1,key='skillBonus',
            value=defaultDict['skillBonus'])
with size:
    size = numInput('Size %',step=1,key='size',
            value=defaultDict['size'])
with elementBonus:
    elementBonus = numInput('Damage with element %',step=1,key='elementBonus',
            value=defaultDict['elementBonus'])
with elementMulti:
    elementMulti = numInput('Elemental modifier %',step=1,key='elementMulti',
            value=defaultDict['elementMulti'])
with enemyDef:
    enemyDef = numInput('Enemy Def',step=1,key='enemyDef',
            value=defaultDict['enemyDef'])
with defPierce:
    defPierce = numInput('Def Pierce %',step=1,key='defPierce',
            value=defaultDict['defPierce'])
with skillPerc:
    skillPerc = numInput('Skill damage %',step=1,key='skillPerc',
            value=defaultDict['skillPerc'])
with skillHits:
    skillHits = numInput('Number of hits',step=1,key='skillHits',
            value=defaultDict['skillHits'])
with skillScale:
    attList = ['Str','Agi','Vit','Int','Dex','Luk']
    attScale = st.selectbox('Attribute',attList)
    attMultiplier = st.number_input('Multiplier')
    attName = 'a'+ attScale.lower()
    skillScaleValue = (jsonValues[attName])*(attMultiplier)
    st.write('{0:.2f} %'.format(skillScaleValue))
    

if st.session_state.calculate:
    atk = Atk(level,astr,aagi,avit,aint,adex,aluk,weapon,flatBonusAtk,mastery,
              race,mproperty,
              size,atkPerc,skillBonus,elementBonus,elementMulti,skillPerc,
              skillHits,skillScaleValue,enemyDef,defPierce)
    finalDamage = atk.final()

    outputDmgHeader.text('Final damage:')
    outputDmg.text('%d'%finalDamage)

if st.session_state.graph:
    atk = Atk(level,astr,aagi,avit,aint,adex,aluk,weapon,mastery,
               flatBonusAtk,race,mproperty,size,
            atkPerc,skillBonus,elementBonus,elementMulti,
            skillPerc,skillHits,
            skillScaleValue,enemyDef,defPierce)
    df = atk.graphDf(valueSlider,selectProp)

    tab1, tab2 = st.tabs(['Graph','Data'])
    tab1.line_chart(df)
    #chart = alt.Chart(df).mark_line().encode(x=df.columns[0])
    #for column in df.columns[1:]:
    #    chart.encode(y=column)
    #chart.encoding.y.scale = alt.Scale(domain=[min(df),max(df)])
    #tab1.altair_chart(chart)
    tab2.write(df)



#must be defined after everything
download.download_button('Save:floppy_disk:',json.dumps(jsonValues),
                         'char.json',use_container_width=True)
