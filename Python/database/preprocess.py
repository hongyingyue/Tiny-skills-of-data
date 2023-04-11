# Todo :pyenchant to check the spell
# Todo: plot the complaint month and sensor's data to make sure
# Todo: reduce the unnecessary NA, nan



import numpy as np
import re
from english_blank import *
import logging

output_columns=['Sensor','VIN','Failure location','Failure type','Fault code','Production month','Complaint month','Carline',
                'Province','City','Month age','Mileage','Cost','Description','PG','Engine type','Complaint reason',
                'Hyperlink','Road condition','Weather','Speed']
output_carline=['W176','W246','X156','V/W205','X253','V/W213','W/X166','V/X222','C/A453']
location=pd.read_csv('Province_city_en_ch.csv',sep=';',encoding='utf-8')
dealer_master=pd.read_excel('Dealer master.xlsx')
warranty_rule_file='Rules update_w&g_20181105'
other_rule_file='Rules update_other sensors_20181105'

def clean_warranty(Repair_list):
    warranty=pd.read_excel(Repair_list)
    warranty=warranty.loc[warranty['Total costs']>0,:]
    warranty['Sensor']='W&G'
    warranty['Carline']=warranty.loc[:,'FIN'].astype(str).str.slice(0,3)
    warranty['Initial registration date']=pd.to_datetime(warranty['Initial registration date'],format='%m/%d/%Y')
    warranty['Repair date']=pd.to_datetime(warranty['Repair date'],format='%m/%d/%Y')
    warranty['Production date'] = pd.to_datetime(warranty['Production date'], format='%m/%d/%Y')
    warranty['Date of credit'] = pd.to_datetime(warranty['Date of credit (sum)'], format='%m/%d/%Y')
    warranty['day_age_']=warranty['Repair date']-warranty['Initial registration date']
    warranty['day_age']=warranty['day_age_'].apply(lambda x: x.days)
    warranty['Month age']=warranty['day_age']//30.5+1
    warranty['Production month'] = list(map(lambda x: x.strftime("%Y%m"), warranty['Production date']))
    warranty['Complaint month'] = list(map(lambda x: x.strftime("%Y%m"), warranty['Date of credit']))

    warranty_rules=pd.read_excel(warranty_rule_file+'.xlsx')
    warranty_rules['Issue_name']=warranty_rules['Issue'].apply(lambda x: x.split(' - ')[0])
    warranty_rules['Type_name']=warranty_rules['Issue'].apply(lambda x: x.split(' - ')[-1])
    warranty=pd.merge(warranty,warranty_rules.loc[:,['Fault location','Issue_name']].drop_duplicates(subset='Fault location'),on='Fault location',how='left')
    warranty=pd.merge(warranty, warranty_rules.loc[:,['Fault location','Fault type','Type_name']].drop_duplicates(subset=['Fault location','Fault type']),on=['Fault location','Fault type'],how='left')
    warranty['Issue_name']=warranty['Issue_name'].fillna(warranty['Unnamed: 11'])
    warranty['Type_name'] = warranty['Type_name'].fillna(warranty['Unnamed: 13'])
    warranty=warranty.merge(location.loc[:,['Province','City']],how='left',on='City')
    warranty['Fault code']=warranty['Fault location']+warranty['Fault type']+' '+warranty['Main damage part']+' '+warranty['Unnamed: 15']
    warranty=warranty.loc[warranty['Issue_name']!='Map data update, navigation system',:]
    warranty = warranty.loc[warranty['Type_name'] != 'Follow-up operations', :]

    warranty.rename(columns={'Vehicle mileage in km':'Mileage','Total costs':'Cost','Workshop message text (complaint)':'Description',
                             'Issue_name':'Failure location','Type_name':'Failure type'},inplace=True)
    for column in output_columns:
        if column not in warranty.columns:
            warranty[column]='NA'
    return warranty.loc[:,output_columns]

