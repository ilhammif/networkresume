import pandas as pd
import numpy as np
from datetime import date
import os
from os import listdir
from django.conf import settings

def NOC_Func(lastweek,currentweek,siteprofile):
    objlw = lastweek
    objcw = currentweek
    objsp = siteprofile
    today = date.today()
    today = today.strftime("%b-%d-%Y")

    dfSP = pd.read_excel(objsp.site_id_profile.path, sheet_name = 'Site Profile', engine= 'openpyxl', header=0)
    dfSP.index = dfSP['SITE ID']
    dfSP = dfSP.drop(['SITE ID'], axis = 1)
    #2G Processing
    df2glw = pd.read_excel(objlw.Meas2G.path, sheet_name = 'BDBH',header= 0, engine= 'openpyxl',)
    df2gcw = pd.read_excel(objcw.Meas2G.path, sheet_name = 'BDBH',header= 0, engine= 'openpyxl',)
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
    df2g =pd.concat([df2gcw,df2glw])
    df2g = df2g.reset_index(drop = True)

    
    df2gr = df2g[(df2g["BTS NAME"].str[1] == "_") |(df2g["BTS NAME"].str[1] == "-")].copy()
    df2gr['SITE ID'] = df2gr["BTS NAME"].str[2:8]

    df2gi = df2g[(df2g["BTS NAME"].str[1] != "_") &(df2g["BTS NAME"].str[1] != "-")].copy()
    df2gi['SITE ID'] = df2gi["BTS NAME"].str[:6]
    print(1)
    df2g = pd.concat([df2gr,df2gi])
    dfg = df2g[df2g["Band"] == "GSM"].copy()
    dfd = df2g[df2g["Band"] == "DCS"].copy()

    #pivot 2G
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

    # 3G
    # 3G input 4 week Scheme
    df3glw = pd.read_excel(objlw.Meas3G.path, sheet_name = wklist[0],header= 0,)
    df3gcw = pd.read_excel(objcw.Meas3G.path, sheet_name = wklist[1],header= 0,)
    df3glw = df3glw.dropna(how='all')
    df3glw = df3glw[df3glw['Maximum available CE for NodeB Uplink'].notna()]
    df3gcw = df3gcw.dropna(how='all')
    df3gcw = df3gcw[df3gcw['Maximum available CE for NodeB Uplink'].notna()]

    df3glw['Week'] = str(objlw.Year) +"-" + wklist[0]
    df3gcw['Week'] = str(objcw.Year) +"-" + wklist[1]

    df3g =pd.concat([df3gcw,df3glw])
    # merge all file in Folder 3G
    
    df3g = df3g.reset_index(drop = True)
    df3g['Band'] = df3g['Status'].replace({"F1" : "U2100", "F2":"U2100", "F3":"U2100","U880":"U900"})
    dfu21 = df3g[df3g['Band'] == 'U2100'].copy()
    dfu9 = df3g[df3g['Band'] == 'U900'].copy()

    #Pivot 3G
    pivotu21 = pd.pivot_table(dfu21, index = ['Site ID'],values=['OSS Cell Name '],columns=['Week'], aggfunc= pd.Series.nunique)
    pivotu9 = pd.pivot_table(dfu9, index = ['Site ID'],values=['OSS Cell Name '],columns=['Week'], aggfunc= pd.Series.nunique)
    pivotu21 = pivotu21.replace(np.nan, 0 )
    u21 = pivotu21[(pivotu21[pivotu21.columns[1]] > 0 ) | (pivotu21[pivotu21.columns[0]] > 0 )].copy()
    pivotu9 = pivotu9.replace(np.nan, 0 )
    u9 = pivotu9[(pivotu9[pivotu9.columns[1]] > 0 ) | (pivotu9[pivotu9.columns[0]] > 0 )].copy()


    u21['U2100'] = 'U2100'
    u21BW = u21.drop([u21.columns[1],u21.columns[0]],axis = 1).copy()
    u21BW.columns = ['U2100']

    u9['U900'] = 'U900'
    u9BW = u9.drop([u9.columns[1],u9.columns[0]],axis = 1).copy()
    u9BW.columns = ['U900']


    #4G
    # 4G input 4 week Scheme
    
    #4g processing

    df4glw = pd.read_excel(objlw.Meas4G.path, sheet_name = 'RAW Data',header= 0, engine= 'openpyxl',)
    df4gcw = pd.read_excel(objcw.Meas4G.path, sheet_name = 'RAW Data',header= 0, engine= 'openpyxl',)
    df4glw = df4glw.dropna(how='all')
    df4gcw = df4gcw.dropna(how='all')
    df4glw['Week'] = str(objlw.Year) +"-" + wklist[0]
    df4gcw['Week'] = str(objcw.Year) +"-" + wklist[1]

    df4g =pd.concat([df4gcw,df4glw])
    df4g = df4g.reset_index(drop=True)
    df4gr = df4g[(df4g['Cell Name'].str[1] == "_") |(df4g['Cell Name'].str[1] == "-")].copy()
    df4gr['SITE ID'] = df4gr['Cell Name'].str[2:8]
    print(3)
    df4gi = df4g[(df4g['Cell Name'].str[1] != "_") &(df4g['Cell Name'].str[1] != "-")].copy()
    df4gi['SITE ID'] = df4gi['Cell Name'].str[:6]

    df4g = pd.concat([df4gr,df4gi])
    df4g['Bandwidth (MHz)'] = df4g['bandWidthDl'].replace({2:5,3:10,4:15,5:20}).copy() 
    dfL23F = df4g[df4g['earfcnDl'] > 2310].copy()
    dfL23E = df4g[(df4g['earfcnDl'] < 2311) & (df4g['earfcnDl'] > 2300)].copy()
    dfL21 = df4g[(df4g['earfcnDl'] < 2300) & (df4g['earfcnDl'] > 2100)].copy()
    dfL18 = df4g[(df4g['earfcnDl'] < 2100) & (df4g['earfcnDl'] > 1800)].copy()
    dfL9 = df4g[(df4g['earfcnDl'] < 1800) & (df4g['earfcnDl'] > 900)].copy()
    #Pivot 4g
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
    print(4)

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
    L23E = pivotl23E[(pivotl23E[pivotl23E.columns[1]] > 0 ) | (pivotl23E[pivotl23E.columns[0]] > 0 )].copy()
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
    
    # dfnolw = pd.read_excel(os.path.join(os.getcwd(),'Output',Nolw), sheet_name = 'DAPOT')
    # si_nolw = dfnolw['SITE ID'].unique()
    si_2g = df2g['SITE ID'].unique()
    si_3g = df3g['Site ID'].unique()
    si_4g = df4g['SITE ID'].unique()
    sicur = np.concatenate((si_2g,si_3g,si_4g)).T #si_nolw,
    sicur = pd.DataFrame(sicur, columns =['SITE ID'])
    siuniq = sicur['SITE ID'].unique()
    dfnocur = pd.DataFrame(index = siuniq,)
    dfnocur['2G'] = np.nan
    dfnocur['3G'] = np.nan
    dfnocur['4G'] = np.nan
    dfnocur['SUMMARY TECH'] = np.nan
    #merge all to 1 data frame
    dfnocur = pd.concat([dfnocur,gsmBW,dcsBW,u9BW,u21BW,bwl9,bwl18,bwl21,bwl23],axis = 1, sort = False)
    print(5)
    dfnocur.loc[dfnocur[(dfnocur['GSM'] == 'GSM') | (dfnocur['DCS'] == 'DCS')].index,'2G'] = '2G'
    dfnocur.loc[dfnocur[(dfnocur['U900'] == 'U900') | (dfnocur['U2100'] == 'U2100')].index,'3G'] = '3G'
    dfnocur.loc[dfnocur[(dfnocur['L900'] >= 5) | (dfnocur['L1800'] >= 5) | (dfnocur['L2100'] >= 5) | (dfnocur['L2300'] >= 5)].index,'4G'] = '4G'
    dfnocur.loc[dfnocur.index, ['2G','3G','4G']] = dfnocur.loc[dfnocur.index, ['2G','3G','4G']].fillna('-')
    dfnocur.loc[dfnocur.index, 'Support Symbol /'] = '/'
    dfnocur.loc[dfnocur.index, ['SUMMARY TECH']] = dfnocur['2G'] + dfnocur['Support Symbol /']+ dfnocur['3G'] + dfnocur['Support Symbol /'] + dfnocur['4G']
    dfnocur.loc[dfnocur[dfnocur['L900']>=5].index,'l9'] = 'L900'
    dfnocur.loc[dfnocur[dfnocur['L1800']>=5].index,'l18'] = 'L1800'
    dfnocur.loc[dfnocur[dfnocur['L2100']>=5].index,'l21'] = 'L2100'
    dfnocur.loc[dfnocur[dfnocur['L2300']>=5].index,'l23'] = 'L2300'
    dfnocur['SUMMARY BAND'] = np.nan
    dfnocur.loc[dfnocur.index, ['GSM','DCS','U900','U2100','l9','l18','l21','l23']] = dfnocur.loc[dfnocur.index, ['GSM','DCS','U900','U2100','l9','l18','l21','l23']].fillna('-')
    dfnocur.loc[dfnocur.index, ['SUMMARY BAND']] =dfnocur['GSM'] + dfnocur['Support Symbol /'] + dfnocur['DCS'] + dfnocur['Support Symbol /'] + dfnocur['U900'] + dfnocur['Support Symbol /'] + dfnocur['U2100'] + dfnocur['Support Symbol /'] + dfnocur['l9'] + dfnocur['Support Symbol /'] + dfnocur['l18'] + dfnocur['Support Symbol /'] + dfnocur['l21'] + dfnocur['Support Symbol /'] + dfnocur['l23']
    dfnocur = dfnocur.replace({'-':np.nan})
    dfnocur = dfnocur.drop(['l9','l18','l21','l23', 'Support Symbol /'],axis = 1)

    # #log
    # dflog = pd.DataFrame()

    # dfnolw.index = dfnolw['SITE ID']
    # dfnolw =dfnolw.drop(['SITE ID','SITE NAME', 'BRANCH', 'CLUSTER SALES', 'CITY', 'LONG', 'LAT','INNER / OUTER'], axis= 1)

    # # compare GSM
    # glw = dfnolw[dfnolw['GSM']=='GSM'].index
    # gcur = dfnocur[dfnocur['GSM']=='GSM'].index
    # cgsm = glw^gcur
    # # new GSM
    # dfgc = pd.DataFrame()
    # if not cgsm.empty:
    #     dfgc['SITE ID']= np.nan
    #     dfgc['SITE ID']= cgsm
    #     dfgc.index = dfgc['SITE ID'].copy()
    #     dfgc = dfgc.drop(['SITE ID'], axis = 1)
    #     dfgc.loc[dfgc.index.intersection(glw),'Remark Status'] = 'Shutdown or Missing from DB'
    #     dfgc.loc[dfgc.index.intersection(gcur),'Remark Status'] = 'Tidak ada di data minggu lalu (New)'
    #     dfgc.loc[dfgc.index,'Band'] = 'GSM'
    # # compare DCS
    # dlw = dfnolw[dfnolw['DCS']=='DCS'].index
    # dcur = dfnocur[dfnocur['DCS']=='DCS'].index
    # cdcs = dlw^dcur
    # # new DCS
    # dfdc = pd.DataFrame()
    # if not cdcs.empty:
    #     dfdc['SITE ID']= np.nan
    #     dfdc['SITE ID']= cdcs
    #     dfdc.index = dfdc['SITE ID'].copy()
    #     dfdc = dfdc.drop(['SITE ID'], axis = 1)
    #     dfdc.loc[dfdc.index.intersection(dlw),'Remark Status'] = 'Shutdown or Missing from DB'
    #     dfdc.loc[dfdc.index.intersection(dcur),'Remark Status'] = 'Tidak ada di data minggu lalu (New)'
    #     dfdc.loc[dfdc.index,'Band'] = 'DCS'


    # print(6)
    # # compare U900
    # u9lw = dfnolw[dfnolw['U900']=='U900'].index
    # u9cur = dfnocur[dfnocur['U900']=='U900'].index
    # cu9= u9lw^u9cur
    # # new U900
    # dfu9c = pd.DataFrame()
    # if not cu9.empty:
    #     dfu9c['SITE ID']= np.nan
    #     dfu9c['SITE ID']= cu9
    #     dfu9c.index = dfu9c['SITE ID'].copy()
    #     dfu9c = dfu9c.drop(['SITE ID'], axis = 1)
    #     dfu9c.loc[dfu9c.index.intersection(u9lw),'Remark Status'] = 'Shutdown or Missing from DB'
    #     dfu9c.loc[dfu9c.index.intersection(u9cur),'Remark Status'] = 'Tidak ada di data minggu lalu (New)'
    #     dfu9c.loc[dfu9c.index,'Band'] = 'U900'
    # # compare U2100
    # u21lw = dfnolw[dfnolw['U2100']=='U2100'].index
    # u21cur = dfnocur[dfnocur['U2100']=='U2100'].index
    # cu21= u21lw^u21cur
    # # new U2100
    # dfu21c = pd.DataFrame()
    # if not cu21.empty:
    #     dfu21c['SITE ID']= np.nan
    #     dfu21c['SITE ID']= cu21
    #     dfu21c.index = dfu21c['SITE ID'].copy()
    #     dfu21c = dfu21c.drop(['SITE ID'], axis = 1)
    #     dfu21c.loc[dfu21c.index.intersection(u21lw),'Remark Status'] = 'Shutdown or Missing from DB'
    #     dfu21c.loc[dfu21c.index.intersection(u21cur),'Remark Status'] = 'Tidak ada di data minggu lalu (New)'
    #     dfu21c.loc[dfu21c.index,'Band'] = 'U2100'
    # # compare LTE Preparation
    # dflcnolw = dfnolw.loc[dfnolw.index,['L900','L1800','L2100','L2300']].copy()
    # dflcnocur = dfnocur.loc[dfnocur.index,['L900','L1800','L2100','L2300']].copy()
    # dflcnolw.columns = ['L900lw','L1800lw','L2100lw','L2300lw']
    # dflcnocur.columns = ['L900cur','L1800cur','L2100cur','L2300cur']
    # dflcomp = pd.concat([dflcnolw,dflcnocur],axis = 1)
    # # compare L900
    # dfcl900 = dflcomp.loc[dflcomp.index,['L900lw','L900cur']].copy()
    # dfcl900.columns =['Bandwidth Past','Bandwidth Present']
    # dfcl900['Remark Status'] = np.nan
    # dfcl900['Band'] = np.nan
    # dfcl900 = dfcl900.fillna(0)
    # dfcl900 = dfcl900.loc[dfcl900[dfcl900['Bandwidth Past']!=dfcl900['Bandwidth Present']].index]
    # dfcl900.loc[dfcl900[dfcl900['Bandwidth Past']>dfcl900['Bandwidth Present']].index, 'Remark Status'] = 'Shutdown , Downgrade BW or Missing from DB'         
    # dfcl900.loc[dfcl900[dfcl900['Bandwidth Past']<dfcl900['Bandwidth Present']].index, 'Remark Status'] = 'New Or Upgrade BW'
    # dfcl900.loc[dfcl900.index,'Band'] = 'L900'
    # # compare L1800
    # dfcl1800 = dflcomp.loc[dflcomp.index,['L1800lw','L1800cur']].copy()
    # dfcl1800.columns =['Bandwidth Past','Bandwidth Present']
    # dfcl1800['Remark Status'] = np.nan
    # dfcl1800['Band'] = np.nan
    # dfcl1800 = dfcl1800.fillna(0)
    # dfcl1800 = dfcl1800.loc[dfcl1800[dfcl1800['Bandwidth Past']!=dfcl1800['Bandwidth Present']].index]
    # dfcl1800.loc[dfcl1800[dfcl1800['Bandwidth Past']>dfcl1800['Bandwidth Present']].index, 'Remark Status'] = 'Shutdown , Downgrade BW or Missing from DB'         
    # dfcl1800.loc[dfcl1800[dfcl1800['Bandwidth Past']<dfcl1800['Bandwidth Present']].index, 'Remark Status'] = 'New Or Upgrade BW'
    # dfcl1800.loc[dfcl1800.index,'Band'] = 'L1800'
    # # compare L2100
    # dfcl2100 = dflcomp.loc[dflcomp.index,['L2100lw','L2100cur']].copy()
    # print(7)
    # dfcl2100.columns =['Bandwidth Past','Bandwidth Present']
    # dfcl2100['Remark Status'] = np.nan
    # dfcl2100['Band'] = np.nan
    # dfcl2100 = dfcl2100.fillna(0)
    # dfcl2100 = dfcl2100.loc[dfcl2100[dfcl2100['Bandwidth Past']!=dfcl2100['Bandwidth Present']].index]
    # dfcl2100.loc[dfcl2100[dfcl2100['Bandwidth Past']>dfcl2100['Bandwidth Present']].index, 'Remark Status'] = 'Shutdown , Downgrade BW or Missing from DB'         
    # dfcl2100.loc[dfcl2100[dfcl2100['Bandwidth Past']<dfcl2100['Bandwidth Present']].index, 'Remark Status'] = 'New Or Upgrade BW'
    # dfcl2100.loc[dfcl2100.index,'Band'] = 'L2100'
    # # compare L2300
    # dfcl2300 = dflcomp.loc[dflcomp.index,['L2300lw','L2300cur']].copy()
    # dfcl2300.columns =['Bandwidth Past','Bandwidth Present']
    # dfcl2300['Remark Status'] = np.nan
    # dfcl2300['Band'] = np.nan
    # dfcl2300 = dfcl2300.fillna(0)
    # dfcl2300 = dfcl2300.loc[dfcl2300[dfcl2300['Bandwidth Past']!=dfcl2300['Bandwidth Present']].index]
    # dfcl2300.loc[dfcl2300[dfcl2300['Bandwidth Past']>dfcl2300['Bandwidth Present']].index, 'Remark Status'] = 'Shutdown , Downgrade BW or Missing from DB'         
    # dfcl2300.loc[dfcl2300[dfcl2300['Bandwidth Past']<dfcl2300['Bandwidth Present']].index, 'Remark Status'] = 'New Or Upgrade BW'
    # dfcl2300.loc[dfcl2300.index,'Band'] = 'L2300'

    # #log concate
    # dfcomp = pd.concat([dfgc,dfdc,dfu9c,dfu21c, dfcl900, dfcl1800, dfcl2100, dfcl2300],axis =0, sort = False)
    # dfcomp = dfcomp.reset_index()


    # silw = dfnolw[(dfnolw['GSM'].notna()) | (dfnolw['DCS'].notna()) | (dfnolw['U900'].notna()) | (dfnolw['U2100'].notna()) | (dfnolw['L900'].notna()) | (dfnolw['L1800'].notna()) | (dfnolw['L2100'].notna()) | (dfnolw['L2300'].notna())].index
    # sicur = dfnolw[(dfnolw['GSM'].notna()) | (dfnolw['DCS'].notna()) | (dfnolw['U900'].notna()) | (dfnolw['U2100'].notna()) | (dfnolw['L900'].notna()) | (dfnolw['L1800'].notna()) | (dfnolw['L2100'].notna()) | (dfnolw['L2300'].notna())].index
    # sicomp = silw^sicur
    # dfcsi = pd.DataFrame()
    # if not sicomp.empty:
    #     dfcsi['SITE ID']= np.nan
    #     dfcsi['SITE ID']= sicomp
    #     dfcsi.index = dfcsi['SITE ID'].copy()
    #     dfcsi = dfu9c.dfcsi(['SITE ID'], axis = 1)
    #     dfcsi['Remark']= np.nan
    #     dfcsi.loc[dfcsi.index.intersection(silw),'Remark'] = 'Shutdown/ Reloc/ DB Corrupt'
    #     dfcsi.loc[dfcsi.index.intersection(silw),'Week'] = wk
    #     dfcsi.loc[dfcsi.index.intersection(sicur),'Remark'] = 'New Site'
    #     dfcsi.loc[dfcsi.index.intersection(sicur),'Week'] = wk
    dfnocur = pd.concat([dfSP,dfnocur], axis = 1, sort = False)
    dfnocur['SITE ID'] = dfnocur.index
    dfnocur1 = dfnocur[['SITE ID','SITE NAME', 'BRANCH', 'CLUSTER SALES', 'CITY', 'LONG', 'LAT',
        'INNER / OUTER', '2G', '3G', '4G', 'SUMMARY TECH', 'GSM', 'DCS', 'U900',
        'U2100', 'L900', 'L1800', 'L2100', 'L2300', 'SUMMARY BAND']].copy()
    #save to spesific directory
    file_output = "Network Overview " + wklist[1] +" "+ today +".xlsx"
    
    directory = os.path.join(settings.MEDIA_ROOT, 'Output')
    if not os.path.exists(directory):
        os.makedirs(directory)
    writer = pd.ExcelWriter(os.path.join(directory, file_output), engine='xlsxwriter')
    sheetname1 ='DAPOT'
    dfnocur1.to_excel(writer, sheet_name = sheetname1, index=False)
    sheetname2 ='LOG ' + wklist[1] 
    # dfcomp.to_excel(writer, sheet_name = sheetname2, index=False)
    # sheetname3 ='Site LOG' + wklist[1] 
    # dfcsi.to_excel(writer, sheet_name = sheetname3, index=False)
    writer.save()
    fileo_path = os.path.join(directory, file_output)
    return([file_output,fileo_path])
