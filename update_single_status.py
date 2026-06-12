import subprocess
import json
import sys
import os

SPACE_ID = "OUTBOUND"

if len(sys.argv) < 2:
    print("Please provide a task name.")
    sys.exit(1)

target_task_name = sys.argv[1]

try:
    with open("Try.json", "r", encoding="utf-8") as file:
        dati = json.load(file)
except FileNotFoundError:
    print("Try.json non trovato.")
    sys.exit(1)

task_found = False
for tc in dati:
    if tc['technicalName'] == target_task_name:
        task_found = True
        break

if not task_found:
    print(f"Task {target_task_name} not found in Try.json.")
    sys.exit(1)

dsp_host = os.environ.get('DSP_HOST', 'https://dataspheredev-leasys.eu10.hcs.cloud.sap/')
dsp_clientid = os.environ.get('DSP_CLIENTID')
dsp_secret = os.environ.get('DSP_SECRET')

if dsp_clientid and dsp_secret:
    command = ['datasphere', 'login', '--', 'host', dsp_host, '--', 'client-id', dsp_clientid, '--', 'client-secret', dsp_secret]
    subprocess.run(command, shell=True)
else:
    print("Warning: DSP_CLIENTID or DSP_SECRET environment variables not set. Authentication may fail.")

for i, tc in enumerate(dati):
    if tc['technicalName'] == target_task_name:
        print(f"Updating status for {target_task_name}")

        log_list_cmd = ['datasphere', 'tasks', 'logs', 'list', '--space', SPACE_ID, '--objectname', target_task_name]
        log_result = subprocess.run(log_list_cmd, input=f"{target_task_name}", capture_output=True, text=True, shell=True)

        try:
            logs = json.loads(log_result.stdout)
            if len(logs) != 0:
                dati[i]['status'] = logs[0]['status']

                with open("Try.json", "w", encoding="utf-8") as file:
                    json.dump(dati, file, indent=4, ensure_ascii=False)
                print(f"Status updated successfully for {target_task_name}")
        except json.JSONDecodeError:
            print(f"Failed to decode logs for {target_task_name}")
        break
