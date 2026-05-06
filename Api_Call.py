import requests
import pandas as pd

url = "https://openapi.hallym.or.kr:8443/md_api/digitaltwin.jsp?IsGubun=DATELIST&stdate=20250701&sttime=00:01&eddate=20250701&edtime=23:59"

response = requests.get(url)
data = response.json() # JSON → dict

df = pd.DataFrame(data)
print(df.head())


'''
print(df['eventname'].unique())
event_list = df['eventname'].unique()
event_df = pd.DataFrame(event_list, columns=['eventname'])
print(event_df)
'''
df.to_excel("D:/DY/df20250701.xlsx", index=False)

