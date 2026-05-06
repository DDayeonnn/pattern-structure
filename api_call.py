# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 16:21:28 2026

@author: hallym
"""

import requests
import pandas as pd

url = "https://openapi.hallym.or.kr:8443/md_api/digitaltwin.jsp?IsGubun=DATELIST&stdate=20260201&sttime=00:01&eddate=20260228&edtime=23:59"

response = requests.get(url)

data = response.json()  # JSON → dict

df = pd.DataFrame(data)

print(df['eventname'].unique())

"""
# 필요한 activity만 필터링
df_filtered = df[df['eventname'].isin(['채혈실 번호표 발행(키오스크)', '채혈바코드 발행 시간', '채혈결과보고 시간', '채혈실 환자 호출시간', '채혈 대기 시간'])]

# csv파일로 저장
df.to_csv(r"D:\DY\result.csv", index=False, encoding='cp949')
"""