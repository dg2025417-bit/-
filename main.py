import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
# 페이지 기본 설정
# ─────────────────────────────────────────────
st.set_page_config(page_title="청소년 SNS와 정신건강", layout="wide")
st.title("📱 하루 SNS 사용량과 학생 생활 지표 비교")
st.write("당곡고등학교 데이터 탐구 - SNS 사용 시간을 30분 단위로 비교합니다.")

# ─────────────────────────────────────────────
# 데이터 불러오기 (영어 → 한글 번역)
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Teen_Mental_Health_Dataset.csv")

    df["gender"] = df["gender"].map({"male": "남성", "female": "여성"})
    df["platform_usage"] = df["platform_usage"].map({
        "Instagram": "인스타그램", "TikTok": "틱톡", "Both": "둘 다"
    })
    df["social_interaction_level"] = df["social_interaction_level"].map({
        "low": "낮음", "medium": "보통", "high": "높음"
    })

    df = df.rename(columns={
        "age": "나이", "gender": "성별",
        "daily_social_media_hours": "하루SNS사용시간",
        "platform_usage": "사용플랫폼", "sleep_hours": "수면시간",
        "screen_time_before_sleep": "취침전스크린시간",
        "academic_performance": "학업성취도", "physical_activity": "신체활동량",
        "social_interaction_level": "사회적상호작용",
        "stress_level": "스트레스수준", "anxiety_level": "불안수준",
        "addiction_level": "중독수준", "depression_label": "우울증여부"
    })
    return df

df = load_data()

# ─────────────────────────────────────────────
# 숫자를 '○시간 ○분' 형태로 바꿔주는 함수
# ─────────────────────────────────────────────
def 시간표시(숫자):
    시 = int(숫자)
    분 = int(round((숫자 - 시) * 60))
    if 분 == 0:
        return f"{시}시간"
    else:
        return f"{시}시간 {분}분"

# ─────────────────────────────────────────────
# 데이터 미리보기
# ─────────────────────────────────────────────
with st.expander("📋 데이터 미리보기 (클릭하여 펼치기)"):
    st.dataframe(df.head(20))
    st.write(f"전체 학생 수: {len(df)} 명")

# ─────────────────────────────────────────────
# 하루 SNS 사용시간을 0.5시간 단위 구간으로 나누기
# ─────────────────────────────────────────────
최소값 = df["하루SNS사용시간"].min()
최대값 = df["하루SNS사용시간"].max()

시작 = (int(최소값 * 2)) / 2
끝 = (int(최대값 * 2) + 1) / 2

구간경계 = []
값 = 시작
while 값 <= 끝:
    구간경계.append(round(값, 1))
    값 += 0.5

구간이름 = []
for i in range(len(구간경계) - 1):
    구간이름.append(f"{시간표시(구간경계[i])} ~ {시간표시(구간경계[i+1])}")

df["SNS사용구간"] = pd.cut(df["하루SNS사용시간"], bins=구간경계,
                          labels=구간이름, right=False)

# 구간별 평균 계산
평균표 = df.groupby("SNS사용구간")[
    ["수면시간", "학업성취도", "신체활동량", "스트레스수준"]
].mean().round(2)

# 그래프 종류 선택
st.write("---")
그래프종류 = st.radio(
    "보고 싶은 그래프 종류를 선택하세요",
    ["막대그래프", "꺾은선 그래프"],
    horizontal=True
)
st.write("---")

# ─────────────────────────────────────────────
# 그래프 그리는 함수
# - columns로 가로 길이 줄이기
# - height로 세로 길이 키워서 차이 잘 보이게
# ─────────────────────────────────────────────
그래프높이 = 450   # 그래프 세로 길이 (숫자가 클수록 막대 차이가 잘 보임)

def 그래프그리기(지표이름):
    # 화면을 [1, 3, 1] 비율로 나눠 가운데(3)에만 그래프 → 가로 길이 줄임
    여백왼, 가운데, 여백오 = st.columns([1, 3, 1])
    with 가운데:
        if 그래프종류 == "막대그래프":
            st.bar_chart(평균표[지표이름], height=그래프높이)
        else:
            st.line_chart(평균표[지표이름], height=그래프높이)

# ─────────────────────────────────────────────
# 4가지 지표를 각각 따로 그리기
# ─────────────────────────────────────────────
st.header("📊 SNS 사용 구간별 지표 비교 (30분 단위)")

st.subheader("😴 수면시간")
그래프그리기("수면시간")

st.subheader("📚 학업성취도")
그래프그리기("학업성취도")

st.subheader("🏃 신체활동량")
그래프그리기("신체활동량")

st.subheader("😣 스트레스수준")
그래프그리기("스트레스수준")

# ─────────────────────────────────────────────
# 평균값 표로 정리
# ─────────────────────────────────────────────
st.header("📑 구간별 평균값 표")
st.dataframe(평균표, use_container_width=True)

st.info(
    "💡 그래프 보는 팁\n\n"
    "- 그래프 세로 길이를 키우면 막대 사이의 작은 차이도 잘 보여요!\n"
    "- 단, 차이가 실제보다 커 보일 수 있으니 '실제 값(표)'도 함께 확인하세요."
)
