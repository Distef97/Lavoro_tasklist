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

    dsp_host = os.environ.get('DSP_HOST', 'https://dataspheredev-leasys.eu10.hcs.cloud.sap/')
    dsp_clientid = os.environ.get('DSP_CLIENTID')
    dsp_secret = os.environ.get('DSP_SECRET')

    print(task)
    if dsp_clientid and dsp_secret:
        command = ['datasphere', 'login', '--', 'host', dsp_host, '--', 'client-id', dsp_clientid, '--', 'client-secret', dsp_secret]
        subprocess.run(command, shell=False)
    else:
        print("Warning: DSP_CLIENTID or DSP_SECRET environment variables not set. Authentication may fail.")

    log_list_cmd = ['datasphere', 'tasks', 'chains', 'run', '--space', SPACE_ID, '--objectname', task]
    subprocess.run(log_list_cmd,  input=f"{task}\n", shell=False, text=True)

if __name__ == "__main__":
    run_task()
