import sqlite3
import time

conn = sqlite3.connect('tasks_pro.db')
cursor = conn.cursor()

print("\n=== TASKFLOW PRO: ADVANCED SPEED TEST ===")

# --- Test 1: Search by Name ONLY (Full Scan) ---
print("\n--- 1. FULL TABLE SCAN ---")
task_to_search = input("Type a task name to search for (e.g., Environmental): ")

start_scan = time.perf_counter()
cursor.execute("SELECT * FROM tasks WHERE name LIKE ?", ('%' + task_to_search + '%',))
results_scan = cursor.fetchall()
end_scan = time.perf_counter()

print(f"🚨 SCAN TIME: {(end_scan - start_scan) * 1000:.4f} ms (Found {len(results_scan)} matches)")


# --- Test 2: Filter by Category ONLY (B-Tree) ---
print("\n--- 2. B-TREE INDEX ONLY ---")
category_to_search = input("Type a category to filter by (e.g., School): ")

start_btree = time.perf_counter()
cursor.execute("SELECT * FROM tasks WHERE category = ?", (category_to_search,))
results_btree = cursor.fetchall()
end_btree = time.perf_counter()

print(f"🚀 INDEX TIME:  {(end_btree - start_btree) * 1000:.4f} ms (Found {len(results_btree)} matches)")


# --- Test 3: Combined Search (B-Tree + Filter) ---
print("\n--- 3. COMBINED: NAME WITHIN CATEGORY ---")
print(f"Searching for '{task_to_search}' inside the '{category_to_search}' category...")

start_combined = time.perf_counter()
# This query uses both!
cursor.execute("SELECT * FROM tasks WHERE category = ? AND name LIKE ?", (category_to_search, '%' + task_to_search + '%'))
results_combined = cursor.fetchall()
end_combined = time.perf_counter()

print(f"🎯 COMBINED TIME: {(end_combined - start_combined) * 1000:.4f} ms (Found {len(results_combined)} matches)")
print("=========================================\n")

conn.close()