def clean_cac(cac_list):
    try:
        cac=pd.read_excel(cac_list,sheetname='Result')
    except:
        cac = pd.read_excel(cac_list)


    try:
        cac['Startdate']=pd.to_datetime(cac['Startdate'],format='%Y-%m-%d %H:%M:%S')
    except:
        if '-' in str(cac.ix[1, 'StartDate']):
            cac['StartDate'] = pd.to_datetime(cac['StartDate'], format='%Y-%m-%d')
        else:
            cac['StartDate'] = pd.to_datetime(cac['StartDate'].astype(int), unit='D', origin=pd.Timestamp('1899-12-30'))

    if cac.loc[~cac['Production_Month'].isnull(),'Production_Month'].values.tolist()[1]>200000:
        try:
            cac.loc[~cac['Production_Month'].isnull(), 'Production_Month'] = cac.loc[~cac[
                'Production_Month'].isnull(), 'Production_Month'].astype(int).astype(str) + '01'
            cac['Production_Month'] = pd.to_datetime((cac['Production_Month']), format='%Y%m%d')
        except:

            cac['Production_Month'] = pd.to_datetime((cac['Production_Month']), format='%m%d%Y')
    else:
        cac.loc[~cac['Production_Month'].isnull(), 'Production_Month'] = pd.to_datetime(
            cac.loc[~cac['Production_Month'].isnull(), 'Production_Month'].astype(int), unit='D',origin=pd.Timestamp('1899-12-30'))

    cac['day_age_']=cac['StartDate']-cac['Production_Month']
    cac['day_age']=cac['day_age_'].apply(lambda x:x.days)
    cac['Month age']=cac['day_age']//30.5+1

    cac['Production_Month']= cac['Production_Month'].dt.strftime('%Y%m').replace('NaT', '')
    #cac.loc[~cac['Production_month'].isnull(), 'Production month'] = list(map(lambda x: x.strftime("%Y%m"),cac.loc[~cac['Production_month'].isnull(),'Production_month']))

    cac=cac.merge(dealer_master.loc[:,['Dealer Name (Chinese)','Province']],how='left',left_on='主经销商名称',right_on='Dealer Name (Chinese)')
    cac.rename(columns={ 'DataSource': 'Sensor','ReportMonth':'Complaint month',
                        'QFS_Tier1':'Failure location','QFS_Tier3':'Failure type','Production_Month':'Production month'}, inplace=True)

    for column in output_columns:
        if column not in cac.columns:
            cac[column]='NA'
    return cac.loc[:,output_columns]

def clean_online(online_list):
    online=pd.read_excel(online_list)
    online['Sensor']='Online'
    try:
        online['Age']=online['Age'].apply(lambda x: str(x).replace('Year',''))
        online['Month age'] = np.ceil(online['Age'].astype(float) * 12)
    except:
        logging.info('Lack of Age columns in: {}'.format(online_list))
    online.rename(columns={'QFS_Tier1':'Failure location','QFS_Tier3':'Failure type','Hyperlink (URL)':'Hyperlink',
                           '链接': 'Hyperlink'},inplace=True)
    online['Post Date']=pd.to_datetime(online['Post Date'],format='%Y-%m-%d %H:%M:%S')
    online=online.loc[~online['Post Date'].isnull(),:]
    online['Complaint month'] = list(map(lambda x: x.strftime('%Y%m'), online['Post Date']))
    online['Description'] = online['Title'].astype(str) + online['Description'].astype(str)

    for column in output_columns:
        if column not in online.columns:
            online[column]='NA'
    return online.loc[:,output_columns]

