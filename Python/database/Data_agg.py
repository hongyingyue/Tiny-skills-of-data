from preprocess import *
from english_blank import *


QFS_data=pd.read_excel('QFS_data.xlsx')

QFS_data['Failure location']=QFS_data['Failure location'].apply(lambda x: str(x).capitalize())
QFS_data['Failure type']=QFS_data['Failure type'].apply(lambda x: str(x).capitalize())
QFS_data['Complaints']=QFS_data['Failure location'].astype(str)+'-'+QFS_data['Failure type'].astype(str)
QFS_data['Complaints']=QFS_data['Complaints'].apply(lambda x: x.replace(' ',''))



other_rule_file='Rules update_other sensors_20181105'
other_rules=pd.read_excel(other_rule_file+'.xlsx')
pattern=re.compile(r"\ASEC|SUV|CC|SMART")
other_rules['Descriptioninothersensors']=other_rules['Descriptioninothersensors'].apply(lambda x: re.sub(pattern,'',x))

other_rules['Failure location1']=other_rules['Issue'].apply(lambda x: x.split('-')[0])
other_rules['Failure location1']=other_rules['Failure location1'].apply(lambda x: re.sub(pattern,'',x))
other_rules['Failure location1']=other_rules['Failure location1'].apply(lambda x: infer_spaces(x).replace(' / ','/').replace(' - ','-'))
other_rules['Failure type1']=other_rules['Issue'].apply(lambda x: x.split('-')[-1])
other_rules['Failure type1']=other_rules['Failure type1'].apply(lambda x: infer_spaces(x).replace(' / ','/').replace(' - ','-'))



QFS_data=QFS_data.merge(other_rules.loc[:,['Descriptioninothersensors','Failure location1','Failure type1']],
                  left_on='Complaints',right_on='Descriptioninothersensors',how='left')



QFS_data.loc[~QFS_data['Failure location1'].isnull(),'Failure location']=QFS_data.loc[~QFS_data['Failure location1'].isnull(),'Failure location1']
QFS_data.loc[~QFS_data['Failure type1'].isnull(),'Failure type']=QFS_data.loc[~QFS_data['Failure type1'].isnull(),'Failure type1']
#QFS_data.drop(['Complaints','Descriptioninothersensors','Failure location1','Failure type1'],axis=1,inplace=True)
QFS_data.drop_duplicates(inplace=True)

QFS_data.to_csv('temp1.csv',sep=';')
