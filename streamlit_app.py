import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# -----------------------
# 국가별 피해/대처 데이터
# -----------------------
country_info = {
    "투발루": {
        "피해": "평균 해발 2~3m로 해수면 상승에 가장 취약. 농경지와 식수원 침수, 환경 난민 발생.",
        "대처": "국제 사회에 이민 요청, 기후변화 협약에서 생존권 보장을 요구."
    },
    "방글라데시": {
        "피해": "우기마다 수백만 명의 농민이 침수 피해를 입음.",
        "대처": "대규모 제방 건설, 기후 난민 정책 추진."
    },
    "몰디브": {
        "피해": "일부 섬이 바닷물에 잠겨 거주 불가능 지역 증가.",
        "대처": "관광 수익으로 해안 방어 시설 건설, 산호초 복원."
    },
    "네덜란드": {
        "피해": "저지대 국가 특성상 해수면 상승 위협이 큼.",
        "대처": "첨단 방조제와 수문 시스템 운영."
    },
    "미국 마이애미": {
        "피해": "‘Sunny Day Flooding’으로 도로가 주기적으로 침수.",
        "대처": "해안 방어벽 건설, 배수 시스템 강화."
    },
    "인도네시아 자카르타": {
        "피해": "해수면 상승과 지반 침하로 도심 침수 심각. 수도 이전 논의.",
        "대처": "누산타라 수도 이전, 대규모 방조제 건설."
    }
}

# -----------------------
# Streamlit UI
# -----------------------
st.title("🌊 해수면 상승 & 기온 변화 대시보드")

# 좌측 사이드바 옵션
st.sidebar.header("보기 옵션")
date = st.sidebar.date_input("날짜 선택")
region = st.sidebar.selectbox("영역 선택", ["전 지구", "북반구", "남반구"])
scale = st.sidebar.slider("색상 범위 절대값 (°C)", 1, 6, 4)
proj_option = st.sidebar.selectbox("투영(화면)", ["Robinson", "PlateCarree", "Mollweide"])

# -----------------------
# 지도 시뮬레이션 (가짜 데이터 예시)
# -----------------------
lon = np.linspace(-180, 180, 360)
lat = np.linspace(-90, 90, 180)
lon2d, lat2d = np.meshgrid(lon, lat)

# 임시 데이터: 위도 기반 온도 편차
temp_anomaly = 2 * np.sin(np.radians(lat2d)) + np.random.normal(0, 0.5, size=lat2d.shape)

# 투영 선택
if proj_option == "Robinson":
    proj = ccrs.Robinson()
elif proj_option == "Mollweide":
    proj = ccrs.Mollweide()
else:
    proj = ccrs.PlateCarree()

fig = plt.figure(figsize=(10,5))
ax = plt.axes(projection=proj)
ax.set_global()
cmap = plt.cm.RdBu_r
im = ax.pcolormesh(lon, lat, temp_anomaly, transform=ccrs.PlateCarree(),
                   cmap=cmap, vmin=-scale, vmax=scale)
ax.coastlines()
plt.colorbar(im, orientation="horizontal", pad=0.05, label="해수면/온도 편차 (°C)")
st.pyplot(fig)

# -----------------------
# 국가 검색
# -----------------------
country = st.text_input("국가명을 입력하세요 (예: 투발루, 방글라데시, 몰디브 등)")

if country in country_info:
    st.subheader(f"📍 {country} 피해 사례 & 대처 방안")
    st.markdown(f"- **피해 사례:** {country_info[country]['피해']}")
    st.markdown(f"- **대처 방안:** {country_info[country]['대처']}")
else:
    if country:
        st.warning("❌ 해당 국가 데이터가 없습니다.")

# -----------------------
# 출처
# -----------------------
st.markdown("""
---
📌 **데이터 출처**  
- IPCC (2021) "Sixth Assessment Report"  
- NASA Sea Level Change Team  
- NOAA (National Oceanic and Atmospheric Administration)  
""")
