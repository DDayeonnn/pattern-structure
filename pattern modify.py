import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# ==============================
# 0. 한글 폰트 설정
# ==============================
mpl.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['font.size'] = 12
# ==============================
# 1. 데이터 불러오기
# ==============================
file_path = r"D:/DY/py_data/250701-250811_df.csv"

df = pd.read_csv(file_path, encoding='euc-kr', low_memory=False)

# 날짜/시간 처리
df['startTime'] = pd.to_datetime(df['startTime'], errors='coerce')

# 특정 날짜만 필터
df = df[df['startTime_Date'] == 20250701].copy()

print("원본 데이터 건수:", len(df))
print(df['activity'].unique())

# ==============================
# 2. activity 그룹화
# ==============================
activity_mapping1 = {
    '진료실도착(대면)': '진료',
    '진료실도착(키오스크)': '진료',
    '진료준비완료': '진료',
    '진료내실(의사)': '진료',
    '진료내실(간호사)': '진료',
    '진료완료(첫처방)': '진료',
    '채혈환자도착': '채혈',
    '채혈환자호출': '채혈',
    '채혈': '채혈',
    '재진료변경': '진료',
    '진료준비완료(당일)': '진료'
}

activity_mapping2 = {
    '진료실도착(대면)': '진료',
    '진료실도착(키오스크)': '진료',
    '진료준비완료': '진료',
    '진료내실(의사)': '진료',
    '진료내실(간호사)': '진료',
    '진료완료(첫처방)': '진료',
    '채혈환자도착': '채혈준비',
    '채혈환자호출': '채혈준비',
    '채혈': '채혈',
    '재진료변경': '진료',
    '진료준비완료(당일)': '진료'
}

df['Activity_Group1'] = df['activity'].map(activity_mapping1)
df['Activity_Group2'] = df['activity'].map(activity_mapping2)

# ==============================
# 3. 특정 조건의 진료완료(첫처방) → 처방 변경
# ==============================
preceding_activities = [
    '진료실도착(대면)', '진료실도착(키오스크)', '진료준비완료',
    '진료내실(의사)', '진료내실(간호사)', '재진료변경', '진료준비완료(당일)'
]
target_activity = '진료완료(첫처방)'

patient_activities = df.groupby('new_patNo')['activity'].agg(set)

valid_patNos = patient_activities[
    patient_activities.apply(lambda x: target_activity in x) &
    patient_activities.apply(lambda x: x.isdisjoint(preceding_activities))
].index

condition = (df['new_patNo'].isin(valid_patNos)) & (df['activity'] == target_activity)

df.loc[condition, 'Activity_Group1'] = '처방'
df.loc[condition, 'Activity_Group2'] = '처방'

# ==============================
# 4. Activity_Group2 기준 연속 중복 제거
# ==============================
df = df.sort_values(by=['new_patNo', 'startTime']).copy()

df['is_duplicate'] = (
    df['Activity_Group2'] == df.groupby('new_patNo')['Activity_Group2'].shift()
)

df_collapsed = df[~df['is_duplicate']].copy()

print("중복 제거 전:", len(df))
print("중복 제거 후:", len(df_collapsed))

# ==============================
# 5. 채혈안함 분류
# ==============================
patient_activity2 = df_collapsed.groupby('new_patNo')['Activity_Group2'].agg(set)

no_blood_test_patNos = patient_activity2[
    patient_activity2.apply(lambda x: '채혈준비' in x) &
    patient_activity2.apply(lambda x: '채혈' not in x)
].index

df_collapsed['pattern'] = '기타'
df_collapsed.loc[df_collapsed['new_patNo'].isin(no_blood_test_patNos), 'pattern'] = '채혈안함'

# ==============================
# 6. 채혈안함이 아닌 환자의 패턴 생성
#    (Activity_Group1 기준, 연속 중복 제거)
# ==============================
df_for_pattern = df_collapsed[df_collapsed['pattern'] != '채혈안함'].copy()
df_for_pattern = df_for_pattern.sort_values(['new_patNo', 'startTime'])

df_for_pattern['prev_group1'] = df_for_pattern.groupby('new_patNo')['Activity_Group1'].shift()
df_for_pattern = df_for_pattern[df_for_pattern['Activity_Group1'] != df_for_pattern['prev_group1']]

pattern_map = (
    df_for_pattern.groupby('new_patNo')['Activity_Group1']
    .apply(lambda x: ' -> '.join(x.dropna().astype(str)))
)

