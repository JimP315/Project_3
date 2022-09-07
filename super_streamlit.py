import pandas as pd
import streamlit as st
from datetime import datetime




#######################
# Reading Excel File
df = pd.read_excel('b.xlsx')
#######################


###################
#heading
st.write('## XYZ Practice Concessional Contribution - Client Database')
###################


#######################
## Merging Last and First Names for dropdown box
years=st.slider('Year',2018,2022, step=1)
df['fullname']=df['Surname']+' '+df['First Name']
options=st.multiselect('Name',(df['fullname']).sort_values())
###########################


#########################
### This is for when I fix Excel Datetime
### Calculates age based on DOB
### This is needed so eligibility changes based on date chosen

#dateforage=datetime.date(years,6, 30)
#df['formatted_DOB'] = [datetime.strptime(d, "%m/%d/%Y").strftime("%d/%m/%Y") for d in df['DOB']]
#df['calc_age']=dateforage-df['formatted_DOB']
##########################


###########################
#Testing eligibility of picked client names
st.write('Eligibility')
eliglist=[]
for names in options:
    age=df.loc[df['fullname']==names]['Age']
    supera=df.loc[df['fullname']==names][f'TSB-{years-2000}']
    if age.values < 75 and supera.values < 500000:
        st.write(names+'-'+'Eligible')
        eliglist.append(names)
    elif age.values > 75:
        st.write(names+'-'+'Ineligible'+' Over 75')
    elif supera.values > 500000:
        st.write(names+'-'+'Ineligible'+' Super Balance')
##########################


#######################
#Slicing DataFrame for only selected Clients
clientdf=pd.DataFrame()
for names in options:
    clientdf=clientdf.append(df[df['fullname']==names])
######################

################################################
#Slicing Dataframe for years wanted

# Returns list of last 2 digits of years selected in the slider. ie 18,19,20
ylist=[]
while years > 2017:
    ylist.append(str(years-2000))
    years=years-1
    
#Selects Columns based on last 2 digits, ie TSB-'19'
col=['Surname', 'First Name']
for i in df.columns:
    for year in ylist:
        if i.find(year) > -1:
            col.append(i)
#############################################


#####################################################
## Dropping True/False xlsx colums
## Dropping Avail Columns that arent current year
try:
    clientdf_final=clientdf[col]
    for i in clientdf_final:
        if i.find('Able') > -1:
            clientdf_final=clientdf_final.drop(columns=i)
        elif i.find(f'Avail{ylist[0]}') > -1:
            continue
        elif i.find('Avail') > -1:
            clientdf_final=clientdf_final.drop(columns=i)
except:
    st.write('Please Select a Client')
########################################################


#################################################
#Try statement because an error will show if no client is selected
try:
    st.write(clientdf_final)
except:
    st.write('Client Data will show here')
###############################################

st.write('### Top 10 Highest Available Contribution amounts')
try:
    top10=df.nlargest(n=10, columns=[f'Avail{ylist[0]}'])
    st.write(top10[['Surname','First Name', f'Avail{ylist[0]}']])
except:
    st.write('Select a year greater than 2018 to see highest available contribution amounts')