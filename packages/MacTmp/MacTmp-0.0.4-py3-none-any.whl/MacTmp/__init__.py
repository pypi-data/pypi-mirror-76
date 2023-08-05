import os

# sudo powermetrics --samplers smc -i1 -n1

def CPU_Temp():
    tmp = (os.popen('sudo powermetrics --samplers smc -i1 -n1')).read()
    return tmp

def GPU_Temp():
    return [i.strip('GPU die temperature: ' for i in os.popen('sudo powermetrics|grep -i "GPU die temperature"').readlines())]
