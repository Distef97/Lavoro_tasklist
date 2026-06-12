import subprocess
import json
import os

SPACE_ID = "OUTBOUND"

with open("Try.json", "r", encoding="utf-8") as file:
    dati = json.load(file)

contatore = 0

dsp_host = 'https://dataspheredev-leasys.eu10.hcs.cloud.sap/'
dsp_clientid = 'sb-5938700a-8b5f-41ae-9eca-b0e50ae4d925!b629583|client!b3650'
dsp_secret = 'a41fde10-2e82-4f0b-8741-6230c89c5a44$QTZDKnDmpq2l0FvSgVyRVNZJwl1T4rrhg3PD-r3xai4='

if dsp_clientid and dsp_secret:
    command = ['datasphere', 'login', '--', 'host', dsp_host, '--', 'client-id', dsp_clientid, '--', 'client-secret', dsp_secret]
    subprocess.run(command, shell=True)
else:
    print("Warning: DSP_CLIENTID or DSP_SECRET environment variables not set. Authentication may fail.")

for tc in dati[0:len(dati)]:
    tech_name = tc['technicalName']
    print(tech_name)

    log_list_cmd = ['datasphere', 'tasks', 'logs', 'list', '--space', SPACE_ID, '--objectname', tech_name]
    log_result = subprocess.run(log_list_cmd, input=f"{tech_name}", capture_output=True, text=True, shell=True)

    try:
        logs = json.loads(log_result.stdout)
        if len(logs) != 0:
            dati[contatore]['status'] = logs[0]['status']

            with open("Try.json", "w", encoding="utf-8") as file:
                json.dump(dati, file, indent=4, ensure_ascii=False)
    except json.JSONDecodeError:
        pass

    contatore += 1