def clean_tips(tips_list):
    tips=pd.read_excel(tips_list)
    tips['Sensor']='TIPS'

    if '-'in str(tips.ix[1, 'case creation date']):
        tips['Case creation date'] = pd.to_datetime(tips['case creation date'], format='%Y-%m-%d %H:%M:%S')
        tips['Initial registration date'] = pd.to_datetime(tips['Initial registration date'],format='%Y-%m-%d %H:%M:%S')
    else:
        tips['Case creation date'] = pd.to_datetime(tips['case creation date'].astype(int), unit='D', origin=pd.Timestamp('1899-12-30'))
        tips.loc[~tips['Initial registration date'].isnull(),'Initial registration date'] = pd.to_datetime(
            tips.loc[~tips['Initial registration date'].isnull(),'Initial registration date'].astype(int), unit='D', origin=pd.Timestamp('1899-12-30'))


    tips['day_age_']=tips['Case creation date']-tips['Initial registration date']
    tips['day_age']=tips['day_age_'].apply(lambda x: x.days)
    tips['Month age']=tips['day_age']//30.5+1
    tips['Complaint month']=list(map(lambda x: x.strftime("%Y%m"), tips['Case creation date']))
    try:
        if '-' in str(tips.ix[1,'Production date']):
            tips['Production date'] = pd.to_datetime(tips['Production date'], format='%Y-%m-%d')
        else:
            tips['Production date'] = pd.to_datetime(tips['Production date'].astype(int), unit='D', origin=pd.Timestamp('1899-12-30'))
        tips['Production month'] = list(map(lambda x: x.strftime('%Y%m'), tips['Production date']))
    except:
        logging.info('Lack of Production date {}'.format(tips_list))
    tips['Description']=tips['Title of the case in the preparing workshop']+tips['Customer complaint (TIPS)']+tips['Workshop findings (TIPS)']+tips['Measures carried out (TIPS)']
    if 'Carline' not in tips.columns:
        tips['Carline']=tips['Vehicle model series']

    tips.rename(columns={'Vin':'VIN','Tier1': 'Failure location', 'Tier3': 'Failure type',
                         'Vehicle mileage in km (TIPS)': 'Mileage','City (W&G)':'City',
                         'QFS_Tier1':'Failure location','QFS_Tier3':'Failure type',
                         'Tier_1':'Failure location','Tier_3':'Failure type'}, inplace=True)
    tips = tips.merge(location.loc[:, ['Province', 'City']], how='left', on='City')
    for column in output_columns:
        if column not in tips.columns:
            tips[column]='NA'
    return tips.loc[:,output_columns]

def clean_aqsiq(aqsiq_list):
    aqsiq=pd.read_excel(aqsiq_list)
    aqsiq['Sensor']='AQSIQ'
    if '注册日期' in aqsiq.columns:
        aqsiq['Initial registration date']=pd.to_datetime(aqsiq['注册日期'],format='%Y-%m-%d %H:%M:%S')
    elif '购买日期' in aqsiq.columns:
        aqsiq['Initial registration date'] = pd.to_datetime(aqsiq['购买日期'], format='%Y-%m-%d %H:%M:%S')
    else:
        print('No 注册日期 or  购买日期 in {}'.format(aqsiq_list))
    aqsiq['Complaint date']=pd.to_datetime(aqsiq['缺陷报告时间'],format='%Y-%m-%d %H:%M:%S')
    aqsiq['Complaint month']=list(map(lambda x: x.strftime('%Y%m'),aqsiq['Complaint date']))
    aqsiq['Mileage']=aqsiq['行驶里程']//1000+1

    aqsiq.rename(columns={'车辆识别代号（VIN）':'VIN','QFS_Tier1':'Failure location','QFS_Tier3':'Failure type',
                          '所在地市':'City','所在省份':'Province_Chinese','缺陷描述':'Description',
                          '所在省市':'Province_Chinese'},inplace=True)
    aqsiq['Province_Chinese'] = aqsiq.loc[:,'Province_Chinese'].apply(lambda x: str(x).replace('省', ''))
    aqsiq['Province_Chinese'] = aqsiq.loc[:,'Province_Chinese'].apply(lambda x: str(x).replace('市', ''))
    aqsiq = aqsiq.merge(location.loc[:, ['Province', 'Province_Chinese']], how='left', on='Province_Chinese')
    for column in output_columns:
        if column not in aqsiq.columns:
            aqsiq[column]='NA'
    return aqsiq.loc[:,output_columns]

