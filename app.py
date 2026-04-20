import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date

# 1. Database Initialization
@st.cache_resource
def init_db():
    conn = sqlite3.connect('tasks_pro.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      name TEXT NOT NULL, 
                      category TEXT NOT NULL,
                      due_date DATE,
                      status TEXT DEFAULT 'Pending')''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category)')
    conn.commit()
    return conn

db_conn = init_db()

# UI Setup
st.set_page_config(page_title="TaskFlow Pro", page_icon="✅", layout="wide")
st.title("✅ TaskFlow Pro")
st.caption("Powered by SQLite B-Tree Indexing Technology")

# 2. Sidebar: Real-world Task Input
with st.sidebar:
    st.header("➕ New Task")
    with st.form("task_form", clear_on_submit=True):
        t_name = st.text_input("Task Description", placeholder="e.g., Study for Midterm")
        t_cat = st.selectbox("Category", ["School", "Work", "Housekeeping"])
        t_date = st.date_input("Due Date", value=date.today())
        submitted = st.form_submit_button("Add Task")
        
        if submitted and t_name:
            db_conn.execute("INSERT INTO tasks (name, category, due_date) VALUES (?, ?, ?)", 
                           (t_name, t_cat, t_date))
            db_conn.commit()
            st.success("Task added!")

    st.divider()
    # Count only pending tasks for the metric
    total_tasks = pd.read_sql("SELECT COUNT(*) FROM tasks WHERE status = 'Pending'", db_conn).iloc[0,0]
    st.metric("Pending Tasks", total_tasks)

# 3. Main Dashboard
col_main, col_internals = st.columns([2, 1])

with col_main:
    st.subheader("Your Tasks")
    c1, c2 = st.columns([2, 1])
    with c1:
        search_query = st.text_input("🔍 Search by name (Triggers Full Scan)...")
    with c2:
        filter_cat = st.selectbox("Filter by Category (Triggers Index)...", ["All", "School", "Work", "Housekeeping"])

    # Query Logic (Updated to hide 'Done' tasks)
    if search_query:
        query = "SELECT * FROM tasks WHERE name LIKE ? AND status = 'Pending'"
        df = pd.read_sql(query, db_conn, params=(f'%{search_query}%',))
        plan_query = f"EXPLAIN QUERY PLAN SELECT * FROM tasks WHERE name LIKE '%{search_query}%' AND status = 'Pending'"
    elif filter_cat != "All":
        query = "SELECT * FROM tasks WHERE category = ? AND status = 'Pending'"
        df = pd.read_sql(query, db_conn, params=(filter_cat,))
        plan_query = f"EXPLAIN QUERY PLAN SELECT * FROM tasks WHERE category = '{filter_cat}' AND status = 'Pending'"
    else:
        df = pd.read_sql("SELECT * FROM tasks WHERE status = 'Pending' ORDER BY due_date ASC", db_conn)
        plan_query = "EXPLAIN QUERY PLAN SELECT * FROM tasks WHERE status = 'Pending'"

    if df.empty:
        st.info("No pending tasks found. Add some in the sidebar!")
    else:
        # Display Loop with Edit & Delete options
        for index, row in df.iterrows():
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 2])
                c1.markdown(f"**{row['name']}** \n`{row['category']}`")
                c2.write(f"📅 {row['due_date']}")
                
                with c3:
                    btn_col1, btn_col2 = st.columns(2)
                    # Mark Done Button
                    if btn_col1.button("✅ Done", key=f"done_{row['id']}"):
                        db_conn.execute("UPDATE tasks SET status = 'Done' WHERE id = ?", (row['id'],))
                        db_conn.commit()
                        st.rerun()
                        
                    # Delete Button
                    if btn_col2.button("🗑️ Delete", key=f"del_{row['id']}"):
                        db_conn.execute("DELETE FROM tasks WHERE id = ?", (row['id'],))
                        db_conn.commit()
                        st.rerun()
                
                # Edit Menu (Expander)
                with st.expander("✏️ Edit Task"):
                    with st.form(key=f"edit_form_{row['id']}"):
                        new_name = st.text_input("Name", value=row['name'])
                        
                        # Pre-select the correct category
                        cat_options = ["School", "Work", "Housekeeping"]
                        current_cat_index = cat_options.index(row['category']) if row['category'] in cat_options else 0
                        new_cat = st.selectbox("Category", cat_options, index=current_cat_index)
                        
                        # Pre-fill the correct date
                        try:
                            parsed_date = datetime.strptime(row['due_date'], "%Y-%m-%d").date()
                        except:
                            parsed_date = date.today()
                        new_date = st.date_input("Due Date", value=parsed_date)
                        
                        if st.form_submit_button("Save Changes"):
                            db_conn.execute("UPDATE tasks SET name = ?, category = ?, due_date = ? WHERE id = ?", 
                                           (new_name, new_cat, new_date, row['id']))
                            db_conn.commit()
                            st.rerun()

# 4. Internal Mapping: The Grader View
with col_internals:
    st.subheader("🧠 Database Internals")
    if search_query or filter_cat != "All":
        cursor = db_conn.cursor()
        cursor.execute(plan_query)
        plan = cursor.fetchone()
        
        st.write("**Current Execution Plan:**")
        st.code(plan[3], language="sql")
        
        if "SEARCH" in plan[3]:
            st.success("✅ **Efficient!** SQLite is using the B-Tree Index.")
        else:
            st.warning("⚠️ **Full Scan!** SQLite is reading every single row.")
    else:
        st.info("Search or Filter to see how the database engine handles the request.")
