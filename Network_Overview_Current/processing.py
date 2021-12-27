import pandas as pd
import numpy as np
def NOC_Func(lastweek,currentweek,siteprofile):
    objlw = lastweek
    objcw = currentweek
    objsp = siteprofile
    #2G Processing
    df2glw = pd.read_excel(objlw.meas2G.path, sheet_name = 'BDBH',header= 0, engine= 'openpyxl',)
    df2gcw = pd.read_excel(objcw.meas2G.path, sheet_name = 'BDBH',header= 0, engine= 'openpyxl',)
    df2glw = df2glw.dropna(how='all')
    df2gcw = df2gcw.dropna(how='all')
    objlist = [objlw.Week,objcw.Week]
    wklist =[]
    for i in objlist:
        if i < 10:
            wk = "W0" + str(i)
        else:
            wk = "W" + str(i)
        wklist.append(wk)

    df2glw['Week'] = str(objlw.Year) +"-" + wklist[0]
    df2gcw['Week'] = str(objcw.Year) +"-" + wklist[1]
    df2gr =pd.concat([df2gcw,df2glw])
    df2gr = df2gr[['BTS NAME','Band','Week']].copy()
    df2gr1 = df2gr[(df2gr["BTS NAME"].str[1] == "_") |(df2gr["BTS NAME"].str[1] == "-")].copy()
    df2gr1['SITE ID'] = df2gr1["BTS NAME"].str[2:8]

    df2gr2 = df2gr[(df2gr["BTS NAME"].str[1] != "_") &(df2gr["BTS NAME"].str[1] != "-")].copy()
    df2gr2['SITE ID'] = df2gr2["BTS NAME"].str[:6]
    df2g_prep = pd.concat([df2gr1,df2gr2])
    dfg = df2g_prep[df2g_prep['Band']=="GSM"].copy()
    dfd = df2g_prep[df2g_prep['Band']=="DCS"].copy()
    pivotg = pd.pivot_table(dfg, index = ['SITE ID'],values=['BTS NAME'],columns=['Week'], aggfunc= pd.Series.nunique)
    pivotd = pd.pivot_table(dfd, index = ['SITE ID'],values=['BTS NAME'],columns=['Week'], aggfunc= pd.Series.nunique)

    pivotg = pivotg.replace(np.nan, 0 )
    gsm = pivotg[(pivotg[pivotg.columns[1]] > 0 ) | (pivotg[pivotg.columns[0]] > 0 )].copy()

    pivotd = pivotd.replace(np.nan, 0 )
    dcs = pivotd[(pivotd[pivotd.columns[1]] > 0 ) | (pivotd[pivotd.columns[0]] > 0 )].copy()

    gsm.loc[gsm.index, 'GSM'] = 'GSM'
    gsmBW = gsm.drop([gsm.columns[0],gsm.columns[1]],axis = 1)
    gsmBW.columns = ['GSM']

    dcs.loc[:,'DCS'] = 'DCS'
    dcsBW = dcs.drop([dcs.columns[0],dcs.columns[1]],axis = 1)
    dcsBW.columns = ['DCS']

    #3G Processing
    df3glw = pd.read_excel(objlw.meas3G.path, sheet_name = wklist[0],header= 0,)
    df3gcw = pd.read_excel(objcw.meas3G.path, sheet_name = wklist[1],header= 0,)
    df3glw = df3glw.dropna(how='all')
    df3glw = df3glw[df3glw['Maximum available CE for NodeB Uplink'].notna()]
    df3gcw = df3gcw.dropna(how='all')
    df3gcw = df3gcw[df3gcw['Maximum available CE for NodeB Uplink'].notna()]

    df3glw['Week'] = str(objlw.Year) +"-" + wklist[0]
    df3gcw['Week'] = str(objcw.Year) +"-" + wklist[1]

    df3gr =pd.concat([df3gcw,df3glw])
    df3gr = df3gr[df3gr['Maximum available CE for NodeB Uplink'].notna()]
    df3gr = df3gr[['Site ID','OSS Cell Name ' , 'Status','Week']].copy()
    df3gr1 = df3gr[(df3gr['OSS Cell Name '].str[1] == "_") |(df3gr['OSS Cell Name '].str[1] == "-")].copy()
    df3gr1['SITE ID'] = df3gr1['OSS Cell Name '].str[2:8]

    df3gr2 = df3gr[(df3gr['OSS Cell Name '].str[1] != "_") &(df3gr['OSS Cell Name '].str[1] != "-")].copy()
    df3gr2['SITE ID'] = df3gr2['OSS Cell Name '].str[:6]


    df3g_prep = pd.concat([df3gr1,df3gr2])
    df3g_prep['Band'] = df3g_prep['Status'].replace({"F1" : "U2100", "F2":"U2100", "F3":"U2100","U880":"U900"})

    dfu9 = df3g_prep[df3g_prep['Band']=="U900"].copy()
    dfu21 = df3g_prep[df3g_prep['Band']=="U2100"].copy()
    pivotu9 = pd.pivot_table(dfu9, index = ['SITE ID'],values=['OSS Cell Name '],columns=['Week'], aggfunc= pd.Series.nunique)
    pivotu21 = pd.pivot_table(dfu21, index = ['SITE ID'],values=['OSS Cell Name '],columns=['Week'], aggfunc= pd.Series.nunique)

        
    pivotu9 = pivotu9.replace(np.nan, 0 )
    u9 = pivotu9[(pivotu9[pivotu9.columns[1]] > 0 ) | (pivotu9[pivotu9.columns[0]] > 0 )].copy()

    pivotu21 = pivotu21.replace(np.nan, 0 )
    u21 = pivotu21[(pivotu21[pivotu21.columns[1]] > 0 ) | (pivotu21[pivotu21.columns[0]] > 0 )].copy()

    u9.loc[u9.index, 'U900'] = 'U900'
    u9BW = u9.drop([u9.columns[0],u9.columns[1]],axis = 1)
    u9BW.columns = ['U900']

    u21.loc[u21.index, 'U2100'] = 'U2100'
    u21BW = u21.drop([u21.columns[0],u21.columns[1]],axis = 1)
    u21BW.columns = ['U2100']

    #4g processing

    df4glw = pd.read_excel(objlw.meas4G.path, sheet_name = 'RAW Data',header= 0, engine= 'openpyxl',)
    df4gcw = pd.read_excel(objcw.meas4G.path, sheet_name = 'RAW Data',header= 0, engine= 'openpyxl',)
    df4glw = df4glw.dropna(how='all')
    df4gcw = df4gcw.dropna(how='all')
    df4glw['Week'] = str(objlw.Year) +"-" + wklist[0]
    df4gcw['Week'] = str(objcw.Year) +"-" + wklist[1]

    df4gr =pd.concat([df4gcw,df4glw])
    df4gr1 = df4gr[(df4gr['Cell Name'].str[1] == "_") |(df4gr['Cell Name'].str[1] == "-")].copy()
    df4gr1['SITE ID'] = df4gr1['Cell Name'].str[2:8]

    df4gr2 = df4gr[(df4gr['Cell Name'].str[1] != "_") &(df4gr['Cell Name'].str[1] != "-")].copy()
    df4gr2['SITE ID'] = df4gr2['Cell Name'].str[:6]
    df4g_prep = pd.concat([df4gr1,df4gr2])
    df4g_prep['Bandwidth (MHz)'] = df4g_prep['bandWidthDl'].replace({2:5,3:10,4:15,5:20}).copy()
    dfL23F = df4g_prep[df4g_prep['earfcnDl'] > 2310].copy()
    dfL23E = df4g_prep[(df4g_prep['earfcnDl'] < 2311) & (df4g_prep['earfcnDl'] > 2300)].copy()
    dfL21 = df4g_prep[(df4g_prep['earfcnDl'] < 2300) & (df4g_prep['earfcnDl'] > 2100)].copy()
    dfL18 = df4g_prep[(df4g_prep['earfcnDl'] < 2100) & (df4g_prep['earfcnDl'] > 1800)].copy()
    dfL9 = df4g_prep[(df4g_prep['earfcnDl'] < 1800) & (df4g_prep['earfcnDl'] > 900)].copy()

    #L900
    dfL95 = dfL9[dfL9['Bandwidth (MHz)'] == 5 ].copy()
    pivotl95 = pd.pivot_table(dfL95, index = ['SITE ID'],values=['Cell Name'],columns=['Week'], aggfunc= pd.Series.nunique)
    L95 = pivotl95[(pivotl95[pivotl95.columns[1]] > 0 ) | (pivotl95[pivotl95.columns[0]] > 0 )].copy()
    L95 = L95.drop([L95.columns[0],L95.columns[1]],axis = 1)


    dfL910 = dfL9[dfL9['Bandwidth (MHz)'] == 10 ].copy()
    pivotl910 = pd.pivot_table(dfL910, index = ['SITE ID'],values=['Cell Name'],columns=['Week'], aggfunc= pd.Series.nunique)
    L910 = pivotl910[(pivotl910[pivotl910.columns[1]] > 0 ) | (pivotl910[pivotl910.columns[0]] > 0 )].copy()
    L910 = L910.drop([L910.columns[0],L910.columns[1]],axis = 1)

    bwl9 = pd.DataFrame(index= dfL9['SITE ID'].unique())
    bwl9.loc[bwl9.index.intersection(L95.index),'L900'] = 5
    bwl9.loc[bwl9.index.intersection(L910.index),'L900'] = 10

    #L1800
    dfL185 = dfL18[dfL18['Bandwidth (MHz)'] == 5 ].copy()
    pivotl185 = pd.pivot_table(dfL185, index = ['SITE ID'],values=['Cell Name'],columns=['Week'], aggfunc= pd.Series.nunique)
    L185 = pivotl185[(pivotl185[pivotl185.columns[1]] > 0 ) | (pivotl185[pivotl185.columns[0]] > 0 )].copy()
    L185 = L185.drop([L185.columns[0],L185.columns[1]],axis = 1)

    dfL1810 = dfL18[dfL18['Bandwidth (MHz)'] == 10 ].copy()
    pivotl1810 = pd.pivot_table(dfL1810, index = ['SITE ID'],values=['Cell Name'],columns=['Week'], aggfunc= pd.Series.nunique)
    L1810 = pivotl1810[(pivotl1810[pivotl1810.columns[1]] > 0 ) | (pivotl1810[pivotl1810.columns[0]] > 0 )].copy()
    L1810 = L1810.drop([L1810.columns[0],L1810.columns[1]],axis = 1)

    dfL1815 = dfL18[dfL18['Bandwidth (MHz)'] == 15 ].copy()
    pivotl1815 = pd.pivot_table(dfL1815, index = ['SITE ID'],values=['Cell Name'],columns=['Week'], aggfunc= pd.Series.nunique)
    L1815 = pivotl1815[(pivotl1815[pivotl1815.columns[1]] > 0 ) | (pivotl1815[pivotl1815.columns[0]] > 0 )].copy()
    L1815 = L1815.drop([L1815.columns[0],L1815.columns[1]],axis = 1)

    dfL1820 = dfL18[dfL18['Bandwidth (MHz)'] == 20 ].copy()
    pivotl1820 = pd.pivot_table(dfL1820, index = ['SITE ID'],values=['Cell Name'],columns=['Week'], aggfunc= pd.Series.nunique)
    L1820 = pivotl1820[(pivotl1820[pivotl1820.columns[1]] > 0 ) | (pivotl1820[pivotl1820.columns[0]] > 0 )].copy()
    L1820 = L1820.drop([L1820.columns[0],L1820.columns[1]],axis = 1)
    bwl18 = pd.DataFrame(index= dfL18['SITE ID'].unique())
    bwl18.loc[bwl18.index.intersection(L185.index),'L1800'] = 5
    bwl18.loc[bwl18.index.intersection(L1810.index),'L1800'] = 10
    bwl18.loc[bwl18.index.intersection(L1815.index),'L1800'] = 15
    bwl18.loc[bwl18.index.intersection(L1820.index),'L1800'] = 20


    #L2100
    dfL215 = dfL21[dfL21['Bandwidth (MHz)'] == 5 ].copy()
    pivotl215 = pd.pivot_table(dfL215, index = ['SITE ID'],values=['Cell Name'],columns=['Week'], aggfunc= pd.Series.nunique)
    L215 = pivotl215[(pivotl215[pivotl215.columns[1]] > 0 ) | (pivotl215[pivotl215.columns[0]] > 0 )].copy()
    L215 = L215.drop([L215.columns[0],L215.columns[1]],axis = 1)

    dfL2110 = dfL21[dfL21['Bandwidth (MHz)'] == 10 ].copy()
    pivotl2110 = pd.pivot_table(dfL2110, index = ['SITE ID'],values=['Cell Name'],columns=['Week'], aggfunc= pd.Series.nunique)
    L2110 = pivotl2110[(pivotl2110[pivotl2110.columns[1]] > 0 ) | (pivotl2110[pivotl2110.columns[0]] > 0 )].copy()
    L2110 = L2110.drop([L2110.columns[0],L2110.columns[1]],axis = 1)

    bwl21 = pd.DataFrame(index= dfL21['SITE ID'].unique())
    bwl21.loc[bwl21.index.intersection(L215.index),'L2100'] = 5
    bwl21.loc[bwl21.index.intersection(L2110.index),'L2100'] = 10
    #L2300
    pivotl23E = pd.pivot_table(dfL23E, index = ['SITE ID'],values=['Cell Name'],columns=['Week'], aggfunc= pd.Series.nunique)
    L23E = pivotl23E[(pivotl23E[pivotl23E.columns[0]] > 0 ) | (pivotl23E[pivotl23E.columns[1]] > 0 )].copy()
    L23E = L23E.drop([L23E.columns[0],L23E.columns[1]],axis = 1)
    L23E.loc[:,'E'] = True  

    pivotl23F = pd.pivot_table(dfL23F, index = ['SITE ID'],values=['Cell Name'],columns=['Week'], aggfunc= pd.Series.nunique)
    L23F = pivotl23F[(pivotl23F[pivotl23F.columns[1]] > 0 ) | (pivotl23F[pivotl23F.columns[0]] > 0 )].copy()
    L23F = L23F.drop([L23F.columns[0],L23F.columns[1]],axis = 1)
    L23F.loc[:,'F'] = True

    L23 = pd.concat([L23E, L23F],axis = 1 ,sort = False)
    L231 = L23.fillna(False)
    L231.loc[L231[(L231[L231.columns[0]] ==True) & (L231[L231.columns[1]] ==True)].index,'Band'] = 30
    L231.loc[L231[(L231[L231.columns[0]] ==True) & (L231[L231.columns[1]] ==False)].index,'Band'] = 20
    L231 = L231.drop([L231.columns[0],L231.columns[1]],axis = 1)
    L231.columns = ['L2300']
    bwl23 = L231.copy()

    #site ID preprocessing
    dfsite_id = pd.read_excel(objsp.site_id_profile.path, sheet_name = 'Site Profile', engine= 'openpyxl',)
    si_profile = dfsite_id['SITE ID'].unique()
    si_2g = df2g_prep['SITE ID'].unique()
    si_3g = df3g_prep['Site ID'].unique()
    si_4g = df4g_prep['SITE ID'].unique()
    sicur = np.concatenate((si_profile,si_2g,si_3g,si_4g)).T

    sicur = pd.DataFrame(sicur, columns =['SITE ID'])
    siuniq = sicur['SITE ID'].unique()
    dfnocur_prep = pd.DataFrame(index = siuniq,)
    dfsite_id = dfsite_id.set_index('SITE ID')
    site_prof = dfsite_id[['SITE NAME','BRANCH', 'CLUSTER SALES', 'CITY', 'LONG', 'LAT', 'INNER / OUTER']].copy()
    dfnocur_prep = pd.concat([dfnocur_prep,site_prof], axis = 1, sort = False)

    dfnocur_prep['2G'] = np.nan
    dfnocur_prep['3G'] = np.nan
    dfnocur_prep['4G'] = np.nan
    dfnocur_prep['SUMMARY TECH'] = np.nan
    dfnocur_prep = pd.concat([dfnocur_prep,gsmBW,dcsBW,u9BW,u21BW,bwl9,bwl18,bwl21,bwl23],axis = 1, sort = False)
    dfnocur_prep.loc[dfnocur_prep[(dfnocur_prep['GSM'] == 'GSM') | (dfnocur_prep['DCS'] == 'DCS')].index,'2G'] = '2G'
    dfnocur_prep.loc[dfnocur_prep[(dfnocur_prep['U900'] == 'U900') | (dfnocur_prep['U2100'] == 'U2100')].index,'3G'] = '3G'
    dfnocur_prep.loc[dfnocur_prep[(dfnocur_prep['L900'] >= 5) | (dfnocur_prep['L1800'] >= 5) | (dfnocur_prep['L2100'] >= 5) | (dfnocur_prep['L2300'] >= 5)].index,'4G'] = '4G'
    dfnocur_prep.loc[dfnocur_prep.index, ['2G','3G','4G']] = dfnocur_prep.loc[dfnocur_prep.index, ['2G','3G','4G']].fillna('-')
    dfnocur_prep.loc[dfnocur_prep.index, 'Support Symbol /'] = '/'
    dfnocur_prep.loc[dfnocur_prep.index, ['SUMMARY TECH']] = dfnocur_prep['2G'] + dfnocur_prep['Support Symbol /']+ dfnocur_prep['3G'] + dfnocur_prep['Support Symbol /'] + dfnocur_prep['4G']
    dfnocur_prep.loc[dfnocur_prep[dfnocur_prep['L900']>=5].index,'l9'] = 'L900'
    dfnocur_prep.loc[dfnocur_prep[dfnocur_prep['L1800']>=5].index,'l18'] = 'L1800'
    dfnocur_prep.loc[dfnocur_prep[dfnocur_prep['L2100']>=5].index,'l21'] = 'L2100'
    dfnocur_prep.loc[dfnocur_prep[dfnocur_prep['L2300']>=5].index,'l23'] = 'L2300'
    dfnocur_prep['SUMMARY BAND'] = np.nan
    dfnocur_prep.loc[dfnocur_prep.index, ['GSM','DCS','U900','U2100','l9','l18','l21','l23']] = dfnocur_prep.loc[dfnocur_prep.index, ['GSM','DCS','U900','U2100','l9','l18','l21','l23']].fillna('-')
    dfnocur_prep.loc[dfnocur_prep.index, ['SUMMARY BAND']] =dfnocur_prep['GSM'] + dfnocur_prep['Support Symbol /'] + dfnocur_prep['DCS'] + dfnocur_prep['Support Symbol /'] + dfnocur_prep['U900'] + dfnocur_prep['Support Symbol /'] + dfnocur_prep['U2100'] + dfnocur_prep['Support Symbol /'] + dfnocur_prep['l9'] + dfnocur_prep['Support Symbol /'] + dfnocur_prep['l18'] + dfnocur_prep['Support Symbol /'] + dfnocur_prep['l21'] + dfnocur_prep['Support Symbol /'] + dfnocur_prep['l23']
    dfnocur_prep = dfnocur_prep.replace({'-':np.nan})
    dfnocur = dfnocur_prep.drop(['l9','l18','l21','l23', 'Support Symbol /'],axis = 1)
    dfnocur = dfnocur.reset_index()
    dfnocur = dfnocur.rename(columns={'index':'SITE ID'},inplace=False)
    
    return dfnocur