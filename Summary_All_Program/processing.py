import pandas as pd
import numpy as np

def SAP_Filter(form):
    objsap = form.cleaned_data['summary_all_program']
    objprv = form.cleaned_data['SAP_Filter']

    # Summary All Program document reading

    df = pd.read_excel(objsap.summary_all_program.path, sheet_name="LIST",header = 0, engine= 'openpyxl',)
    df = df.drop(['Unnamed: 0'], axis=1)
    df = df.dropna(how='all')
    df['SoW PAYG'] = df['SoW PAYG'].str.replace("MHz", "Mhz", case = False) 
    df['SoW PAYG'] = df['SoW PAYG'].str.replace(" Mhz", "Mhz", case = False)
    df['SoW PAYG'] = df['SoW PAYG'].str.replace(" Mh", "Mhz", case = False)
    df['SoW PAYG'] = df['SoW PAYG'].str.replace('17.7', '20', case = False)  
    df['SoW PAYG'] = df['SoW PAYG'].str.replace("17", "20", case = False)
    df['SoW PAYG'] = df['SoW PAYG'].str.replace("-20", "- 20", case = False)
    df['SoW PAYG'] = df['SoW PAYG'].str.replace("EQP New Site LTE", "EQP New Site 4G LTE", case = False)

    df = df[df['Active']==True]

    # UNIQUE LIST (CHECK FIRST BEFORE RUNNING CODE)
    curcptls = df['CP'].unique()
    curcpt = pd.DataFrame(curcptls, columns = ['CP'])
    curcpt = curcpt.dropna()
    curcpt = curcpt[curcpt.CP != 'Antenna Modernization 2019']
    curcpt = curcpt[curcpt.CP != 'FoC 2019']
    curcpt = curcpt[curcpt.CP != 'TBD']
    #filter each segmented type NO

    cptls0 = pd.read_excel(objprv.SAP_Filter.path, sheet_name = 'Filter', header = 0, engine= 'openpyxl',)
    cptls0 = cptls0.dropna(how='all')
    cptls = cptls0.values
    cptls = pd.DataFrame(cptls, columns= ['CP','List Type'])
    curcpt = curcpt.reset_index(drop=True)
    for x in range(len(curcpt)):
        y = curcpt.loc[x,'CP']
        if y not in cptls['CP'].values:
            cptls.loc[len(cptls),'CP'] = y

    sowls = df['SoW PAYG'].unique()
    dfsow = pd.DataFrame(sowls, columns =['SoW PAYG'])
    for x in range(len(dfsow)):
        if dfsow.loc[x,'SoW PAYG'][:15] == 'EQP New Site 4G':
            dfsow.loc[x,"SOW Type"] = 'New Site'
        elif dfsow.loc[x,'SoW PAYG'][:18] == 'EQP Upgrade BW LTE':
            dfsow.loc[x,"SOW Type"] = 'Upgrade'
    dfsow1 = dfsow[dfsow["SOW Type"]== 'New Site'].reset_index(drop = True)   
    dfsow2 = dfsow[dfsow["SOW Type"]== 'Upgrade'].reset_index(drop = True)
    dfsow3 = pd.concat([dfsow1,dfsow2], ignore_index=True)

    for x in range (len(dfsow3)):
        if dfsow3.loc[x, "SOW Type"] == 'New Site': # Newsite Formula parsing
            if dfsow3.loc[x,'SoW PAYG'][20] == '9':
                dfsow3.loc[x,'Band'] = int(dfsow3.loc[x,'SoW PAYG'][20:23])
                if dfsow3.loc[x,'SoW PAYG'][24:25] == '5':
                    dfsow3.loc[x,'Bandwidth'] = int(dfsow3.loc[x,'SoW PAYG'][24:25])
                else:
                    dfsow3.loc[x,'Bandwidth'] = int(dfsow3.loc[x,'SoW PAYG'][24:26])
            else:
                dfsow3.loc[x,'Band'] = int(dfsow3.loc[x,'SoW PAYG'][20:24])
                if dfsow3.loc[x,'SoW PAYG'][25:26] == '5':
                    dfsow3.loc[x,'Bandwidth'] = int(dfsow3.loc[x,'SoW PAYG'][25:26])
                else:
                    dfsow3.loc[x,'Bandwidth'] = int(dfsow3.loc[x,'SoW PAYG'][25:27])

        elif dfsow3.loc[x, "SOW Type"] =='Upgrade': # upgrade Formula Parsing
            if dfsow3.loc[x,'SoW PAYG'][19] == '9':
                dfsow3.loc[x,'Band'] = int(dfsow3.loc[x,'SoW PAYG'][19:22])
                dfsow3.loc[x,'Bandwidth Before'] = int(dfsow3.loc[x,'SoW PAYG'][23:25])
                if dfsow3.loc[x,'Bandwidth Before'] == 10:
                    dfsow3.loc[x,'Bandwidth After'] = 10
                else:
                    dfsow3.loc[x,'Bandwidth After'] = int(dfsow3.loc[x,'SoW PAYG'][27:29])
            else:
                dfsow3.loc[x,'Band'] = int(dfsow3.loc[x,'SoW PAYG'][19:23])
                dfsow3.loc[x,'Bandwidth Before'] = int(dfsow3.loc[x,'SoW PAYG'][24:26])
                dfsow3.loc[x,'Bandwidth After'] = int(dfsow3.loc[x,'SoW PAYG'][29:31])
        return [cptls0, cptls, dfsow3]