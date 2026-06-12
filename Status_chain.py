import subprocess
import json
import os

SPACE_ID = "OUTBOUND"

with open("Try.json", "r", encoding="utf-8") as file:
    dati = json.load(file)

contatore = 0

dsp_host = os.environ.get('DSP_HOST', 'https://dataspheredev-leasys.eu10.hcs.cloud.sap/')
dsp_clientid = os.environ.get('DSP_CLIENTID')
dsp_secret = os.environ.get('DSP_SECRET')

if dsp_clientid and dsp_secret:
    command = ['datasphere', 'login', '--', 'host', dsp_host, '--', 'client-id', dsp_clientid, '--', 'client-secret', dsp_secret]
    subprocess.run(command, shell=False)
else:
    print("Warning: DSP_CLIENTID or DSP_SECRET environment variables not set. Authentication may fail.")

for tc in dati[0:len(dati)]:
    tech_name = tc['technicalName']
    print(tech_name)

    log_list_cmd = ['datasphere', 'tasks', 'logs', 'list', '--space', SPACE_ID, '--objectname', tech_name]
    log_result = subprocess.run(log_list_cmd, input=f"{tech_name}", capture_output=True, text=True, shell=False)

    try:
        logs = json.loads(log_result.stdout)
        if len(logs) != 0:
            dati[contatore]['status'] = logs[0]['status']

            with open("Try.json", "w", encoding="utf-8") as file:
                json.dump(dati, file, indent=4, ensure_ascii=False)
    except json.JSONDecodeError:
        pass

    contatore += 1