mask = df_collapsed['pattern'] != '채혈안함'
df_collapsed.loc[mask, 'pattern'] = df_collapsed.loc[mask, 'new_patNo'].map(pattern_map)

# ==============================
# 7. 환자별 패턴 테이블 생성
# ==============================
patient_pattern = df_collapsed[['new_patNo', 'pattern']].drop_duplicates().copy()

print("\n환자별 pattern 개수")
print(patient_pattern['pattern'].value_counts())

# ==============================
# 8. 패턴 그룹 재분류
# ==============================
def regroup_pattern(x):
    if x in ['진료 -> 채혈', '진료 -> 채혈 -> 진료']:
        return '진료 -> 채혈 계열'
    elif x in ['채혈 -> 진료', '채혈 -> 진료 -> 채혈']:
        return '채혈 -> 진료 계열'
    elif x in ['진료 -> 채혈 -> 진료 -> 채혈', '진료 -> 채혈 -> 진료 -> 채혈 -> 진료']:
        return '진료 -> 채혈 -> 진료 -> 채혈 계열'
    else:
        return x

patient_pattern['pattern_group'] = patient_pattern['pattern'].apply(regroup_pattern)

print("\n환자별 pattern_group 개수")
print(patient_pattern['pattern_group'].value_counts())

# ==============================
# 9. 첫 채혈환자호출 시간 추출
# ==============================
call_df = df[df['activity'] == '채혈환자호출'].copy()

first_call_time = (
    call_df.groupby('new_patNo')['startTime']
    .min()
    .reset_index()
    .rename(columns={'startTime': 'first_call_time'})
)

# merge (모든 환자 기준)
patient_pattern = patient_pattern.merge(first_call_time, on='new_patNo', how='left')

# 시간대 추출
patient_pattern['hour'] = patient_pattern['first_call_time'].dt.hour

# ==============================
# 10. 패턴 그룹 × 첫 채혈 시간대 집계
# ==============================
pattern_hour_count_grouped = (
    patient_pattern
    .groupby(['pattern_group', 'hour'])
    .size()
    .reset_index(name='count')
)

pivot_grouped = pattern_hour_count_grouped.pivot(
    index='pattern_group',
    columns='hour',
    values='count'
).fillna(0)

# 컬럼명 변경
pivot_grouped = pivot_grouped.rename(columns={-1.0: '채혈없음', -1: '채혈없음'})

# ==============================
# 11. 원하는 순서로 정렬
# ==============================
pattern_order = [
    '채혈',
    '진료 -> 채혈 계열',
    '채혈안함',
    '채혈 -> 진료 계열',
    '처방 -> 채혈',
    '진료 -> 채혈 -> 진료 -> 채혈 계열'
]

# 실제 존재하는 패턴만 남기고 순서 반영
existing_patterns = [p for p in pattern_order if p in pivot_grouped.index]
remaining_patterns = [p for p in pivot_grouped.index if p not in existing_patterns]
pivot_grouped = pivot_grouped.reindex(existing_patterns + remaining_patterns).fillna(0)

# 시간대 컬럼 순서 정렬
def sort_hour_col(col):
    if col == '채혈없음':
        return -1
    return col

pivot_grouped = pivot_grouped[sorted(pivot_grouped.columns, key=sort_hour_col)]

print("\n최종 피벗 테이블")
print(pivot_grouped)

# ==============================
# 12. 그래프 그리기
# ==============================
pivot_ratio = pivot_grouped.div(pivot_grouped.sum(axis=0), axis=1)

ax = pivot_ratio.T.plot(
    kind='bar',
    stacked=True,
    figsize=(14, 6),
    colormap='tab20'
)

plt.title('시간대별 패턴 비율', fontsize=16)
plt.xlabel('시간대')
plt.ylabel('비율')

for i, hour in enumerate(pivot_ratio.columns):
    bottom = 0
    for pattern in pivot_ratio.index:
        value = pivot_ratio.loc[pattern, hour]

        if value > 0.03:
            color = 'white' if value > 0.1 else 'black'

            ax.text(
                i,
                bottom + value / 2,
                f'{value*100:.0f}%',
                ha='center',
                va='center',
                fontsize=10,
                color=color,
                fontweight='bold'
            )

        bottom += value

plt.legend(bbox_to_anchor=(1.05,1))
plt.tight_layout()
plt.show()

