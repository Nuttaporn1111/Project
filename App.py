import streamlit as st
import pandas as pd
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
        "back": "กลับไปหน้าแรก",
        "search": "ค้นหาอาหาร",
        "search_results": "ผลลัพธ์การค้นหา"
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
        "back": "Back to Home",
        "search": "Search Food",
        "search_results": "Search Results"
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
        t['breakfast']: [],
        t['lunch']: [],
        t['dinner']: [],
        t['snack']: []
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
    if st.button(f"📝 {t['submit']}", key='submit_registration'):
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

# Function to get calories from Excel
def get_calories(meal_name):
    try:
        # Read data from Excel file
        df = pd.read_excel('Food.xlsx')  # Change to the path of your Excel file
        # Find calories by meal name
        result = df[df['Menu'] == meal_name]  # Change 'Menu' to the column name for meal names
        if not result.empty:
            return result.iloc[0]['Cal']  # Change 'Cal' to the column name for calories
        else:
            return None
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return None

# Function to search meals by name
def search_meals(search_term):
    try:
        df = pd.read_excel('Food.xlsx')  # Change to the path of your Excel file
        # Filter meals that start with the search term
        filtered = df[df['Menu'].str.contains(search_term, na=False, case=False)]
        return filtered
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Function for home page
def home_page():
    st.title(f"🏠 {t['welcome']}")
    st.subheader(f"👤 {t['user_data']}")
    
    # Display user data
    if st.session_state.user_data:
        st.write(f"**{t['weight']}:** {st.session_state.user_data.get('weight', 0):.2f} กิโลกรัม" if language == "ไทย" else f"{t['weight']}: {st.session_state.user_data.get('weight', 0):.2f} kg")
        st.write(f"**{t['height']}:** {st.session_state.user_data.get('height', 0)} เซนติเมตร" if language == "ไทย" else f"{t['height']}: {st.session_state.user_data.get('height', 0)} cm")
        st.write(f"**{t['age']}:** {st.session_state.user_data.get('age', 0)} ปี" if language == "ไทย" else f"{t['age']}: {st.session_state.user_data.get('age', 0)} years")
        st.write(f"**{t['gender']}:** {st.session_state.user_data.get('gender', '')}" if language == "ไทย" else f"{t['gender']}: {st.session_state.user_data.get('gender', '')}")
        st.write(f"**{t['bmi']}:** {st.session_state.user_data.get('bmi', 0):.2f}")
        st.write(f"**{t['tdee']}:** {st.session_state.user_data.get('tdee', 0):.2f} kcal")

    # Meal logging section
    st.subheader(f"🍽️ {t['choose_meal']}")
    meal_type = st.selectbox(f"📋 {t['add_meal']}", [t['breakfast'], t['lunch'], t['dinner'], t['snack']])
    
    # Date, name, calories, and image upload for meals
    meal_date = st.date_input(f"📅 {t['meal_date']}", datetime.today())
    
    # Search functionality for meal name
    st.subheader(f"🔍 {t['search']}")
    search_term = st.text_input(f"🔍 {t['search']}")
    
    meal_name = None
    calories = None

    if search_term:
        search_results = search_meals(search_term)  # Function to search meals by name
        st.subheader(t['search_results'])
        if search_results is not None and not search_results.empty:
            meal_name = st.selectbox(f"📝 {t['meal_name']}", options=search_results['Menu'].tolist(), key='search_meal_name')
            calories = get_calories(meal_name)
            if calories:
                st.write(f"**{t['meal_calories']}:** {calories} กิโลแคลอรี่" if language == "ไทย" else f"{t['meal_calories']}: {calories} kcal")
            else:
                st.write(f"{t['search_results']}: {t['no_meal_data']}")
        else:
            st.write("❌ ไม่พบข้อมูลที่ตรงกัน")  

    meal_image = st.file_uploader(f"🖼️ {t['meal_image']}", type=["jpg", "jpeg", "png"])
    
    if meal_image:
        st.image(meal_image)

    if st.button(f"💾 {t['save_meal']}", key='save_meal'):
        if meal_name and calories:
            meal_data = {
                "date": meal_date,
                "name": meal_name,
                "calories": calories,
                "image": meal_image.name if meal_image else None
            }
            st.session_state.meal_data[meal_type].append(meal_data)
            st.success(f"✅ {t['save_meal']}! {t['back']}")
        else:
            st.error("กรุณากรอกชื่ออาหารและตรวจสอบแคลอรี่!")  # Error message if not filled

    # Display saved meals
    st.subheader(f"📋 {t['saved_meals']}")
    for meal_type, meals in st.session_state.meal_data.items():
        st.write(f"**{meal_type}:**")
        if meals:
            for idx, meal in enumerate(meals):
                st.write(f"{idx + 1}. {meal['date']} - {meal['name']} - {meal['calories']} kcal")
                if meal['image']:
                    st.image(meal['image'])
        else:
            st.write(t['no_meal_data'])

# Navigation logic
if st.session_state.current_page == "registration":
    registration_page()
else:
    home_page()
