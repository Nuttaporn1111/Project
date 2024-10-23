import streamlit as st
import pandas as pd

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
        "search_results": "ผลลัพธ์การค้นหา",
        "calculate_today_calories": "คำนวณแคลอรี่ในวันนี้",
        "calories_consumed": "แคลอรี่ที่บริโภคในวันนี้",
        "calories_vs_tdee": "การเปรียบเทียบแคลอรี่กับ TDEE"
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
        "search_results": "Search Results",
        "calculate_today_calories": "Calculate Today's Calories",
        "calories_consumed": "Calories Consumed Today",
        "calories_vs_tdee": "Comparison of Calories with TDEE"
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

# Function to calculate today's total calories
def calculate_today_calories():
    total_calories = 0
    for meals in st.session_state.meal_data.values():
        for meal in meals:
            total_calories += meal['calories']
    return total_calories

# Function for home page
def home_page():
    st.title(f"🏠 {t['welcome']}")
    st.subheader(f"👤 {t['user_data']}")

    # Display user data
    if st.session_state.user_data:
        st.write(f"**{t['weight']}:** {st.session_state.user_data['weight']} kg")
        st.write(f"**{t['height']}:** {st.session_state.user_data['height']} cm")
        st.write(f"**{t['age']}:** {st.session_state.user_data['age']} years")
        st.write(f"**{t['gender']}:** {st.session_state.user_data['gender']}")
        st.write(f"**{t['country']}:** {st.session_state.user_data['country']}")
        st.write(f"**{t['bmi']}:** {st.session_state.user_data.get('bmi', 'N/A'):.2f}")
        st.write(f"**{t['tdee']}:** {st.session_state.user_data.get('tdee', 'N/A'):.2f} kcal")

    # Meal selection
    meal_type = st.selectbox(f"🍽️ {t['choose_meal']}", [t['breakfast'], t['lunch'], t['dinner'], t['snack']])

    # Search meals feature
    search_term = st.text_input(f"🔍 {t['search']}")
    if search_term:
        search_results = search_meals(search_term)
        if not search_results.empty:
            st.subheader(f"📜 {t['search_results']}:")
            for index, row in search_results.iterrows():
                st.write(f"- {row['Menu']} : {row['Cal']} kcal")  # Adjust column names as necessary
                if st.button(f"➕ {t['add_meal']} {row['Menu']}", key=f"add_{index}"):
                    st.session_state.meal_data[meal_type].append({
                        "name": row['Menu'],
                        "calories": row['Cal']
                    })
                    st.success(f"{row['Menu']} {t['saved_meals']}!")

    # Display saved meals
    st.subheader(f"📊 {t['saved_meals']}:")
    if st.session_state.meal_data[meal_type]:
        for meal in st.session_state.meal_data[meal_type]:
            st.write(f"- {meal['name']} : {meal['calories']} kcal")
    else:
        st.write(t['no_meal_data'])

    # Calculate total calories for the day
    if st.button("🔍 คำนวณแคลอรี่ในวันนี้ / Calculate Today's Calories"):
        total_calories = sum(meal['calories'] for meal_list in st.session_state.meal_data.values() for meal in meal_list)
        st.write(f"**แคลอรี่ที่ได้รับในวันนี้:** {total_calories} kcal")

        # Compare with TDEE
        tdee = st.session_state.user_data.get("tdee", 0)
        if total_calories > tdee:
            st.warning(f"📉 คุณได้รับแคลอรี่มากกว่าความต้องการพลังงานทั้งหมด (TDEE) ที่ {tdee:.2f} kcal!")
        elif total_calories < tdee:
            st.success(f"📈 คุณได้รับแคลอรี่น้อยกว่าความต้องการพลังงานทั้งหมด (TDEE) ที่ {tdee:.2f} kcal!")
        else:
            st.info(f"📊 คุณได้รับแคลอรี่อยู่ที่ระดับความต้องการพลังงานทั้งหมด (TDEE) ที่ {tdee:.2f} kcal!")

# Render the current page
if st.session_state.current_page == "registration":
    registration_page()
else:
    home_page() 