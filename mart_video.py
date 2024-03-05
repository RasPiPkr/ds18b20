import tkinter as tk
import threading
import time
import glob


# Setup the DS18B20 Temperature Sensor.
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')


def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


def get_temp():
    c, f = read_temp(device_folder[0] + '/w1_slave')
    t_str.set('{:.1f}C'.format(c))
    root.after(1000, get_temp())


root = tk.Tk()
root.title('Temperature')
root.geometry('200x100')

t_str = tk.StringVar()
label = tk.Label(root, textvariable=t_str)
label.pack()

thread = threading.Thread(target=get_temp)
thread.start()

root.mainloop()


##while True:
##    c, f = read_temp(device_folder[0] + '/w1_slave')
##    print('{:.2f}C'.format(c))
##    time.sleep(1)
















