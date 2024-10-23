import streamlit as st
from datetime import datetime

# Set up language translations
translations = {
    "ไทย": {
        "title": "NAB Food Calculator App",
        "registration": "ลงทะเบียน",
        "weight": "น้ำหนัก (กิโลกรัม)",
        "height": "ส่วนสูง (เซนติเมตร)",
        "age": "อายุ (ปี)",
        "gender": "เพศ",
        "country": "เลือกประเทศ",
        "language": "เลือกภาษา",
        "activity_level": "ระดับกิจกรรม",
        "submit": "บันทึกข้อมูล",
        "welcome": "ยินดีต้อนรับสู่แอปคำนวณแคลอรี่!",
        "user_data": "ข้อมูลผู้ใช้ของคุณ",
        "bmi": "ค่าดัชนีมวลกาย (BMI)",
        "tdee": "ความต้องการพลังงานทั้งหมด (TDEE)",
        "choose_meal": "เลือกมื้ออาหาร",
        "breakfast": "มื้อเช้า",
        "lunch": "มื้อกลางวัน",
        "dinner": "มื้อเย็น",
        "snack": "ของว่าง",
        "add_meal": "เพิ่มข้อมูล",
        "meal_date": "เลือกวันที่",
        "meal_name": "ชื่ออาหาร",
        "meal_calories": "เลือกแคลอรี่ (กิโลแคลอรี่)",
        "meal_image": "อัพโหลดภาพอาหาร",
        "save_meal": "บันทึกมื้ออาหาร",
        "saved_meals": "ข้อมูลที่บันทึกไว้",
        "no_meal_data": "ยังไม่มีข้อมูลที่บันทึกไว้",
        "back": "กลับไปหน้าแรก"
    },
    "English": {
        "title": "NAB Food Calculator App",
        "registration": "Registration",
        "weight": "Weight (kg)",
        "height": "Height (cm)",
        "age": "Age (years)",
        "gender": "Gender",
        "country": "Select Country",
        "language": "Select Language",
        "activity_level": "Activity Level",
        "submit": "Submit",
        "welcome": "Welcome to the Calorie Calculator App!",
        "user_data": "Your User Data",
        "bmi": "Body Mass Index (BMI)",
        "tdee": "Total Daily Energy Expenditure (TDEE)",
        "choose_meal": "Choose a Meal",
        "breakfast": "Breakfast",
        "lunch": "Lunch",
        "dinner": "Dinner",
        "snack": "Snack",
        "add_meal": "Add Meal",
        "meal_date": "Select Date",
        "meal_name": "Meal Name",
        "meal_calories": "Choose Calories (kcal)",
        "meal_image": "Upload Meal Image",
        "save_meal": "Save Meal",
        "saved_meals": "Saved Meal Data",
        "no_meal_data": "No saved meal data",
        "back": "Back to Home"
    }
}

# Select language
language = st.selectbox("🌐 เลือกภาษา / Select Language", ["ไทย", "English"])

# Use the selected language for translations
t = translations[language]

# Sidebar configuration with circular logo
st.sidebar.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="https://i.imgur.com/d7m4oYk_d.webp?maxwidth=760&fidelity=grand" style="width: 60px; height: 60px; border-radius: 50%; margin-right: 10px;">
        <h2 style="margin: 0;">{t['title']}</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Dictionary to store meal data
if 'meal_data' not in st.session_state:
    st.session_state.meal_data = {
        "breakfast": [],
        "lunch": [],
        "dinner": [],
        "snack": []
    }

# User registration data
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Main application logic
if 'current_page' not in st.session_state:
    st.session_state.current_page = "registration"