def clean_crm(crm_list):
    crm=pd.read_excel(crm_list)
    crm['Sensor']='CRM'
    if '/' in str(crm.ix[1, 'Opened Date']) or '-' in str(crm.ix[1, 'Opened Date']):
        try:
            crm['Complaint date']=pd.to_datetime(crm['Opened Date'],format='%m/%d/%Y')
        except:
            crm['Complaint date'] = pd.to_datetime(crm['Opened Date'], format='%Y-%m-%d %H:%M:%S')
    else:
        crm['Complaint date'] = pd.to_datetime(crm['Opened Date'].astype(int), unit='D',origin=pd.Timestamp('1899-12-30'))
    crm['Complaint month']=list(map(lambda x: x.strftime('%Y%m'),crm['Complaint date']))
    #crm['Mileage']=crm['Mileage'].astype(int)//1000+1

    crm.rename(columns={'Tier_1':'Failure location','Tier_3':'Failure type','QFS_Tier1':'Failure location',
                        'QFS_Tier3':'Failure type','Tier1':'Failure location','Tier3':'Failure type'},inplace=True)
    for column in output_columns:
        if column not in crm.columns:
            crm[column]='NA'
    return crm.loc[:,output_columns]

def clean_all(QFS_data):
    assert not QFS_data.empty
    QFS_data['PG'] = QFS_data['PG'].apply(lambda x: str(x).replace("PG", "").replace(" ", ""))
    #issue template
    QFS_data['Failure location'] = [i.strip() if isinstance(i, str) else i for i in QFS_data['Failure location']]
    QFS_data['Failure type'] = [i.strip() if isinstance(i, str) else i for i in QFS_data['Failure type']]
    blank = re.compile(r" +")
    QFS_data['Failure location'] = [blank.sub(' ', i) if isinstance(i, str) else i for i in
                                    QFS_data['Failure location']]
    #issue name
    QFS_data.loc[(QFS_data.loc[:,'Failure location']=='Tire')& (QFS_data['Failure type'].isin(['Bulge','Burst','Brust'])) ,'Failure type']='Bulge/burst'
    QFS_data.loc[(QFS_data.loc[:,'Failure type']=='Noise')& (QFS_data['Failure location'].isin(['Brake lining, rear','Brake lining, front','Brake pad'])),'Failure location']='Brake'
    QFS_data['Failure location']=QFS_data['Failure location'].apply(lambda x: str(x).replace('Carbody','Car body'))

    QFS_data['Failure location'] = QFS_data['Failure location'].apply(lambda x: str(x).capitalize())
    QFS_data['Failure type'] = QFS_data['Failure type'].apply(lambda x: str(x).capitalize())
    QFS_data['Complaints'] = QFS_data['Failure location'].astype(str) + '-' + QFS_data['Failure type'].astype(str)
    QFS_data['Complaints'] = QFS_data['Complaints'].apply(lambda x: x.replace(' ', '').replace('dynamic','Dynamic').replace('static','Static'))

    other_rules = pd.read_excel(other_rule_file + '.xlsx')
    pattern = re.compile(r"\ASEC|SUV|CC|SMART")
    other_rules['Descriptioninothersensors'] = other_rules['Descriptioninothersensors'].apply(lambda x: re.sub(pattern, '', x))

    other_rules['Failure location1'] = other_rules['Issue'].apply(lambda x: x.split('-')[0])
    other_rules['Failure location1'] = other_rules['Failure location1'].apply(lambda x: re.sub(pattern, '', x))
    other_rules['Failure location1'] = other_rules['Failure location1'].apply(
        lambda x: infer_spaces(x).replace(' / ', '/').replace(' - ', '-').replace(' ( ','(').replace(' ) ',')'))
    other_rules['Failure type1'] = other_rules['Issue'].apply(lambda x: x.split('-')[-1])
    other_rules['Failure type1'] = other_rules['Failure type1'].apply(
        lambda x: infer_spaces(x).replace(' / ', '/').replace(' - ', '-').replace(' (','(').replace('( ','(').replace(' )',')').replace(') ',')'))

    QFS_data = QFS_data.merge(other_rules.loc[:, ['Descriptioninothersensors', 'Failure location1', 'Failure type1']],
                              left_on='Complaints', right_on='Descriptioninothersensors', how='left')

    QFS_data.loc[~QFS_data['Failure location1'].isnull(), 'Failure location'] = QFS_data.loc[
        ~QFS_data['Failure location1'].isnull(), 'Failure location1']
    QFS_data.loc[~QFS_data['Failure type1'].isnull(), 'Failure type'] = QFS_data.loc[
        ~QFS_data['Failure type1'].isnull(), 'Failure type1']
    QFS_data.drop(['Complaints','Descriptioninothersensors','Failure location1','Failure type1'],axis=1,inplace=True)
    QFS_data.drop_duplicates(inplace=True)


    #carline
    QFS_data.loc[QFS_data.Carline.str.contains('156', na=False), 'Carline'] = 'X156'
    QFS_data.loc[QFS_data.Carline.str.contains('205', na=False), 'Carline'] = 'V/W205'
    QFS_data.loc[QFS_data.Carline.str.contains('213', na=False), 'Carline'] = 'V/W213'
    QFS_data.loc[QFS_data.Carline.str.contains('253', na=False), 'Carline'] = 'X253'
    QFS_data.loc[QFS_data.Carline.str.contains('222', na=False), 'Carline'] = 'V/X222'
    QFS_data.loc[QFS_data.Carline.str.contains('176', na=False), 'Carline'] = 'W176'
    QFS_data.loc[QFS_data.Carline.str.contains('246', na=False), 'Carline'] = 'W246'
    QFS_data.loc[QFS_data.Carline.str.contains('166', na=False), 'Carline'] = 'W/X166'
    QFS_data.loc[QFS_data.Carline.str.contains('218', na=False), 'Carline'] = 'C/X218'
    QFS_data.loc[QFS_data.Carline.str.contains('453', na=False), 'Carline'] = 'C/A453'
    QFS_data.loc[QFS_data.Carline.str.contains('177', na=False), 'Carline'] = 'Z177'
    QFS_data = QFS_data.loc[QFS_data.Carline.isin(output_carline), :]
    #production month
    #Province
    QFS_data['Province'] = QFS_data['Province'].apply(lambda x: str(x).replace(' ', ''))
    QFS_data['Province']=QFS_data['Province'].astype('str')
    QFS_data.loc[QFS_data['Province']=='InnerMongolia','Province']='Neimenggu'
    QFS_data.loc[QFS_data['Province'] == 'Tibet', 'Province'] = 'Xizang'
    QFS_data.loc[QFS_data['Province'] == 'xicang', 'Province'] = 'Xizang'
    QFS_data.loc[QFS_data['Province'] == 'zhongqing', 'Province'] = 'Chongqing'
    QFS_data.loc[QFS_data['Province'] == 'shaanxi', 'Province'] = 'Shannxi'
    QFS_data.loc[QFS_data['Province'] == 'Shaanxi', 'Province'] = 'Shannxi'
    #online
    QFS_data['Road condition']=QFS_data['Road condition'].apply(lambda x: str(x).replace('-',' '))
    QFS_data['Road condition']=QFS_data['Road condition'].apply(lambda x: str(x).replace(';', '/'))
    QFS_data['Weather']=QFS_data['Weather'].apply(lambda x: str(x).replace('Ambiant','Ambient'))
    QFS_data['Weather'] = QFS_data['Weather'].apply(lambda x: str(x).replace(';', '/'))
    QFS_data['Mileage']=QFS_data['Mileage'].apply(lambda x: str(x).replace('km',''))
    QFS_data['Mileage'] = QFS_data['Mileage'].apply(lambda x: str(x).replace('nan', ''))


    #description
    QFS_data['Description']=QFS_data['Description'].apply(lambda x: str(x).replace('\n','')[:3800])
    #drop duplicate
    QFS_data.drop_duplicates(keep='first', inplace=True)
    QFS_data = QFS_data.loc[QFS_data['Failure location'] != 'Delete', :]
    QFS_data = QFS_data.loc[QFS_data['Failure location'] != 'Nan', :]
    QFS_data = QFS_data.loc[QFS_data['Failure location'] != 'Na', :]
    QFS_data.replace('NA', np.nan, inplace=True)
    QFS_data.replace('nan', np.nan, inplace=True)
    return QFS_data

