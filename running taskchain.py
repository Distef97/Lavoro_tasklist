import subprocess
import sys
import os

SPACE_ID = "OUTBOUND"

def run_task(task_name=None):
    if not task_name:
        if len(sys.argv) > 1:
            task_name = sys.argv[1]
        else:
            task_name = "TC_LTR1_PRICE_LIST_AUTO_DK_GP"

    task=task_name

    dsp_host = 'https://dataspheredev-leasys.eu10.hcs.cloud.sap/'
    dsp_clientid = 'sb-5938700a-8b5f-41ae-9eca-b0e50ae4d925!b629583|client!b3650'
    dsp_secret = 'a41fde10-2e82-4f0b-8741-6230c89c5a44$QTZDKnDmpq2l0FvSgVyRVNZJwl1T4rrhg3PD-r3xai4='

    print(task)
    if dsp_clientid and dsp_secret:
        command = ['datasphere', 'login', '--', 'host', dsp_host, '--', 'client-id', dsp_clientid, '--', 'client-secret', dsp_secret]
        subprocess.run(command, shell=True)
    else:
        print("Warning: DSP_CLIENTID or DSP_SECRET environment variables not set. Authentication may fail.")

    log_list_cmd = ['datasphere', 'tasks', 'chains', 'run', '--space', SPACE_ID, '--objectname', task]
    subprocess.run(log_list_cmd,  input=f"{task}\n", shell=True, text=True)

if __name__ == "__main__":
    run_task()
