import streamlit as st
import pandas as pd
import numpy as np
import uuid

# Define the Streamlit web application
st.set_page_config(page_title="Priority-based Task Scheduling", layout="centered")

# Global Data Storage
if "task_list" not in st.session_state:
    st.session_state.task_list = pd.DataFrame(columns=[
        "TaskID", "Deadline", "Computational Complexity", "User Priority", 
        "System Priority", "CPU", "RAM", "Network Bandwidth"
    ])

if "results" not in st.session_state:
    st.session_state.results = pd.DataFrame(columns=[
        "Scheduling Algorithm Used", "Avg Turnaround Time", "Avg Waiting Time"
    ])

# --- Task Creation Section ---
st.header("Create Tasks")

# Auto-generated Task ID
task_id = str(uuid.uuid4())[:8]

# Task Input Fields
col1, col2 = st.columns(2)
deadline = col1.number_input("Deadline (ms)", min_value=1, value=1000, step=100)
complexity = col2.selectbox("Computational Complexity", ["Heavy", "Medium", "Light"])
user_priority = col1.selectbox("User Defined Priority", ["High", "Medium", "Low"])

# Resource Requirements
cpu = st.number_input("CPU (1-100)", min_value=1, max_value=100, value=10, step=1)
ram = st.number_input("RAM (KB)", min_value=1, max_value=1024, value=256, step=1)
bandwidth = st.number_input("Network Bandwidth (KB, 0-10GB)", min_value=0, max_value=10_000_000, value=500_000, step=1)

# Submit New Task
if st.button("Submit Task"):
    new_task = pd.DataFrame([{
        "TaskID": task_id,
        "Deadline": deadline,
        "Computational Complexity": complexity,
        "User Priority": user_priority,
        "System Priority": None,  # To be determined
        "CPU": cpu,
        "RAM": ram,
        "Network Bandwidth": bandwidth
    }])
    st.session_state.task_list = pd.concat([st.session_state.task_list, new_task], ignore_index=True)
    st.rerun()

# Random Process Generator
def generate_random_tasks():
    complexities = ["Heavy", "Medium", "Light"]
    priorities = ["High", "Medium", "Low"]
    
    random_tasks = pd.DataFrame([
        {
            "TaskID": str(uuid.uuid4())[:8],
            "Deadline": np.random.randint(500, 5000),
            "Computational Complexity": np.random.choice(complexities),
            "User Priority": np.random.choice(priorities),
            "System Priority": None,
            "CPU": np.random.randint(1, 101),
            "RAM": np.random.randint(1, 1025),
            "Network Bandwidth": np.random.randint(0, 10_000_001)
        }
        for _ in range(30)
    ])
    
    st.session_state.task_list = pd.concat([st.session_state.task_list, random_tasks], ignore_index=True)

if st.button("Generate 30 Random Tasks"):
    generate_random_tasks()
    st.rerun()

# --- Task Table Section ---
st.header("Task List")
st.write("List of tasks created:")

if not st.session_state.task_list.empty:
    st.dataframe(st.session_state.task_list)

# --- Scheduling Algorithm Implementation ---
def heuristic_scheduling(tasks):
    """ Placeholder function for heuristic scheduling algorithms. 
    You can replace this with your own heuristic approach. """
    
    if tasks.empty:
        return pd.DataFrame(columns=[
            "Scheduling Algorithm Used", "Avg Turnaround Time", "Avg Waiting Time"
        ])

    # Example: Simple priority-based sorting
    priority_map = {"High": 1, "Medium": 2, "Low": 3}
    tasks["System Priority"] = tasks["User Priority"].map(priority_map)

    # Sort tasks based on system priority & deadline
    sorted_tasks = tasks.sort_values(by=["System Priority", "Deadline"])

    avg_turnaround_time = sorted_tasks["Deadline"].mean()
    avg_waiting_time = avg_turnaround_time / 2  # Approximation

    results = pd.DataFrame([{
        "Scheduling Algorithm Used": "Heuristic Priority Scheduling",
        "Avg Turnaround Time": round(avg_turnaround_time, 2),
        "Avg Waiting Time": round(avg_waiting_time, 2)
    }])
    
    return results

# Submit Tasks Button
if st.button("Submit Tasks for Scheduling"):
    st.session_state.results = heuristic_scheduling(st.session_state.task_list)
    st.rerun()

# --- Scheduling Results Section ---
st.header("Scheduling Results")
st.write("Results from the heuristic scheduling algorithm:")

if not st.session_state.results.empty:
    st.dataframe(st.session_state.results)