def month_update():
    # single sensor
    warranty = clean_warranty('Repair_list.xlsx')
    cac = clean_cac('Mastersheet_CAC_0604.xlsx')
    online = clean_online('Dashboard-MB-201801-05.xlsx')
    tips = clean_tips('TIPS_list.xlsx')
    aqsiq = clean_aqsiq('AQSIQ.xlsx')
    crm = clean_crm('CRM_list.xlsx')
    # all sensor
    QFS_data = pd.concat([warranty, cac, online, tips, aqsiq, crm], axis=0)
    QFS_data = clean_all(QFS_data)
    return QFS_data

def all_update():
    QFS_data=pd.DataFrame()
    #for sensor in ['tips']:
    for sensor in ['warranty','cac','online','tips','aqsiq','crm']:
        sensor_path=os.path.join(os.getcwd(),sensor)
        for file in os.listdir(sensor_path):
            sensor_file=os.path.join(sensor_path,file)
            if sensor =='warranty':
                warranty=clean_warranty(sensor_file)
                QFS_data=pd.concat([QFS_data, warranty],axis=0,ignore_index=True)
                print("Warranty is done:",file,', +Rows:',len(QFS_data))
            elif sensor =='cac':
                QFS_data=QFS_data.append(clean_cac(sensor_file), ignore_index=True)
                print("CAC is done:",file,', +Rows:',len(QFS_data))
            elif sensor =='online':
                QFS_data=QFS_data.append(clean_online(sensor_file), ignore_index=True)
                print("Online is done:",file,', +Rows:',len(QFS_data))
            elif sensor =='aqsiq':
                QFS_data=QFS_data.append(clean_aqsiq(sensor_file), ignore_index=True)
                print("AQSIQ is done:",file,', +Rows:',len(QFS_data))
            elif sensor =='crm':
                QFS_data=QFS_data.append(clean_crm(sensor_file), ignore_index=True)
                print("CRM is done:",file,' ,+Rows:',len(QFS_data))
            elif sensor == 'tips':
                QFS_data=QFS_data.append(clean_tips(sensor_file), ignore_index=True)
                print("TIPS is done:",file,', +Rows:',len(QFS_data))
    QFS_data = clean_all(QFS_data)
    return QFS_data


if '__main__' == __name__:
    #choose monthly update or all file update

    #QFS_data = month_update()
    QFS_data = all_update()
    #assert QFS_data.loc[QFS_data['Month age'] < 0, :].shape[0] > 30
    #assert QFS_data.loc[QFS_data['Failure location']=='NA',:].shape[0]>50
    #assert QFS_data.loc[ QFS_data['Failure type'] == 'NA',:].shape[0]>50
    #save to csv
    QFS_data.to_csv("QFS_data.csv",sep=',',index=False,encoding='utf-8-sig')
    #save to excel
    writer = pd.ExcelWriter('QFS_data.xlsx')
    QFS_data.to_excel(writer, 'Sheet1', index=False)
    writer.save()

