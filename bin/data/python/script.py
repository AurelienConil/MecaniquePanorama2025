import serial
import time
import os
import sys
import glob
import subprocess
from pythonosc import udp_client

# Serial ID to select the port
SERIAL_ID = 2

# OS choose ofApp working directory
# os.chdir('ImageSeqFromOSC/')

def start_app():
    global mpPath
    global ofAppName
    print("========= START OF APP======")
    if sys.platform.startswith('darwin'):
        cmd = [os.path.join(mpPath, ofAppName, "bin", f"{ofAppName}Debug.app/Contents/MacOS/{ofAppName}Debug")]
    elif sys.platform.startswith('win'):
        cmd = [os.path.join(mpPath, ofAppName, 'bin', f"{ofAppName}.exe")]
    print("launch : ")
    print(cmd)
    subprocess.Popen(cmd)
    print(cmd)
    print("======== OF APP STARTED ====")

def kill_app():
    print("========= KILL OF APP ======")
    path = os.path.join(mpPath, "script")
    os.chdir(path)
    print("Path is " + path)
    if sys.platform.startswith('win'):
        subprocess.call([r'quit_app.bat'])
    else:
        subprocess.call(['./quit_app.sh'])

def shutdown_computer():
    print("========= SHUTDOWN COMPUTER ======")
    path = os.path.join(mpPath, "script")
    os.chdir(path)
    print("Path is " + path)
    if sys.platform.startswith('win'):
        subprocess.call(["shutdown", "/s"])
    else:
        subprocess.call(['sudo', 'shutdown', 'now'])

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    ports = []
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port, 115200)
            s.close()
            result.append(port)
        except:
            pass
    return result

if __name__ == '__main__':
    
    print("========= Mecanique Panorama : PYTHON ARDUINO ======")
    # Serial print port available
    serialNames = serial_ports()
    if not serialNames:
        print("Pas de port disponible, merci et au revoir.")
        sys.exit(0)
        
    print("Liste des ports série disponibles :")
    print(serialNames)
    # Final Path
    global mpPath
    global ofAppName
    ofAppName = "ImageSeqFromOSC"
    if sys.platform.startswith('win'):
        mpPath = os.path.join('C:', os.sep, 'Users', 'Aurelien', 'Documents', 'OPENFRAMEWORKS', 'of_v0.10.0_vs2017_release', 'apps', 'MecaniquePanorama')
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        mpPath = "/home/nano/Dev/of/apps/MecaniquePanorama/"
    elif sys.platform.startswith('darwin'):
        mpPath = "/Users/adminmac/Boulot/Mecanique-Panorama/GIT/MecaniquePanorama"
    else:
        raise EnvironmentError('Unsupported platform')

    # Serial connect
    try:
        if SERIAL_ID < len(serialNames):
            selected_port = serialNames[SERIAL_ID]
        else:
            selected_port = serialNames[0]

        print(f"Connection au Serial : {selected_port}")
        ser = serial.Serial(selected_port, 115200)
    except:
        print("Impossible to connect to Serial")
        ser = None

    # Start OF app
    #time.sleep(1)
    #start_app()

    # OSC
    client = udp_client.SimpleUDPClient("127.0.0.1", 12345)

    value = 0
    param = []
    msg = []

    while True:
        isMessage = False
        finalValue = -1000
        while ser.in_waiting:
            if ser:
                msg = ser.readline().decode('utf-8').strip()
            else:
                msg = ""

            if len(msg) > 1:
                value = int(msg[1])

                if msg[0] == "-":
                    if finalValue == -1000:
                        finalValue = 1
                    finalValue += value
                    isMessage = True
                elif msg[0] == '+':
                    if finalValue == -1000:
                        finalValue = -1
                    finalValue -= value
                    isMessage = True
                elif msg[0] == 'q':
                    shutdown_computer()

        if isMessage:
            try:
                if finalValue > 0:
                    client.send_message("/transport/next", abs(finalValue))
                    print("next frames :" + str(finalValue))
                else:
                    client.send_message("/transport/previous", abs(finalValue))
                    print("previous frames : " + str(finalValue))
            except Exception as e:
                print(e)

        time.sleep(0.055)
