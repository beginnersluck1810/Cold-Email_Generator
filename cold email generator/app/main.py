import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from sqlalchemy.dialects.mysql.mariadb import loader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm,portfolio,clean_text):
    st.title("Cold email Generator 📧")
    url_input=st.text_input("Enter a URL:", value="https://careers.nike.com/cdn-security-engineer-waf/job/R-48004")
    submit_button=st.button("SUBMIT")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                # Join the list of skills into a single string
                skills_string = ", ".join(skills)  # You can adjust the separator as needed (e.g., comma, space)
                links = portfolio.query_links(skills_string)  # Pass the joined string to the query_links function
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"AN ERROR OCCURRED: {e}")


if __name__ =="__main__":
    chain=Chain()
    portfolio=Portfolio()
    st.set_page_config(layout="wide", page_title="COLD EMAIL GENERATOR 📧 ", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
