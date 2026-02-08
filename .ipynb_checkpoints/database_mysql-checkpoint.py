import mysql.connector

def get_connection():
    return mysql.connector.connect(
    host="localhost",
    user="arcane_user",
    password="arcane1234",
    database="arcane_db"
   )

def insert_project(sector, name, description, dataset_path=None): 
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO projects (sector, name, description, dataset_path) VALUES (%s, %s, %s, %s)",
        (sector, name, description, dataset_path)
    )
    conn.commit()
    project_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return project_id

def get_projects(limit=50):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, sector, name, description, created_at FROM projects ORDER BY id DESC LIMIT %s",
        (limit,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows