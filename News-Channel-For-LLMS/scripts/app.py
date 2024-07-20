import streamlit as st
import psycopg2
import pandas as pd
from streamlit_modal import Modal
from contextlib import contextmanager
from utils.envs import *
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    try:
        yield conn
    finally:
        conn.close()


# Fetch categories from the database
def get_categories():
    try:
        with get_db_connection() as conn:
            query = "SELECT DISTINCT category FROM news_articles ORDER BY category;"
            df = pd.read_sql(query, conn)
            return df['category'].tolist()
    except Exception as e:
        st.error("Failed to fetch categories: " + str(e))
        return []


def get_data(category):
    try:
        with get_db_connection() as conn:
            query = """
                    SELECT id, title, author, source, description, published_at
                    FROM news_articles
                    WHERE category = %s AND is_latest = TRUE
                    ORDER BY published_at DESC
                    """
            
            df = pd.read_sql(query, conn, params=(category,))
            return df
    except Exception as e:
        st.error("Failed to fetch data: " + str(e))
        return pd.DataFrame()



# Fetch data based on category
def show_details(article):
    st.subheader(article.title)
    st.write('Author:', article.author)
    st.write('Source:', article.source)
    st.write('Last Published:', article.published_at.strftime("%B %d, %Y"))
    st.write('Description:', article.description)

def main():
    modal = Modal(key="article_modal", title="Article Details")
    st_autorefresh(interval=15 * 60 * 1000, key="dataframerefresh")
    tz = pytz.timezone("Europe/London")
    last_updated_time = datetime.now(tz).strftime("%H:%M:%S")
    st.write(f"Data refresh every 15 minutes, last updated at:{last_updated_time}")
    categories = get_categories()
    category = st.selectbox('Select a Category', categories)
    if category:
        data = get_data(category)
        if not data.empty:
            cols = st.columns(3)
            for index, row in data.iterrows():
                col = cols[index % 3]
                with col:
                    open_modal = st.button(row['title'], key=row['id'])
                    if open_modal:
                        with modal.container():
                            show_details(row)
        else:
            st.write('No articles found in this category.')

if __name__ == "__main__":
    main()
