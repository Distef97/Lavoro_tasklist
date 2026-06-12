import json
import subprocess
import threading
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os

app = Flask(__name__)

active_processes = 0
process_lock = threading.Lock()

def run_script_in_background(command):
    global active_processes
    with process_lock:
        active_processes += 1
    try:
        subprocess.run(command)
    finally:
        with process_lock:
            active_processes -= 1
app.secret_key = 'supersecretkey'  # Needed for flashing messages

DATA_FILE = 'Try.json'

def get_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

@app.route('/')
def index():
    tasks = get_tasks()

    search_query = request.args.get('search', '').lower()
    status_filter = request.args.get('status', 'ALL')

    filtered_tasks = []
    for task in tasks:
        match_search = search_query in task.get('technicalName', '').lower()
        match_status = status_filter == 'ALL' or status_filter == task.get('status', '').upper()

        if match_search and match_status:
            filtered_tasks.append(task)

    total_tasks = len(filtered_tasks)

    is_updating_flag = False
    with process_lock:
        is_updating_flag = active_processes > 0

    return render_template('index.html', tasks=filtered_tasks, search_query=request.args.get('search', ''), status_filter=status_filter, total_tasks=total_tasks, is_updating=is_updating_flag)

@app.route('/is_updating', methods=['GET'])
def is_updating():
    with process_lock:
        return jsonify({"is_updating": active_processes > 0})

@app.route('/update_status', methods=['POST'])
def update_status():
    search_query = request.form.get('search', '')
    status_filter = request.form.get('status', 'ALL')
    # Run the status update script
    threading.Thread(target=run_script_in_background, args=(['python', 'Status_chain.py'],)).start()
    flash('Aggiornamento status avviato in background.', 'info')
    return redirect(url_for('index', search=search_query, status=status_filter))

@app.route('/update_single_status', methods=['POST'])
def update_single_status():
    search_query = request.form.get('search', '')
    status_filter = request.form.get('status', 'ALL')
    task_name = request.form.get('task_name')
    if task_name:
        threading.Thread(target=run_script_in_background, args=(['python', 'update_single_status.py', task_name],)).start()
        flash(f'Aggiornamento status per {task_name} avviato in background.', 'info')
    else:
        flash('Nessun task selezionato.', 'error')
    return redirect(url_for('index', search=search_query, status=status_filter))

@app.route('/run_task', methods=['POST'])
def run_task():
    search_query = request.form.get('search', '')
    status_filter = request.form.get('status', 'ALL')
    task_name = request.form.get('task_name')
    if task_name:
        # Run the taskchain script with the task_name as argument
        threading.Thread(target=run_script_in_background, args=(['python', 'running taskchain.py', task_name],)).start()
        flash(f'Task {task_name} avviata in background.', 'success')
    else:
        flash('Nessun task selezionato.', 'error')
    return redirect(url_for('index', search=search_query, status=status_filter))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
