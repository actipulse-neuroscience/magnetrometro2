import serial
import time
import numpy as np
#%% 
# Set the 3D printer serial port and baud rate
printer_port = 'COM4'  # Replace 'COMY' with the appropriate port name
printer_baud_rate = 115200
# Set the Arduino serial port and baud rate
arduino_port = 'COM3'  # Replace 'COMX' with the appropriate port name
arduino_baud_rate = 1000000

#%% 
# Establish connection with 3D printer
printer_ser = serial.Serial(printer_port, printer_baud_rate)
time.sleep(2)  # Wait for printer to initialize
arduino_ser = serial.Serial(arduino_port, arduino_baud_rate)
time.sleep(2)  # Wait for printer to initialize
#%% 
# Set G-code command to send to the printer
printer_ser.write(("G28\n").encode()) # Find (0,0,0)
gcode_instructions = [
    'G90',                      # Set to absolute positioning mode
    'G1 Z35',                   # Move to the center of the bed plate
    'G1 X101 Y135',             # Move to the center of the bed plate
    'G91',                      # Set to relative positioning mode
    'G1 Y12.5 F6000',           # Move +12.5 mm in the Y axis at a feedrate of 6000 mm/min
    'G1 X-12.5'                 # Move -12.5 mm in the X axis (relative to the current position)
]
for instruction in gcode_instructions:
    printer_ser.write((instruction + '\n').encode())
    time.sleep(1)  # Delay between instructions

#%% 
additional_gcode_instructions = []
distance_movement=4.5 # distance center-center of wheels
# Generate the G-code instructions
for moment in range (12):   
    for _ in range(11):
        additional_gcode_instructions.append("G1 X" + str(distance_movement))  # Move +4.5 mm in the X axis (relative to the current position)
        # Move 4.5 mm in the negative Y-axis
    additional_gcode_instructions.append("G1 X-" + str(11* distance_movement)+" G1 Y-" + str(distance_movement))
    #additional_gcode_instructions.append("G1 Y-" + str(distance_movement))

#%% 
# Set recording duration and initialize data array
array_final = list () 
printer_ser.write(("G91\n").encode())

for instruction in additional_gcode_instructions:
    lista = np.arange(20000)
    array_vacio = np.zeros (20000)
    time_array = np.zeros(20000)
    arduino_ser.flushInput()
    arduino_ser.write(b'1')
    time.sleep(1)  # Wait for printer to initialize
    start_time = time.perf_counter()  # Record the start time
    arduino_ser.reset_input_buffer()
    for data in lista: 
        dummy = arduino_ser.readline().decode().strip()
        array_vacio[data] = dummy
        time_array[data] = time.perf_counter() - start_time
    array_final.append(array_vacio)
    printer_ser.write((instruction + '\n').encode())
    time.sleep(1)
printer_ser.write(("G90\n").encode())

#%% 
array_final = np.array(array_final)
matriz = np.mean (array_final, axis =1)

#%% 
matriz2=np.reshape(matriz,(12,12))
import matplotlib.pyplot as plt
plt.imshow(matriz2, cmap='inferno')  # You can choose a different colormap if desired

#%%
Milivolts=(array_final*3300)/1023 #calculo de mV
offset=(508*3300)/1023
Magnetic_field_mT=(Milivolts-offset)/7.5
Magnetic_field_gauss=Magnetic_field_mT*(10)

#%% 
plt.plot(Magnetic_field_gauss[66,2000:3000])                  # generar el gráfico de la función y=x
plt.show()                   # mostrar el gráfico en pantalla

#%% 
Datos = np.transpose(array_final)
np.savetxt("Medicion_Bobina_3.csv", Datos, delimiter=",")

#%% 
printer_ser.close()
arduino_ser.close()
