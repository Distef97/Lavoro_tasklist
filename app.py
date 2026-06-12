import json
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
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

    return render_template('index.html', tasks=filtered_tasks, search_query=request.args.get('search', ''), status_filter=status_filter, total_tasks=total_tasks)

@app.route('/update_status', methods=['POST'])
def update_status():
    # Run the status update script
    subprocess.Popen(['python', 'Status_chain.py'])
    flash('Aggiornamento status avviato in background.', 'info')
    return redirect(url_for('index'))

@app.route('/run_task', methods=['POST'])
def run_task():
    task_name = request.form.get('task_name')
    if task_name:
        # Run the taskchain script with the task_name as argument
        subprocess.Popen(['python', 'running taskchain.py', task_name])
        flash(f'Task {task_name} avviata in background.', 'success')
    else:
        flash('Nessun task selezionato.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
