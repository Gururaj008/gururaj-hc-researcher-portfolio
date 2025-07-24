# app.py

import streamlit as st
from PIL import Image
import pandas as pd
from streamlit_option_menu import option_menu
import re

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Gururaj H C | PhD Candidate",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS FOR A CLASSY LOOK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Agdasima');
    @import url('https://fonts.googleapis.com/css2?family=Roboto');

    /* General font and theme adjustments */
    body {
        font-family: 'Roboto', sans-serif;
    }
    .stApp {
        background-color: #111111;
    }

    [data-testid="stSidebar"] h1 {
        font-size: 1.8rem;
    }
    [data-testid="stSidebar"] p {
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    /* Main content styling */
    h1, h2 {
        color: #FAFAFA;
    }

    .custom-subheader {
        font-family: 'Agdasima', sans-serif !important;
        font-size: 32px !important;
        color: cyan !important;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .keyword-title {
        font-family: 'Agdasima', sans-serif !important;
        font-size: 1.3em !important;
        color: cyan !important;
        font-weight: bold;
    }

    /* Classy image styling */
    .profile-image img {
        border-radius: 50%;
        border: 3px solid #FF4B4B;
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.5);
        transition: transform 0.3s ease-in-out;
    }
    .profile-image img:hover {
        transform: scale(1.05);
    }

    .justified-text, .publication-abstract {
        text-align: justify;
    }

    .degree-title, .job-title {
        font-size: 1.25rem;
        font-weight: bold;
        color: #FAFAFA;
    }
    .institution-name, .organization-name {
        font-style: italic;
        color: #AAAAAA;
    }
    .year-text, .duration-text {
        text-align: right;
        color: #AAAAAA;
    }

    .st-emotion-cache-p5msec {
        font-size: 1.1rem;
    }
    .st-emotion-cache-p5msec:hover {
        color: #FF4B4B;
    }
    .github-link {
        font-weight: bold;
        color: #FF4B4B;
    }

    /* Contact page styling */
    .contact-icon {
        display: inline-block;
        width: 30px;
        vertical-align: middle;
        margin-right: 10px;
    }
    .contact-link a {
        font-size: 1.1rem;
        color: #CCCCCC;
        text-decoration: none;
        vertical-align: middle;
    }
    .contact-link a:hover {
        color: #FF4B4B;
        text-decoration: underline;
    }

</style>
""", unsafe_allow_html=True)


# --- HELPER FUNCTIONS ---
def render_custom_subheader(text):
    st.markdown(f'<p class="custom-subheader">{text}</p>', unsafe_allow_html=True)


# --- PAGE DEFINITIONS ---

def render_home_page():
    st.title("My True North")
    st.markdown("---")
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        st.markdown('<div class="profile-image">', unsafe_allow_html=True)
        try:
            image = Image.open("Gururaj_H_C_PhD_candidate_photo.png")
            st.image(image, width=250)
        except FileNotFoundError:
            st.error("Profile image 'Gururaj_H_C_PhD_candidate_photo.png' not found.")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        try:
            df = pd.read_excel("My_True_North.xlsx", sheet_name="My True North")
            if 'Sub-title' in df.columns and 'Content' in df.columns:
                for index, row in df.iterrows():
                    render_custom_subheader(row['Sub-title'])
                    st.markdown(f"<div class='justified-text'>{row['Content']}</div>", unsafe_allow_html=True)
                    st.write("")
            else:
                st.error("Excel file must contain 'Sub-title' and 'Content' columns.")
        except FileNotFoundError:
            st.error("File 'My_True_North.xlsx' not found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")


def render_education_page():
    render_custom_subheader("Education")
    try:
        df = pd.read_excel("Education.xlsx", sheet_name="Education")
        required_cols = ['Degree', 'Institution', 'Year']
        if not all(col in df.columns for col in required_cols):
            st.error(f"Education.xlsx must contain the columns: {', '.join(required_cols)}")
            return
        for index, row in df.iterrows():
            st.write("")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"<p class='degree-title'>{row['Degree']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='institution-name'>{row['Institution']}</p>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<p class='year-text'>{row['Year']}</p>", unsafe_allow_html=True)
            if index < len(df) - 1:
                st.markdown("---")
    except FileNotFoundError:
        st.error("File 'Education.xlsx' not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def render_data_science_projects_page():
    render_custom_subheader("Data Science Projects")
    try:
        xls = pd.ExcelFile("Data_Science_projects.xlsx")
        sheet_names = xls.sheet_names
        tabs = st.tabs(sheet_names)
        keywords = ['Task', 'Dataset', 'Method', 'Key Results', 'Impact', 'Tech Stack']
        for i, sheet_name in enumerate(sheet_names):
            with tabs[i]:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                required_cols = ['Project title', 'Description', 'GitHub repo link']
                if not all(col in df.columns for col in required_cols):
                    st.warning(f"Sheet '{sheet_name}' is missing required columns. Skipping.")
                    continue
                for index, row in df.iterrows():
                    clean_title = row['Project title'].strip().strip('*')
                    with st.expander(f"**{clean_title}**"):
                        description = row['Description']
                        found_keywords = []
                        for kw in keywords:
                            match = re.search(r'\b' + re.escape(kw) + r'\s*:', description, re.IGNORECASE)
                            if match:
                                found_keywords.append({'keyword': kw, 'start': match.start(), 'end': match.end()})
                        found_keywords.sort(key=lambda x: x['start'])
                        if not found_keywords:
                            st.markdown(description)
                        else:
                            first_kw_start = found_keywords[0]['start']
                            if first_kw_start > 0:
                                st.markdown(description[:first_kw_start].strip())
                            for i in range(len(found_keywords)):
                                current_kw_info = found_keywords[i]
                                content_start = current_kw_info['end']
                                if i + 1 < len(found_keywords):
                                    content_end = found_keywords[i + 1]['start']
                                else:
                                    content_end = len(description)
                                content = description[content_start:content_end].strip()
                                if content:
                                    st.markdown(
                                        f"- <span class='keyword-title'>{current_kw_info['keyword']}:</span> {content}",
                                        unsafe_allow_html=True)
                        st.write("")
                        st.markdown(
                            f"🔗 <a href='{row['GitHub repo link']}' class='github-link' target='_blank'>View on GitHub</a>",
                            unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("For a more extensive archive of my earlier projects, please visit my [secondary portfolio](https://gururaj-hc-personal-webpage.streamlit.app/).")
        
    except FileNotFoundError:
        st.error("File 'Data_Science_projects.xlsx' not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def render_pre_prints_page():
    render_custom_subheader("Pre-prints")
    try:
        df = pd.read_excel("Pre_prints.xlsx", sheet_name="Pre-prints")
        required_cols = ['Title', 'Abstract', 'Available at']
        if not all(col in df.columns for col in required_cols):
            st.error(f"pre_prints.xlsx must contain the columns: {', '.join(required_cols)}")
            return
        for index, row in df.iterrows():
            with st.expander(f"**{row['Title']}**"):
                st.markdown(f"<div class='publication-abstract'>{row['Abstract']}</div>", unsafe_allow_html=True)
                st.write("")
                url = row['Available at']
                try:
                    domain_name = url.split('/')[2].replace('www.', '').split('.')[0].capitalize()
                    button_label = f"View on {domain_name}"
                except:
                    button_label = "View Pre-print"
                st.link_button(button_label, url, use_container_width=True)
            st.markdown("---")
    except FileNotFoundError:
        st.error("File 'pre_prints.xlsx' not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def render_publications_page():
    render_custom_subheader("Publications")
    try:
        df = pd.read_excel("Publications.xlsx", sheet_name="Publications")
        required_cols = ['Title', 'Abstract', 'Available at']
        if not all(col in df.columns for col in required_cols):
            st.error(f"Publications.xlsx must contain the columns: {', '.join(required_cols)}")
            return
        for index, row in df.iterrows():
            with st.expander(f"**{row['Title']}**"):
                st.markdown(f"<div class='publication-abstract'>{row['Abstract']}</div>", unsafe_allow_html=True)
                st.write("")
                url = row['Available at']
                if index < 3:
                    button_label = "View on Springer"
                else:
                    try:
                        domain_name = url.split('/')[2].replace('www.', '').split('.')[0].capitalize()
                        button_label = f"View on {domain_name}"
                    except:
                        button_label = "View Publication"
                st.link_button(button_label, url, use_container_width=True)
            st.markdown("---")
    except FileNotFoundError:
        st.error("File 'Publications.xlsx' not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def render_work_experience_page():
    render_custom_subheader("Work Experience")
    try:
        df = pd.read_excel("Work_Experience.xlsx", sheet_name="Work_Experience")
        required_cols = ['Designation', 'Organization', 'Duration', 'Job desscription']
        if not all(col in df.columns for col in required_cols):
            st.error(f"Work_Experience.xlsx must contain the columns: {', '.join(required_cols)}")
            st.write("Columns found in the Excel file:", df.columns.tolist())
            return
        for index, row in df.iterrows():
            st.write("")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"<p class='job-title'>{row['Designation']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='organization-name'>{row['Organization']}</p>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<p class='duration-text'>{row['Duration']}</p>", unsafe_allow_html=True)
            st.write("")
            job_points = row['Job desscription'].split('\n')
            for point in job_points:
                if point.strip():
                    st.markdown(f"- {point.strip()}")
            if index < len(df) - 1:
                st.markdown("---")
    except FileNotFoundError:
        st.error("File 'Work_Experience.xlsx' not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def render_work_projects_page():
    render_custom_subheader("Work Projects")
    try:
        df = pd.read_excel("Work_projects.xlsx", sheet_name="Work_projects")
        required_cols = ['Project title', 'Project Description', 'Goal', 'Solution', 'Results', 'Learning']
        if not all(col in df.columns for col in required_cols):
            st.error(f"Work_projects.xlsx must contain the columns: {', '.join(required_cols)}")
            return
        for index, row in df.iterrows():
            with st.expander(f"**{row['Project title']}**"):
                st.markdown(row['Project Description'])
                st.write("")
                sections = ['Goal', 'Solution', 'Results', 'Learning']
                for section in sections:
                    if pd.notna(row[section]) and str(row[section]).strip():
                        st.markdown(f"<span class='keyword-title'>{section}:</span>", unsafe_allow_html=True)
                        points = str(row[section]).split('\n')
                        for point in points:
                            if point.strip():
                                st.markdown(f"- {point.strip()}")
                        st.write("")
            st.markdown("---")
    except FileNotFoundError:
        st.error("File 'Work_projects.xlsx' not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def render_awards_and_achievements_page():
    render_custom_subheader("Awards and Achievements")
    try:
        df = pd.read_excel("Awards_and_Achievements.xlsx", sheet_name="Awards_and_Achievements")
        required_cols = ['Timeline', 'Description']
        if not all(col in df.columns for col in required_cols):
            st.error(f"Awards_and_Achievements.xlsx must contain the columns: {', '.join(required_cols)}")
            return
        for index, row in df.iterrows():
            st.write("")
            st.markdown(f"<p class='job-title'>{row['Timeline']}</p>", unsafe_allow_html=True)
            description_points = str(row['Description']).split('\n')
            for point in description_points:
                point_stripped = point.strip()
                if point_stripped:
                    if point_stripped.startswith("While working as a Consultant"):
                        st.markdown(point_stripped)
                    elif point_stripped.startswith(('•', '-', '*')):
                        st.markdown(point_stripped)
                    else:
                        st.markdown(f"- {point_stripped}")
            if index < len(df) - 1:
                st.markdown("---")
    except FileNotFoundError:
        st.error("File 'Awards_and_Achievements.xlsx' not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def render_contact_details_page():
    render_custom_subheader("Get in Touch")
    st.markdown(
        "I'm actively seeking PhD opportunities and welcome connections from researchers and academic groups. Please feel free to reach out.")
    st.write("")
    try:
        df = pd.read_excel("Contact_details.xlsx", sheet_name="Contact_details")
        required_cols = ['Platform', 'Link']
        if not all(col in df.columns for col in required_cols):
            st.error(f"Contact_details.xlsx must contain the columns: {', '.join(required_cols)}")
            return
        icons = {
            "email id": """<svg class="contact-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>""",
            "linkedin profile": """<svg class="contact-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>""",
            "github link": """<svg class="contact-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>"""
        }
        for index, row in df.iterrows():
            platform_key = row['Platform'].lower().strip()
            link = row['Link']
            icon_html = icons.get(platform_key, "•")
            if platform_key == "email id":
                display_link = f"<a href='mailto:{link}' target='_blank'>{link}</a>"
            else:
                display_link = f"<a href='{link}' target='_blank'>{row['Platform']}</a>"
            st.markdown(f"{icon_html} <span class='contact-link'>{display_link}</span>", unsafe_allow_html=True)
            st.write("")
    except FileNotFoundError:
        st.error("File 'Contact_details.xlsx' not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


# --- SIDEBAR AND NAVIGATION ---
with st.sidebar:
    try:
        sidebar_image = Image.open("Gururaj_H_C_PhD_candidate_photo.png")
        st.image(sidebar_image, width=120)
    except FileNotFoundError:
        pass
    st.title("Gururaj H C")
    st.markdown("Independent researcher & Data Scientist")
    st.markdown("---")

    page_options = ["My True North", "Education", "Data Science Projects", "Pre-prints", "Publications",
                    "Work Experience", "Work Projects", "Awards and Achievements", "Contact Details"]
    page_icons = ["house-heart-fill", "mortarboard-fill", "robot", "file-earmark-arrow-up-fill", "journal-text",
                  "briefcase-fill", "kanban-fill", "trophy-fill", "person-lines-fill"]

    selected_page = option_menu(
        menu_title=None,
        options=page_options,
        icons=page_icons,
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#1E1E1E"},
            "icon": {"color": "white", "font-size": "16px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#333333"},
            "nav-link-selected": {"background-color": "#FF4B4B"},
        }
    )

# --- MAIN PAGE RENDERING LOGIC ---
if selected_page == "My True North":
    render_home_page()
elif selected_page == "Education":
    render_education_page()
elif selected_page == "Data Science Projects":
    render_data_science_projects_page()
elif selected_page == "Pre-prints":
    render_pre_prints_page()
elif selected_page == "Publications":
    render_publications_page()
elif selected_page == "Work Experience":
    render_work_experience_page()
elif selected_page == "Work Projects":
    render_work_projects_page()
elif selected_page == "Awards and Achievements":
    render_awards_and_achievements_page()
elif selected_page == "Contact Details":
    render_contact_details_page()
