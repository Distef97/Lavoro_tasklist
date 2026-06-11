import subprocess



def list_spaces ():

    # Step 1: Login to Datasphere using host and secrets file
    dsp_host = 'https://dataspheredev-leasys.eu10.hcs.cloud.sap/'
    dsp_clientid = 'sb-5938700a-8b5f-41ae-9eca-b0e50ae4d925!b629583|client!b3650'
    dsp_secret = 'a41fde10-2e82-4f0b-8741-6230c89c5a44$QTZDKnDmpq2l0FvSgVyRVNZJwl1T4rrhg3PD-r3xai4='

    command = f'datasphere login -- host {dsp_host} -- client-id {dsp_clientid} -- client-secret {dsp_secret}'

    subprocess.run(command, shell=True) 

    command = f'datasphere spaces list --json'
    results= subprocess.run(command, shell=True)
    print(results)

    command = f'datasphere tasks logs list --space OUTBOUND'


    result_space = subprocess.run(command, capture_output=True, shell=True,
    text=True) 
    result_space = subprocess.run(f'TC_LTR1_01_001_GL_ED_GP', capture_output=True, shell=True,
    text=True) # Run the command and capture output
    print(result_space)

    spaces = result_space # Split output into individual lines

    

list_spaces ()

print(spaces)