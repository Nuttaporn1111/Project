import streamlit as st
from datetime import datetime

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
    st.title("ลงทะเบียน")
    
    # Input for weight, height, age, and gender
    weight = st.number_input("น้ำหนัก (กิโลกรัม)", min_value=0.0, format="%.2f")
    height = st.number_input("ส่วนสูง (เซนติเมตร)", min_value=0.0, format="%.2f")
    age = st.number_input("อายุ (ปี)", min_value=0, format="%d")
    gender = st.selectbox("เพศ", ["ชาย", "หญิง"])
    
    # Country selection
    country = st.selectbox("เลือกประเทศ", ["ประเทศไทย", "สหรัฐอเมริกา", "ญี่ปุ่น", "ประเทศอื่นๆ"])
    
    # Language selection
    language = st.selectbox("เลือกภาษา", ["ไทย", "อังกฤษ", "ญี่ปุ่น"])
    
    # Activity level selection
    activity_level = st.selectbox("ระดับกิจกรรม", [
        ("นั่งทำงาน", 1.2),
        ("ออกกำลังกายเบา", 1.375),
        ("ออกกำลังกายปานกลาง", 1.55),
        ("ออกกำลังกายหนัก", 1.725)
    ], format_func=lambda x: x[0])

    # Button to submit registration
    if st.button("บันทึกข้อมูล"):
        st.session_state.user_data = {
            "weight": weight,
            "height": height,
            "age": age,
            "gender": gender,
            "country": country,
            "language": language
        }

        # Calculate BMI
        if height > 0:
            bmi = weight / ((height / 100) ** 2)  # Convert height to meters
            st.session_state.user_data["bmi"] = bmi

            # Calculate BMR
            if gender == "ชาย":
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

            # Calculate TDEE
            tdee = bmr * activity_level[1]
            st.session_state.user_data["tdee"] = tdee

        st.success("ลงทะเบียนเรียบร้อยแล้ว! กดที่ปุ่มเพื่อไปที่หน้าแรก")
        st.session_state.current_page = "home"

# Function to display the home page
def home_page():
    st.title("หน้าแรก")
    st.write("ยินดีต้อนรับสู่แอปคำนวณแคลอรี่!")
    
    # Show user data
    st.write(f"น้ำหนัก: {st.session_state.user_data.get('weight', 0)} กิโลกรัม")
    st.write(f"ส่วนสูง: {st.session_state.user_data.get('height', 0)} เซนติเมตร")
    st.write(f"อายุ: {st.session_state.user_data.get('age', 0)} ปี")
    st.write(f"ประเทศ: {st.session_state.user_data.get('country', '')}")
    st.write(f"ภาษา: {st.session_state.user_data.get('language', '')}")
    
    # Display BMI and TDEE
    if "bmi" in st.session_state.user_data:
        st.write(f"ค่าดัชนีมวลกาย (BMI): {st.session_state.user_data['bmi']:.2f}")
    if "tdee" in st.session_state.user_data:
        st.write(f"ความต้องการพลังงานทั้งหมด (TDEE): {st.session_state.user_data['tdee']:.2f} กิโลแคลอรี่")

    # Create buttons for each meal type
    if st.button("มื้อเช้า"):
        st.session_state.current_page = "breakfast"
    if st.button("มื้อกลางวัน"):
        st.session_state.current_page = "lunch"
    if st.button("มื้อเย็น"):
        st.session_state.current_page = "dinner"
    if st.button("ของว่าง"):
        st.session_state.current_page = "snack"

# Function to display the add meal page
def add_meal_page(meal_type, meal_name):
    st.title(f"เพิ่มข้อมูล {meal_name}")
    
    # Date input
    date_input = st.date_input("เลือกวันที่", datetime.today())
    
    # Input for meal name
    meal_name_input = st.text_input("ชื่ออาหาร", value="", key=f"{meal_type}_name")

    # Use select_slider for calorie selection
    calories = st.select_slider(
        "เลือกแคลอรี่ (กิโลแคลอรี่)",
        options=list(range(0, 1001, 50)),  # สร้างลิสต์จาก 0 ถึง 1000 โดยเพิ่มทีละ 50
        value=0,
        key=f"{meal_type}_calories"
    )
    
    # Input for description
    description = st.text_area("คำบรรยายเกี่ยวกับอาหาร", value="", key=f"{meal_type}_description")

    # Image upload
    image = st.file_uploader("อัพโหลดภาพอาหาร", type=["jpg", "png", "jpeg"], key=f"{meal_type}_image")

    # Button to save meal data
    if st.button("บันทึกมื้ออาหาร"):
        meal_entry = {
            'name': meal_name_input,
            'calories': calories,
            'description': description,
            'image': image
        }
        
        # Ensure the meal type key exists before appending
        if meal_type in st.session_state.meal_data:
            st.session_state.meal_data[meal_type].append(meal_entry)
            st.success("บันทึกมื้ออาหารเรียบร้อยแล้ว!")
        else:
            st.error("ประเภทมื้ออาหารไม่ถูกต้อง!")

    # Display stored meal data for the selected meal type
    st.subheader(f"ข้อมูล {meal_name} ที่บันทึกไว้")
    if meal_type in st.session_state.meal_data and st.session_state.meal_data[meal_type]:
        for meal in st.session_state.meal_data[meal_type]:
            if meal['image'] is not None:
                st.image(meal['image'], use_column_width=True)  # Show image
            st.write(f"**ชื่ออาหาร:** {meal['name']}")
            st.write(f"**แคลอรี่:** {meal['calories']} กิโลแคลอรี่")
            st.write(f"**คำบรรยาย:** {meal['description']}")  # Show description
            st.write("---")  # Separator for each meal entry
    else:
        st.warning(f"ยังไม่มีข้อมูล {meal_name} ที่บันทึกไว้")
    
    if st.button("กลับไปหน้าแรก"):
        st.session_state.current_page = "home"

# Render the selected page
if st.session_state.current_page == "registration":
    registration_page()
elif st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page == "breakfast":
    add_meal_page("breakfast", "มื้อเช้า")
elif st.session_state.current_page == "lunch":
    add_meal_page("lunch", "มื้อกลางวัน")
elif st.session_state.current_page == "dinner":
    add_meal_page("dinner", "มื้อเย็น")
elif st.session_state.current_page == "snack":
    add_meal_page("snack", "ของว่าง")
