import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
# 페이지 기본 설정
# ─────────────────────────────────────────────
st.set_page_config(page_title="청소년 SNS와 정신건강", layout="wide")
st.title("📱 청소년 하루 SNS 사용량과 생활 지표 분석")
st.write("당곡고등학교 데이터 탐구 활동 - 하루 SNS 사용량에 따른 수면, 학업, 신체활동, 스트레스 비교")

# ─────────────────────────────────────────────
# 데이터 불러오기
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Teen_Mental_Health_Dataset.csv")

    # 영어 값을 한글로 번역
    df["gender"] = df["gender"].map({"male": "남성", "female": "여성"})
    df["platform_usage"] = df["platform_usage"].map({
        "Instagram": "인스타그램",
        "TikTok": "틱톡",
        "Both": "둘 다"
    })
    df["social_interaction_level"] = df["social_interaction_level"].map({
        "low": "낮음",
        "medium": "보통",
        "high": "높음"
    })

    # 열 이름을 한글로 번역
    df = df.rename(columns={
        "age": "나이",
        "gender": "성별",
        "daily_social_media_hours": "하루SNS사용시간",
        "platform_usage": "사용플랫폼",
        "sleep_hours": "수면시간",
        "screen_time_before_sleep": "취침전스크린시간",
        "academic_performance": "학업성취도",
        "physical_activity": "신체활동량",
        "social_interaction_level": "사회적상호작용",
        "stress_level": "스트레스수준",
        "anxiety_level": "불안수준",
        "addiction_level": "중독수준",
        "depression_label": "우울증여부"
    })
    return df

df = load_data()

# ─────────────────────────────────────────────
# 원본 데이터 미리보기
# ─────────────────────────────────────────────
with st.expander("📋 데이터 미리보기 (클릭하여 펼치기)"):
    st.dataframe(df.head(20))
    st.write(f"전체 데이터 수: {len(df)} 명")

# ─────────────────────────────────────────────
# 하루 SNS 사용시간을 구간으로 나누기
# ─────────────────────────────────────────────
st.header("📊 하루 SNS 사용량 구간별 평균 비교")

# 0~2, 2~4, 4~6, 6~8 시간 구간으로 분류
구간경계 = [0, 2, 4, 6, 8.1]
구간이름 = ["0~2시간", "2~4시간", "4~6시간", "6~8시간"]
df["SNS사용구간"] = pd.cut(df["하루SNS사용시간"], bins=구간경계,
                          labels=구간이름, right=False)

# 구간별 평균 계산
평균표 = df.groupby("SNS사용구간")[
    ["수면시간", "학업성취도", "신체활동량", "스트레스수준"]
].mean()

st.write("아래 그래프는 SNS 사용 시간 구간별 평균값을 보여줍니다.")

# ─────────────────────────────────────────────
# 비교할 지표 선택
# ─────────────────────────────────────────────
지표선택 = st.selectbox(
    "비교할 지표를 선택하세요",
    ["수면시간", "학업성취도", "신체활동량", "스트레스수준"]
)

st.subheader(f"📈 SNS 사용 구간별 평균 {지표선택}")
st.bar_chart(평균표[지표선택])

# ─────────────────────────────────────────────
# 4가지 지표 한눈에 비교 (라인 차트)
# ─────────────────────────────────────────────
st.subheader("📉 4가지 지표 한눈에 비교 (선 그래프)")
st.line_chart(평균표)

st.dataframe(평균표.round(2))

# ─────────────────────────────────────────────
# 산점도: SNS 사용시간 vs 선택 지표 (개별 데이터)
# ─────────────────────────────────────────────
st.header("🔍 개별 학생 데이터로 보는 관계 (산점도)")

산점도지표 = st.selectbox(
    "SNS 사용시간과 비교할 지표를 선택하세요",
    ["수면시간", "학업성취도", "신체활동량", "스트레스수준"],
    key="scatter"
)

st.scatter_chart(
    df,
    x="하루SNS사용시간",
    y=산점도지표
)

st.info("💡 점들의 분포를 보고 SNS 사용 시간과 각 지표 사이에 관계가 있는지 직접 탐구해 보세요!")
