# robocontroller
Serial interface for controlling IKA RCT 5 ditigtal

# Finding the right COM port in Python
ports = list_ports.comports()
  for port in ports:
      print(port.name)

# Example run (3 houes at 
ser = serial.Serial(port="COM5", timeout=0.5)

 temp = 87
    set_par(ser, temp, temp=True)
    set_par(ser, 220, speed=True)
    start_stop(ser, True, heater=True)
    start_stop(ser, True, motor=True)
    FILENAME = "temps.txt"
    with open(FILENAME, 'a') as f:
        f.write("Start run\n")
    record_temp(ser, 180, 10, FILENAME) # 240, 10
  
