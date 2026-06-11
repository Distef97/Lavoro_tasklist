import subprocess
#datasphere tasks chains run --space OUTBOUND
SPACE_ID = "OUTBOUND"
#-- objects TC_LTR1_PRICE_LIST_AUTO_DK_GP , input=f"{task}"

import sys
def run_task(task_name=None):
    if not task_name:
        if len(sys.argv) > 1:
            task_name = sys.argv[1]
        else:
            task_name = "TC_LTR1_PRICE_LIST_AUTO_DK_GP"

    task=task_name
    # Step 1: Login to Datasphere using host and secrets file
    dsp_host = 'https://dataspheredev-leasys.eu10.hcs.cloud.sap/'
    dsp_clientid = 'sb-5938700a-8b5f-41ae-9eca-b0e50ae4d925!b629583|client!b3650'
    dsp_secret = 'a41fde10-2e82-4f0b-8741-6230c89c5a44$QTZDKnDmpq2l0FvSgVyRVNZJwl1T4rrhg3PD-r3xai4='

    command = f'datasphere login -- host {dsp_host} -- client-id {dsp_clientid} -- client-secret {dsp_secret}'
    print(task)
    subprocess.run(command, shell=True) # Execute the login command
    ######
    log_list_cmd = f'datasphere tasks chains run --space {SPACE_ID} --objectname {task}'
    subprocess.run(log_list_cmd,  input=f"{task}\n", shell=True, text=True)

if __name__ == "__main__":
    run_task()