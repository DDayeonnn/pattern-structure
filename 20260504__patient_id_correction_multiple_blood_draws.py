import pandas as pd

file_path = r"D:\DY\py_data\case_result2.csv"

df = pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False)
df.columns = df.columns.str.strip()

df['startTime'] = pd.to_datetime(df['startTime'])

# 같은 시간일 때 activity 순서 강제 지정
activity_order = {
    '채혈환자도착': 1,
    '채혈환자호출': 2,
    '채혈': 3
}

df['activity_order'] = df['activity'].map(activity_order).fillna(99)

# 중요: startTime이 같으면 도착 → 호출 → 채혈 순서로 정렬
df = df.sort_values(
    ['new_patNo', 'startTime', 'activity_order']
).copy()

df['blood_case_no'] = 1

for patno, g in df.groupby('new_patNo'):
    activities = g['activity'].tolist()
    idx_list = g.index.tolist()

    case_no = 1
    seen_blood = False
    pending_start = None
    result = [1] * len(g)

    for i, act in enumerate(activities):

        # 채혈 완료 후 새로운 도착이 나오면 새 케이스 후보
        if act == '채혈환자도착' and seen_blood and pending_start is None:
            pending_start = i

        # 새 케이스 후보 이후 채혈이 나오면 새 케이스 확정
        if act == '채혈' and pending_start is not None:
            case_no += 1

            for j in range(pending_start, i + 1):
                result[j] = case_no

            pending_start = None
            seen_blood = True

        elif act == '채혈':
            seen_blood = True

        result[i] = case_no if pending_start is None else result[i]

    df.loc[idx_list, 'blood_case_no'] = result

df['new_patno_case'] = (
    df['new_patNo'].astype(str) + '_' +
    df['blood_case_no'].astype(str)
)

# 확인
print(df[['new_patNo', 'new_patno_case', 'patNo', 'activity', 'startTime', 'blood_case_no']].head(30))

test=df[df['new_patNo']=='250156737_20250708_MO']
print(test.head())

output_path = r"D:\DY\py_data\case_result2.csv"
df.to_csv(output_path, index=False, encoding='utf-8-sig')