import subprocess



def list_tasks ():

    # Step 1: Login to Datasphere using host and secrets file
    dsp_host = 'https://dataspheredev-leasys.eu10.hcs.cloud.sap/'
    dsp_clientid = 'sb-5938700a-8b5f-41ae-9eca-b0e50ae4d925!b629583|client!b3650'
    dsp_secret = 'a41fde10-2e82-4f0b-8741-6230c89c5a44$QTZDKnDmpq2l0FvSgVyRVNZJwl1T4rrhg3PD-r3xai4='

    command = f'datasphere login -- host {dsp_host} -- client-id {dsp_clientid} -- client-secret {dsp_secret}'

    subprocess.run(command, shell=True) # Execute the login command

    command = ['datasphere', 'objects','task-chains', 'list', '--space', 'OUTBOUND', '--top', '100', ' --output ', 'C:/Users/simonedistefano/OneDrive - KPMG/Documents/SAP Datasphere/Datasphere CLI/Try.json']

    result=subprocess.run(command, capture_output=True,text=True, shell=True) # Execute the login command
    result=result.stdout
    with open("C:/Users/simonedistefano/OneDrive - KPMG/Documents/SAP Datasphere/Datasphere CLI/Try.json", "w", encoding="utf-8") as file:
        file.write(result)
list_tasks ()
