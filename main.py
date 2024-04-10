import streamlit as st
from bs4 import BeautifulSoup
import requests

class Authentication:
    @staticmethod
    def init_session():
        if 'isLogged' not in st.session_state:
            st.session_state.isLogged = False

    @staticmethod
    def login(username, password):
        payload = {
            'LoginForm[username]': username,
            'LoginForm[password]': password
        }
        return payload

Authentication.init_session()
container = st.container(border=True)
container.subheader("Login with Etlab")
with container.form("Login", border=False):
    username = st.text_input("Etlab Username")
    password = st.text_input("Etlab Password", type='password')
    submit = st.form_submit_button("Login")
    if submit:
        payload = Authentication.login(username, password)
        userSession = requests.session()
        login_response = userSession.post(url='https://sctce.etlab.in/user/login', data=payload)
        if login_response.status_code == 200:
            st.write("Login successful!")
            st.session_state.isLogged = True
            profile_response = userSession.get('https://sctce.etlab.in/student/profile')
            subject_response = userSession.get('https://sctce.etlab.in/ktuacademics/student/viewattendancesubject/88')
            
            if profile_response.status_code == 200 and subject_response.status_code == 200:
                html_profile = BeautifulSoup(profile_response.content, 'html.parser')
                html_subject = BeautifulSoup(subject_response.content, 'html.parser')
                html_attendance = BeautifulSoup(subject_response.content, 'html.parser')

                try:
                    name_tag = html_profile.find('th', string='Name')
                    gender_tag = html_profile.find('th', string='Gender')
                    university_id = html_profile.find('th', string='University Reg No')
                    subject_by_subs = html_subject.find_all('th', class_='span2')
                    attendance_by_subs = html_attendance.find_all('td', class_='span2')

                    userData = {
                        'isLoggedIn': True,
                        'Username': username,
                        'Password': password,
                        'Name': name_tag.find_next('td').text.strip(),
                        'Gender': gender_tag.find_next('td').text.strip(),
                        'Department_ID': university_id.find_next('td').text.strip()
                    }
                    subject_data = [subject.text.strip() for subject in subject_by_subs]
                    attendance_data = [attendance.text.strip() for attendance in attendance_by_subs]
                    data = list(zip(subject_data, attendance_data))
                    st.write(userData)
                    for subject, attendance in data:
                        st.write(f"Subject: {subject} ==> Attendance: {attendance}")

                except AttributeError:
                    st.error("Error parsing profile information.")
            else:
                st.error("Error fetching profile or subject data.")
        else:
            st.error("Login failed. Please check your credentials.")
    else:
        st.error("Enter the Details!")
        st.text("prnv pwoli alle huhu")
