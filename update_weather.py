import requests
import os
from datetime import datetime

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Seoul"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

README_PATH = "README.md"

def get_weather():
    if not API_KEY:
        return "OPENWEATHER_API_KEY가 설정되지 않았습니다(Secrets 확인)."

    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            return f"서울: {weather}, {temp}°C, 습도 {humidity}%"
        return f"날씨 조회 실패: status={response.status_code}"
    except Exception as e:
        return f"예외 발생: {e}"

def update_readme():
    weather_info = get_weather()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    readme_content = f"""# Weather API Status

이 리포지토리는 OpenWeather API를 사용하여 서울의 날씨 정보를 자동으로 업데이트합니다.

## 현재 서울 날씨
> {weather_info}

⏳ 업데이트 시간: {now}

---
자동 업데이트 봇에 의해 관리됩니다.
"""
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)

if __name__ == "__main__":
    update_readme()
