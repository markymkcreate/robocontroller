# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 10:09:07 2024

@author: marcud
"""

import serial
from serial.tools import list_ports
import time
from random import randint


def set_par(ser, value, temp=False, speed=False):
    TEMP_COM = "OUT_SP_1"
    SPEED_COM = "OUT_SP_4"
    
    if temp:
        cmd_pfx = TEMP_COM
    elif speed:
        cmd_pfx = SPEED_COM
    else:
        print("Err: Temp or speed not specified.")
        return None
        
    cmd = "{} {}\r\n".format(cmd_pfx, value)
    ser.write(cmd.encode())

def start_stop(ser, start_or_stop, heater=False, motor=False):
    # start_or_stop: True for start, False for stop
    HEATER_SFX = 1
    MOTOR_SFX = 4

    if heater:
        cmd_sfx = HEATER_SFX
    elif motor:
        cmd_sfx = MOTOR_SFX
    else:
        print("Err: Motor or heater not specified.")
        return None
    
    cmd_pfx = "START" if start_or_stop else "STOP"
        
    cmd = "{}_{}\r\n".format(cmd_pfx, cmd_sfx)
    ser.write(cmd.encode())
    

def read_par(ser, ext_temp=False, plate_temp=False, speed=False, viscosity=False,
             rated_temp=False, safe_temp=False, rated_speed=False):
    
    PAR_DICT = ["PV_1", "PV_2", "PV_4", "PV_5", "SP_1", "SP_3", "SP_4"]
    par_list = [ext_temp, plate_temp, speed, viscosity, rated_temp, safe_temp, rated_speed]
    
    if sum(par_list) > 1:
        print("ERR: Too many parameters specified")
        return None
    elif sum(par_list) == 0:
        print("ERR: Specify at least one paramter")
        return None
    
    par_index = par_list.index(1)
    cmd = "IN_" + PAR_DICT[par_index] + "\r\n"
    
    ser.write(cmd.encode())
    response = ser.readline()
    text_response = response.decode().strip() # Returns the paramter followed by a number, which I am not sure what means
    
    if text_response == "" or text_response == None:
        print("Err: nothing returned for parameter")
        return None
    
    return float(text_response.split(" ")[0])
    

def record_temp(ser, t, interval, fname): # t in minutes, interval in minutes
    
    t0 = time.time()
    t_sec = t * 60
    int_sec = interval * 60
    temps = []
    while time.time() < t0 + t_sec:
        temp = read_par(ser, ext_temp=True)
        temps.append(temp)
        with open(fname, 'a') as f:
            f.write(str(time.time()) + "," + str(temp) + "\n")
        time.sleep(int_sec)
        
    return temps

