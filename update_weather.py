import requests
import os
from datetime import datetime, timedelta

# 1. 설정: 충남 서산, 한국어
CITY = "Seosan,KR"
API_KEY = os.getenv("OPENWEATHER_API_KEY")
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"

README_PATH = "README.md"

def get_weather_emoji(weather_id):
    if 200 <= weather_id <= 232: return "⚡"
    if 300 <= weather_id <= 321: return "🌧️"
    if 500 <= weather_id <= 531: return "☔"
    if 600 <= weather_id <= 622: return "☃️"
    if 701 <= weather_id <= 781: return "🌫️"
    if weather_id == 800: return "☀️"
    if 801 <= weather_id <= 804: return "☁️"
    return "🌡️"

def get_weather_advice(weather_id):
    if 200 <= weather_id <= 232: return "천둥 번개가 쳐요! 🌩️ 외출을 자제하고 안전한 실내에 계세요."
    if 300 <= weather_id <= 531: return "비가 내려요. ☔ 튼튼한 우산 꼭 챙기시고 빗길 운전 조심하세요!"
    if 600 <= weather_id <= 622: return "눈이 내려요. ☃️ 옷 따뜻하게 챙겨 입으시고 빙판길 조심하세요!"
    if 701 <= weather_id <= 781: return "안개가 짙어요. 🌫️ 마스크 착용하시고 앞이 잘 안 보일 수 있으니 주의하세요."
    if weather_id == 800: return "날씨가 아주 좋아요! ☀️ 가벼운 산책이나 환기를 시켜보는 건 어때요?"
    if 801 <= weather_id <= 804: return "구름이 좀 있네요. ☁️ 그래도 활동하기엔 무난한 날씨예요."
    return "오늘도 서산에서 행복한 하루 보내세요! 🍀"

def get_weather():
    if not API_KEY: return None
    try:
        response = requests.get(URL, timeout=10)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def update_readme():
    data = get_weather()
    
    kst_now = datetime.utcnow() + timedelta(hours=9)
    formatted_time = kst_now.strftime("%Y년 %m월 %d일 %p %I:%M (KST)")

    if data:
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        weather_desc = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]
        humidity = data["main"]["humidity"]
        
        emoji = get_weather_emoji(weather_id)
        advice = get_weather_advice(weather_id)
        
        readme_content = f"""# 🏡 내 고향 서산 날씨 알리미

충남 서산(Seosan)의 실시간 날씨와 추천 행동을 전해드립니다.

| 위치 | 날씨 | 기온 | 체감 온도 | 습도 |
|:---:|:---:|:---:|:---:|:---:|
| **📍 서산 (Seosan)** | {emoji} {weather_desc} | **{temp:.1f}°C** | {feels_like:.1f}°C | 💧 {humidity}% |

### 💡 오늘의 추천
> **"{advice}"**

<div align="right">
  
  ⏳ 업데이트: {formatted_time}
</div>

---
*이 정보는 GitHub Actions 봇이 매 시간 정각에 서산을 바라보며 갱신합니다.*
"""
    else:
        readme_content = f"""# 🏡 내 고향 서산 날씨 알리미

⚠️ 날씨 정보를 가져오는 데 실패했습니다. 잠시 후 다시 시도합니다.

⏳ 확인 시간: {formatted_time}
"""

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)

if __name__ == "__main__":
    update_readme()