# Function for user registration
def registration_page():
    st.title(f"📋 {t['registration']}")
    
    # Use Columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input(f"🏋️‍♂️ {t['weight']}", min_value=0.0, format="%.2f")
        height = st.number_input(f"📏 {t['height']}", min_value=0.0, format="%.2f")
        age = st.number_input(f"👶 {t['age']}", min_value=0, format="%d")
    
    with col2:
        gender = st.selectbox(f"🚻 {t['gender']}", ["ชาย" if language == "ไทย" else "Male", "หญิง" if language == "ไทย" else "Female"])
        country = st.selectbox(f"🌍 {t['country']}", ["ประเทศไทย" if language == "ไทย" else "Thailand", "สหรัฐอเมริกา" if language == "ไทย" else "USA", "ญี่ปุ่น" if language == "ไทย" else "Japan", "ประเทศอื่นๆ" if language == "ไทย" else "Other"])
    
    # Activity level selection with icons
    activity_level = st.selectbox(f"🏃‍♀️ {t['activity_level']}", [
        ("นั่งทำงาน 💻" if language == "ไทย" else "Sedentary 💻", 1.2),
        ("ออกกำลังกายเบา 🚶‍♂️" if language == "ไทย" else "Light Exercise 🚶‍♂️", 1.375),
        ("ออกกำลังกายปานกลาง 🏋️‍♀️" if language == "ไทย" else "Moderate Exercise 🏋️‍♀️", 1.55),
        ("ออกกำลังกายหนัก 🏃‍♂️" if language == "ไทย" else "Heavy Exercise 🏃‍♂️", 1.725)
    ], format_func=lambda x: x[0])

    # Submit registration with a button
    if st.button(f"📝 {t['submit']}", help=t["submit"]):
        st.session_state.user_data = {
            "weight": weight,
            "height": height,
            "age": age,
            "gender": gender,
            "country": country
        }

        # Calculate BMI
        if height > 0:
            bmi = weight / ((height / 100) ** 2)  # Convert height to meters
            st.session_state.user_data["bmi"] = bmi

            # Calculate BMR
            if gender == ("ชาย" if language == "ไทย" else "Male"):
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

            # Calculate TDEE
            tdee = bmr * activity_level[1]
            st.session_state.user_data["tdee"] = tdee

        st.success(f"🎉 {t['submit']}! {t['back']}")
        st.session_state.current_page = "home"

# Function to display the home page
def home_page():
    st.title(f"🏠 {t['title']}")
    st.write(f"{t['welcome']} 😃")
    
    # Display user data with an expander
    with st.expander(f"📊 {t['user_data']}"):
        st.write(f"**{t['weight']}:** {st.session_state.user_data.get('weight', 0)} กิโลกรัม" if language == "ไทย" else "kg")
        st.write(f"**{t['height']}:** {st.session_state.user_data.get('height', 0)} เซนติเมตร" if language == "ไทย" else "cm")
        st.write(f"**{t['age']}:** {st.session_state.user_data.get('age', 0)} ปี" if language == "ไทย" else "years")
        st.write(f"**{t['country']}:** {st.session_state.user_data.get('country', '')}")
    
        # Display BMI and TDEE
        if "bmi" in st.session_state.user_data:
            st.metric(f"📏 {t['bmi']}", f"{st.session_state.user_data['bmi']:.2f}")
        if "tdee" in st.session_state.user_data:
            st.metric(f"🔥 {t['tdee']}", f"{st.session_state.user_data['tdee']:.2f} กิโลแคลอรี่")

    # Create buttons with icons
    st.markdown(f"## 🍽️ {t['choose_meal']}")
    if st.button(f"🍳 {t['breakfast']}"):
        st.session_state.current_page = "breakfast"
    if st.button(f"🍲 {t['lunch']}"):
        st.session_state.current_page = "lunch"
    if st.button(f"🍛 {t['dinner']}"):
        st.session_state.current_page = "dinner"
    if st.button(f"🍪 {t['snack']}"):
        st.session_state.current_page = "snack"

# Function to display the add meal page
def add_meal_page(meal_type):
    st.title(f"🍽️ {t['add_meal']}")
    meal_date = st.date_input(f"📅 {t['meal_date']}", datetime.now())
    meal_name = st.text_input(f"🍴 {t['meal_name']}")
    meal_calories = st.slider(f"🔢 {t['meal_calories']}", 0, 2000, 100)
    meal_image = st.file_uploader(f"🖼️ {t['meal_image']}")

    if st.button(f"💾 {t['save_meal']}"):
        # Save meal data
        st.session_state.meal_data[meal_type].append({
            "date": meal_date,
            "name": meal_name,
            "calories": meal_calories,
            "description": meal_description,
            "image": meal_image
        })
        st.success(f"✅ {t['save_meal']}")
        st.session_state.current_page = "home"

# Routing pages based on current page state
if st.session_state.current_page == "registration":
    registration_page()
elif st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page in ["breakfast", "lunch", "dinner", "snack"]:
    add_meal_page(st.session_state.current_page)
