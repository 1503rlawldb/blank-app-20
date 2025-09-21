import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt
from datetime import datetime

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="물러서는 땅, 다가오는 바다",
    page_icon="🌊",
    layout="wide"
)

# ----------------------------
# 1. 좌측 조작 옵션
# ----------------------------
st.sidebar.header("보기 옵션")

# 날짜 선택 (년도 단위)
year = st.sidebar.slider("년도 선택", 1800, 2025, 2024)

# 지역 선택
region = st.sidebar.selectbox("지역 선택", ["전 세계", "대한민국", "투발루", "몰디브", "방글라데시", "네덜란드"])

# 색상 범위 조절
temp_range = st.sidebar.slider("색상 범위 절대값 (°C)", 1, 10, 5)

# 지도 투영 방식 (샘플)
projection = st.sidebar.selectbox("투영(화면)", ["Robinson", "Equirectangular", "Mercator"])

# ----------------------------
# 2. 지도 데이터 (샘플 생성)
# ----------------------------
# 샘플 격자 데이터
lats = np.linspace(-60, 80, 50)
lons = np.linspace(-180, 180, 100)
temp_anomaly = np.random.uniform(-temp_range, temp_range, size=(len(lats)*len(lons)))

df_map = pd.DataFrame({
    "lat": np.repeat(lats, len(lons)),
    "lon": np.tile(lons, len(lats)),
    "anomaly": temp_anomaly
})

# ----------------------------
# 3. 지도 시각화
# ----------------------------
st.subheader(f"🌍 해수면·기온 변화 지도 ({year}년 기준)")
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(latitude=0, longitude=0, zoom=1),
    layers=[
        pdk.Layer(
            "HeatmapLayer",
            data=df_map,
            get_position=["lon", "lat"],
            get_weight="anomaly",
            radiusPixels=30,
            opacity=0.6
        )
    ]
))

# ----------------------------
# 4. 나라별 피해 사례 / 대처 방안
# ----------------------------
case_study = {
    "투발루": {
        "피해": "국토의 40% 이상이 침수 위협을 받고 있으며, 주민들의 해외 이주가 현실화되고 있음.",
        "대처": "국제 사회에 기후 난민 보호 요청, 해안 방벽 설치 시도."
    },
    "몰디브": {
        "피해": "리조트와 주거지가 반복적인 홍수 피해를 입음.",
        "대처": "인공섬 건설, 해안 방파제 강화."
    },
    "방글라데시": {
        "피해": "델타 지역 농경지와 마을이 매년 침수됨.",
        "대처": "방조제 건설, 홍수 예측 시스템 개발."
    },
    "네덜란드": {
        "피해": "과거 해수면 상승과 폭풍으로 국토 침수 경험.",
        "대처": "세계적 수준의 방조제·수문 관리 시스템 구축."
    },
    "대한민국": {
        "피해": "인천·부산 등 해안 도시 침수 위험 증가.",
        "대처": "연안관리 기본계획 수립, 해안 방벽·배수 시설 확충."
    }
}

if region in case_study:
    st.markdown(f"### 📍 {region} 피해 사례 & 대처 방안")
    st.write(f"**피해 사례:** {case_study[region]['피해']}")
    st.write(f"**대처 방안:** {case_study[region]['대처']}")

# ----------------------------
# 5. 현재(2025) vs 선택년도 비교
# ----------------------------
st.subheader("📊 해수면 상승 수치 비교")

current_sea_level = 21.0  # cm (예시)
selected_sea_level = round(np.random.uniform(0, current_sea_level), 2)

col1, col2 = st.columns(2)
col1.metric(f"{year}년 해수면 상승(cm)", selected_sea_level)
col2.metric("2025년 해수면 상승(cm)", current_sea_level, delta=f"{current_sea_level-selected_sea_level:.2f} cm")

# ----------------------------
# 6. 투발루 피해 특별 강조
# ----------------------------
st.subheader("🌊 투발루의 위기")
st.info("투발루는 해수면 상승으로 국토 대부분이 침수 위기에 처해 있으며, 기후 난민 문제가 국제적 이슈로 떠오르고 있습니다.")

# ----------------------------
# 7. 해수면 상승 인지도 체크박스
# ----------------------------
st.subheader("📝 성찰: 나는 얼마나 알고 있을까?")
st.checkbox("해수면 상승이 내 삶에 영향을 줄 수 있다고 생각한다.")
st.checkbox("국제 사회가 함께 해결해야 한다고 생각한다.")
st.checkbox("개인적으로 기후 행동에 참여할 의향이 있다.")

# ----------------------------
# 8. 출처
# ----------------------------
st.markdown("---")
st.markdown("#### 📚 출처")
st.markdown("""
- [IPCC Reports](https://www.ipcc.ch/)  
- [NASA Climate Change](https://climate.nasa.gov/)  
- [NOAA Sea Level Rise](https://coast.noaa.gov/slr/)  
""")
