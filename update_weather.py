import requests
import os
from datetime import datetime, timedelta

# 1. 설정: 충남 서산, 한국어, 미터법
CITY = "Seosan,KR"
API_KEY = os.getenv("OPENWEATHER_API_KEY")
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"

README_PATH = "README.md"

def get_weather_emoji(weather_id):
    # 날씨 코드에 따른 이모지 선택
    if 200 <= weather_id <= 232: return "⚡"  # 뇌우
    if 300 <= weather_id <= 321: return "🌧️"  # 이슬비
    if 500 <= weather_id <= 531: return "☔"  # 비
    if 600 <= weather_id <= 622: return "☃️"  # 눈
    if 701 <= weather_id <= 781: return "🌫️"  # 안개
    if weather_id == 800: return "☀️"        # 맑음
    if 801 <= weather_id <= 804: return "☁️"  # 구름
    return "🌡️"

def get_weather():
    if not API_KEY:
        # 로컬 테스트용 (API키가 없을 때)
        return None
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def update_readme():
    data = get_weather()
    
    # 한국 시간(KST) = UTC + 9시간
    kst_now = datetime.utcnow() + timedelta(hours=9)
    formatted_time = kst_now.strftime("%Y년 %m월 %d일 %p %I:%M (KST)")

    if data:
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        weather_desc = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]
        humidity = data["main"]["humidity"]
        emoji = get_weather_emoji(weather_id)
        
        # 예쁜 README 내용 작성
        readme_content = f"""# 🌤️ 오늘의 서산 날씨

충남 서산(Seosan)의 날씨 정보를 자동으로 업데이트합니다.

| 위치 | 날씨 | 기온 | 체감 온도 | 습도 |
|:---:|:---:|:---:|:---:|:---:|
| **📍 서산 (Seosan)** | {emoji} {weather_desc} | **{temp:.1f}°C** | {feels_like:.1f}°C | 💧 {humidity}% |

<div align="right">
  
  ⏳ 업데이트: {formatted_time}
</div>

---
*이 정보는 GitHub Actions 봇이 주기적으로 확인하여 갱신합니다.*
"""
    else:
        readme_content = f"""# 🌤️ 오늘의 서산 날씨

⚠️ 날씨 정보를 가져오는 데 실패했습니다. 

⏳ 확인 시간: {formatted_time}
"""

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)

if __name__ == "__main__":
    update_readme()
