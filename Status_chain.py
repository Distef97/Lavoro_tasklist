import subprocess
import json
SPACE_ID = "OUTBOUND"

# 1. Apri il file JSON in modalità lettura ('r')
with open("Try.json", "r", encoding="utf-8") as file:

    # 2. Usa json.load() per caricare il contenuto nella variabile
    dati = json.load(file)

#print(dati[1]['technicalName'])

# def list_tasks ():

#     # Step 1: Login to Datasphere using host and secrets file
#     dsp_host = 'https://dataspheredev-leasys.eu10.hcs.cloud.sap/'
#     dsp_clientid = 'sb-5938700a-8b5f-41ae-9eca-b0e50ae4d925!b629583|client!b3650'
#     dsp_secret = 'a41fde10-2e82-4f0b-8741-6230c89c5a44$QTZDKnDmpq2l0FvSgVyRVNZJwl1T4rrhg3PD-r3xai4='

#     command = f'datasphere login -- host {dsp_host} -- client-id {dsp_clientid} -- client-secret {dsp_secret}'

#     subprocess.run(command, shell=True) # Execute the login command

#     command = ['datasphere', 'objects','task-chains', 'read', '--space', 'OUTBOUND',  ' --output ', 'Try.json']

#     result=subprocess.run(command, capture_output=True,text=True, shell=True) # Execute the login command
#     result=result.stdout
#     with open("Try.json", "w", encoding="utf-8") as file:
#         file.write(result)
contatore = 0

for tc in dati[0:len(dati)]:
    tech_name = tc['technicalName']
    
    print(tech_name)
    # Step 1: Login to Datasphere using host and secrets file
    dsp_host = 'https://dataspheredev-leasys.eu10.hcs.cloud.sap/'
    dsp_clientid = 'sb-5938700a-8b5f-41ae-9eca-b0e50ae4d925!b629583|client!b3650'
    dsp_secret = 'a41fde10-2e82-4f0b-8741-6230c89c5a44$QTZDKnDmpq2l0FvSgVyRVNZJwl1T4rrhg3PD-r3xai4='

    command = f'datasphere login -- host {dsp_host} -- client-id {dsp_clientid} -- client-secret {dsp_secret}'

    subprocess.run(command, shell=True) # Execute the login command
    # 2. Per ogni catena, recupera la lista dei log per trovare l'ultima esecuzione
    log_list_cmd = f'datasphere tasks logs list --space {SPACE_ID} --objectname {tech_name}'
    log_result = subprocess.run(log_list_cmd, input=f"{tech_name}", capture_output=True, text=True, shell=True)
    logs = json.loads(log_result.stdout)
    #print(logs[0]['status'])
    if len(logs) != 0:
        dati[contatore]['status'] = logs[0]['status']
    
        with open("Try.json", "w", encoding="utf-8") as file:
            # 2. Usa json.load() per caricare il contenuto nella variabile
            json.dump(dati, file, indent=4, ensure_ascii=False)
    contatore += 1
    
                        
               