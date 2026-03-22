# AirAware 

AirAware is a Streamlit-based dashboard that helps users monitor *Air Quality Index (AQI)* across Indian cities.  
It integrates live API data, historical datasets, and Twilio SMS alerts to notify users when air quality becomes hazardous.

---

## 🚀 Features
- 📊 Interactive AQI dashboard with charts and maps
- 🔔 SMS alerts via Twilio when AQI crosses thresholds
- 🌐 Live weather and AQI data from OpenWeather API
- 🗂 Historical data visualization using city_day.csv
- 📈 Forecasting with Facebook Prophet
- 🎨 Clean, user-friendly UI built with Streamlit

---

## 🛠️ Tech Stack
- *Python* (Streamlit, Pandas, Requests, Plotly, Prophet)
- *Twilio API* for SMS alerts
- *OpenWeather API* for live AQI/weather data
- *dotenv* for secure environment variable management

---

## ⚙️ Setup Instructions
- Create a virtual environment  
- Install dependencies with pip install -r requirements.txt  
- Add a .env file with your Twilio and OpenWeather keys  
- Run the app using streamlit run app.py  

---

## 📸 Screenshots

![WhatsApp Image 2026-03-22 at 6 19 04 PM](https://github.com/user-attachments/assets/61760ca4-2dbe-43af-a3b5-d9e6c7bc0a86)
----
![WhatsApp Image 2026-03-22 at 6 19 04 PM (2)](https://github.com/user-attachments/assets/60b654e4-be02-44e7-b217-8f4a2dc8afc8)
----
![WhatsApp Image 2026-03-22 at 6 19 04 PM (1)](https://github.com/user-attachments/assets/e9a22e54-2018-4661-bc67-d09364b8d360)
----
![WhatsApp Image 2026-03-22 at 6 19 05 PM](https://github.com/user-attachments/assets/22360445-f7f5-4bdd-a554-f52911f89616)
----
![WhatsApp Image 2026-03-22 at 6 23 17 PM](https://github.com/user-attachments/assets/ca7ecc1b-bcae-4940-9955-55cdf74618f9)
----
### 📱 SMS Alert Proof  
When AQI crosses hazardous levels, the system sends an SMS notification — for example: “AirAware Alert: AQI in Kolkata has reached 250 (Very Unhealthy). Stay Safe.”

![WhatsApp Image 2026-03-22 at 6 09 18 PM](https://github.com/user-attachments/assets/aec1628e-3053-4e38-88a2-b280e31a2879)


---

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License
MIT License
