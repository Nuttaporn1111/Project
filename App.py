import streamlit as st
import pandas as pd
from datetime import datetime
import re  # Import regular expressions for cleaning strings

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

        st.success(f"🎉 {t['submit']}! {t['back']}")  # Show success message
        st.session_state.current_page = "home"

def get_calories(meal_name):
    try:
        # Read data from Excel file
        df = pd.read_excel('Food.xlsx')  # Change to the path of your Excel file
        # Find calories by meal name
        result = df[df['Menu'] == meal_name]  # Change 'Menu' to the column name for meal names
        if not result.empty:
            # Clean the calorie value by removing unwanted characters
            calories_str = result.iloc[0]['Cal']  # Change 'Cal' to the column name for calories
            calories = float(re.sub(r'[^\d.]', '', calories_str))  # Remove non-numeric characters
            return calories
        else:
            return None
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return None


def search_meals(search_term):
    try:
        df = pd.read_excel('Food.xlsx')  # Change to the path of your Excel file
        # Filter meals that start with the search term
        filtered = df[df['Menu'].str.contains(search_term, na=False, case=False)]
        
        # Clean the calories in the filtered DataFrame
        if not filtered.empty:
            filtered['Cal'] = filtered['Cal'].apply(lambda x: float(re.sub(r'[^\d.]', '', x)))
        
        return filtered
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


# Home page
def home_page():
    st.title(f"🏠 {t['welcome']}")

    # Display user data if available
    if st.session_state.user_data:
        st.subheader(t['user_data'])
        st.write(f"💪 น้ำหนัก: {st.session_state.user_data['weight']} kg")
        st.write(f"📏 ส่วนสูง: {st.session_state.user_data['height']} cm")
        st.write(f"👶 อายุ: {st.session_state.user_data['age']} ปี")
        st.write(f"🚻 เพศ: {st.session_state.user_data['gender']}")
        st.write(f"🌍 ประเทศ: {st.session_state.user_data['country']}")
        st.write(f"🏋️‍♂️ BMI: {st.session_state.user_data['bmi']:.2f}")
        st.write(f"⚡ TDEE: {st.session_state.user_data['tdee']:.2f} kcal")

    # Meal addition section
    st.subheader(f"🍽️ {t['add_meal']}")
    
    # Choose meal type
    meal_type = st.selectbox(f"📋 {t['choose_meal']}", [t['breakfast'], t['lunch'], t['dinner'], t['snack']])
    meal_date = st.date_input(f"📅 {t['meal_date']}", datetime.today())
    
   # Search functionality
    st.subheader(f"🔍 {t['search']}")
    search_term = st.text_input(f"🔍 {t['search']}")

    meal_name = None
    calories = None

    if search_term:
        search_results = search_meals(search_term)  # Function to search meals by name
        st.subheader(t['search_results'])
        if search_results is not None and not search_results.empty:
            meal_name = st.selectbox(f"📝 {t['meal_name']}", options=search_results['Menu'].tolist())
            calories = get_calories(meal_name)
            if calories:
                st.write(f"**{t['meal_calories']}:** {calories} กิโลแคลอรี่" if language == "ไทย" else f"{t['meal_calories']}: {calories} kcal")
            else:
                st.write(f"{t['search_results']}: {t['no_meal_data']}")
        else:
            st.write("❌ ไม่พบข้อมูลที่ตรงกัน")

    # Upload meal image
    meal_image = st.file_uploader(f"📸 {t['meal_image']}", type=["jpg", "jpeg", "png"])


    # Add meal button
    if st.button(f"💾 {t['save_meal']}"):
        if meal_name:
            calories = get_calories(meal_name)
            if calories is not None:
                meal_data = {
                    "name": meal_name,
                    "calories": calories,
                    "date": meal_date
                }
                st.session_state.meal_data[meal_type].append(meal_data)
                st.success(f"✅ บันทึก {meal_name} ({calories} kcal) สำเร็จแล้ว!")
            else:
                st.error("❌ ไม่พบข้อมูลแคลอรี่สำหรับอาหารนี้")
        else:
            st.error("❌ กรุณากรอกชื่ออาหาร")

    # Button to view saved meals
    if st.button(f"📜 {t['saved_meals']}"):
        st.session_state.current_page = "meals"

def display_meals_page():
    # Other parts of your code remain the same...

    # Calculate total calories for the day
    if st.button("🔍 คำนวณแคลอรี่ในวันนี้ / Calculate Today's Calories"):
        total_calories = 0  # Initialize total_calories
        for meal_list in st.session_state.meal_data.values():
            for meal in meal_list:
                # Ensure the calories value is converted to float
                if meal['calories'] is not None:  # Check if calories is not None
                    try:
                        total_calories += float(meal['calories'])  # Convert to float before summing
                    except ValueError:
                        st.warning(f"Invalid calorie value for meal: {meal['calories']}")
        
        st.write(f"**แคลอรี่ที่ได้รับในวันนี้:** {total_calories:.2f} kcal")  # Display with 2 decimal places

        # Compare with TDEE
        tdee = st.session_state.user_data.get("tdee", 0)
        if total_calories > tdee:
            st.warning(f"📉 คุณได้รับแคลอรี่มากกว่าความต้องการพลังงานทั้งหมด (TDEE) ที่ {tdee:.2f} kcal!")
        elif total_calories < tdee:
            st.success(f"📈 คุณได้รับแคลอรี่น้อยกว่าความต้องการพลังงานทั้งหมด (TDEE) ที่ {tdee:.2f} kcal!")
        else:
            st.info(f"📊 คุณได้รับแคลอรี่อยู่ที่ระดับความต้องการพลังงานทั้งหมด (TDEE) ที่ {tdee:.2f} kcal!")



# Main application loop
if st.session_state.current_page == "registration":
    registration_page()
elif st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page == "meals":
    display_meals_page()

