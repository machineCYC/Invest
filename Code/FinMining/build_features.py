'''
a script to build all features
'''

import subprocess

def main():
    ### kd feature
    cmd = 'python Features\F_kd.py'
    run = subprocess.call(cmd, shell=False)

    if run == 0:
        print("kd feature build sucessed")
    else:
        print('kd feature build FAILED!!!')

    ### ma feature
    cmd = 'python Features\F_ma.py'
    run = subprocess.call(cmd, shell=False)

    if run == 0:
        print("ma feature build sucessed")
    else:
        print('ma feature build FAILED!!!')

    ### macd feature
    cmd = 'python Features\F_macd.py'
    run = subprocess.call(cmd, shell=False)

    if run == 0:
        print("macd feature build sucessed")
    else:
        print('macd feature build FAILED!!!')


if __name__ == '__main__':
    main()