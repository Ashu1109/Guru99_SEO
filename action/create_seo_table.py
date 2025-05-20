import json
from action.connect_to_db import connect_to_db
import streamlit as st

def create_backlink_table():
    """
    Creates a table to store backlink data if it doesn't exist already
    
    Returns:
        bool: True if table created or exists, False if failed
    """
    conn, cursor = connect_to_db()
    if not conn or not cursor:
        return False
    
    try:
        # Create table if it doesn't exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS backlinks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    backlink VARCHAR(500) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
        """
        cursor.execute(create_table_query)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False
    finally:
        if conn:
            conn.close()
            

def save_backlink(backlink):
    """
    Saves a backlink to the database
    
    Args:
        backlink (str): The backlink URL to save
        
    Returns:
        int or None: ID of the saved backlink if successful, None otherwise
    """
    conn, cursor = connect_to_db()
    if not conn or not cursor:
        return None
    
    try:
        # Insert backlink into table
        insert_query = "INSERT INTO backlinks (backlink) VALUES (%s)"
        cursor.execute(insert_query, (backlink,))
        conn.commit()
        
        # Get the ID of the inserted row
        last_id = cursor.lastrowid
        return last_id
    except Exception as e:
        print(f"Error saving backlink: {e}")
        return None
    finally:
        if conn:
            conn.close()




def create_seo_data_table():
    """
    Creates a table to store SEO data if it doesn't exist already
    
    Returns:
        bool: True if table created or exists, False if failed
    """
    conn, cursor = connect_to_db()
    if not conn or not cursor:
        return False
    
    try:
        # Create table if it doesn't exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS seo_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    backlink_id INT,
                    link VARCHAR(500),
                    title VARCHAR(500),
                    query_data TEXT,
                    clicks_of_words TEXT,
                    top15 TEXT,
                    GSC_top_KW TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (backlink_id) REFERENCES backlinks(id)
                );
        """
        cursor.execute(create_table_query)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False
    finally:
        if conn:
            conn.close()

def to_str(val):
        if isinstance(val, list):
            return ','.join(map(str, val))
        return str(val)

def save_seo_data(backlink_id,link, title, query_data, clicks_of_words, top15, gsc_top_kw):
    """
    Saves SEO data to the database
    
    Args:
        link (str): URL of the page
        title (str): Page title
        query_data (dict): Query data
        clicks_of_words (DataFrame): Clicks of words data
        top15 (DataFrame): Top 15 keywords
        gsc_top_kw (DataFrame): GSC top keywords
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    conn, cursor = connect_to_db()
    if not conn or not cursor:
        return False
    
    try:

        
        # Convert query_data to JSON string
        query_data_json = json.dumps(query_data) if query_data else '{}'
        
        # Insert data into table
        insert_query = """
        INSERT INTO seo_data (backlink_id, link, title, query_data, clicks_of_words, top15, gsc_top_kw)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        print(f"Saving data for backlink ID {backlink_id}: {link}, {title} with query data {query_data_json}, clicks of words {clicks_of_words}, top15 {top15}, GSC top KW {gsc_top_kw}")
        cursor.execute(insert_query, (backlink_id, link, title, to_str(query_data_json), to_str(clicks_of_words), to_str(top15), to_str(gsc_top_kw)))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False
    finally:
        if conn:
            conn.close()


def create_table_master_seo_link():
    """
    Creates a table to store master SEO link data if it doesn't exist already
    
    Returns:
        bool: True if table created or exists, False if failed
    """
    conn, cursor = connect_to_db()
    if not conn or not cursor:
        return False
    
    try:
        # Create table if it doesn't exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS master_seo_link (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    backlink_id INT,
                    link VARCHAR(500),
                    title VARCHAR(500),
                    query_data TEXT,
                    clicks_of_words TEXT,
                    top15 TEXT,
                    GSC_top_KW TEXT,
                    suggested_title_1 VARCHAR(500),
                    suggested_title_2 VARCHAR(500),
                    response TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (backlink_id) REFERENCES backlinks(id)
                );
        """
        cursor.execute(create_table_query)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False
    finally:
        if conn:
            conn.close()