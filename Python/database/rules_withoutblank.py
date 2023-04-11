from preprocess import *


rule_file='Rule_20181126'
rules=pd.read_excel(rule_file+'.xlsx')
pattern=re.compile(r"\ASEC|SUV|CC|SMART")
rules['Issue before grouping']=rules['Issue before grouping'].apply(lambda x: re.sub(pattern,'',x))

rules['Failure location1']=rules['Issue before grouping'].apply(lambda x: x.split('-')[0])
rules['Failure location1']=rules['Failure location1'].apply(lambda x: infer_spaces(x).replace(' / ', '/').replace(' - ', '-').replace(' ( ','(').replace(' ) ',')'))
rules['Failure type1']=rules['Issue before grouping'].apply(lambda x: x.split('-')[-1])
rules['Failure type1']=rules['Failure type1'].apply(lambda x: infer_spaces(x).replace(' / ', '/').replace(' - ', '-').replace(' (','(').replace('( ','(').replace(' )',')').replace(') ',')'))

rules.to_csv('Rules.csv',sep=';',index=False)

