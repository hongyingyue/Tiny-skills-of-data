import pandas as pd
import numpy as np

tips=pd.read_excel("Copy of Tips Mar. 2018 (002).xlsx")
survey=pd.read_excel("dealer_processed_0404.xlsx",sheetname=0)
survey.columns=survey.columns.str.replace(" ","")

def top_carline(data):
    carline=data.groupby('Carline',as_index=False)['Complaints'].count()
    carline.sort_values(by='Complaints',ascending=False,inplace=True)
    carline=carline.reset_index()
    sum=np.sum(carline['Complaints'])
    i,back=0,0
    while back<sum*0.5:
        back+=carline['Complaints'][i]
        i=i+1
    return list(carline['Carline'])[:i]

for i,data in enumerate([tips,survey]):
    data['Complaints'] = data['Tier1'] + " " + data['Tier3']
    if i==0:
        data_sum = data.groupby('Complaints')['Complaints'].count()
    elif i==1:
        data_sum = data.groupby('Complaints')['Num'].sum()
    data_sum = data_sum.to_frame(name='data_Value').reset_index()
    data_sum.sort_values(by='data_Value', ascending=False, inplace=True)
    data_max = np.max(data_sum['data_Value'])
    data_sum['data_Score'] = data_sum['data_Value'] / data_max
    data_carline = data.groupby('Complaints')['Complaints', 'Carline'].apply(lambda x: top_carline(x))
    data_carline = data_carline.to_frame(name='Carline').reset_index()
    if i==0:
        tips_ = pd.merge(data_sum, data_carline, on='Complaints', how='left')
    elif i==1:
        survey_=pd.merge(data_sum, data_carline, on='Complaints', how='left')

dealer=pd.merge(tips_,survey_,on='Complaints',how='outer').fillna(0)
dealer['Score']=dealer['data_Score_x']+dealer['data_Score_y']
dealer.sort_values(by='Score',ascending=False,inplace=True)
print(dealer)
dealer.to_csv("dealer result.csv",sep=';',index=False)


print("Dealer survey: ",sum(survey['Num'])/len(set(survey['Dealer'])))
print("TIPS: ",len(tips))


'''


tips['Complaints']=tips['Tier1']+" "+tips['Tier3']
tips_sum=tips.groupby('Complaints')['Complaints'].count()
tips_sum=tips_sum.to_frame(name='tips_Value').reset_index()
tips_sum.sort_values(by='tips_Value',ascending=False,inplace=True)
tips_max=np.max(tips_sum['tips_Value'])
tips_sum['tips_Score']=tips_sum['tips_Value']/tips_max
tips_carline=tips.groupby('Complaints')['Complaints','Carline'].apply(lambda x: top_carline(x))
tips_carline=tips_carline.to_frame(name='Carline').reset_index()
tips_sum=pd.merge(tips_sum,tips_carline,on='Complaints',how='left')




survey['Complaints']=survey['Tier 1']+" "+survey['Tier 3']
survey['Num']=survey['Num'].astype('float32')
survey_sum=survey.groupby('Complaints')['Num'].sum() #problem: all 2.5 are count as 3
survey_sum=survey_sum.to_frame(name='survey_Value').reset_index()
survey_sum.sort_values(by='survey_Value',ascending=False,inplace=True)
survey_max=np.max(survey_sum['survey_Value'])
survey_sum['survey_Score']=survey_sum['survey_Value']/survey_max
#survey_sum['survey_Carline']=top_carline(tips)

dealer=pd.merge(tips_sum,survey_sum,on='Complaints',how='outer')
dealer['Score']=dealer['tips_Score']+dealer['survey_Score']
dealer.sort_values(by='Score',ascending=False,inplace=True)
dealer.to_csv("dealer result.csv",sep=';')

'''
