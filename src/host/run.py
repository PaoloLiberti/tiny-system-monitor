import serial
import psutil
import gpu
import cpu
import struct

def get_cpu_temperature():
    temperature = psutil.sensors_temperatures()
    if 'cpu-thermal' in temperature:
        cpu_temperature = temperature['cpu-thermal'][0].current
        return cpu_temperature
    else:
        return None


ser = serial.Serial(
    '/dev/tty.usbmodem14314101',  # Change this lino to the port the device is connected
    baudrate=115200,
    timeout=0.2)

# This is platform dependant and provided for a reference
gpu_usage = gpu.GpuUsage()
gpu_usage.start()

temp_sensor = cpu.CpuTemperature()
temp_sensor.start()

counter = 0

disk_percent = 0
net_stat = psutil.net_io_counters()
acc_bytes_sent = net_stat.bytes_sent
acc_bytes_recv = net_stat.bytes_recv
while True:
    cpu_percent = round(psutil.cpu_percent(interval=1))
    if counter % 20 == 0:
        disk_percent = psutil.disk_usage('/').percent

    net_stat = psutil.net_io_counters()
    bits_sent_per_sec = (psutil.net_io_counters().bytes_sent - acc_bytes_sent) * 8
    bits_recv_per_sec = (psutil.net_io_counters().bytes_recv - acc_bytes_recv) * 8
    if bits_recv_per_sec < 0:
        bits_recv_per_sec = 0
    if bits_sent_per_sec < 0:
        bits_sent_per_sec = 0
    acc_bytes_sent = net_stat.bytes_sent
    acc_bytes_recv = net_stat.bytes_recv

    print("🚀 ~ file: run.py:49 ~ temp_sensor:", temp_sensor.temperature)

    message = struct.pack("bbbbIIf", cpu_percent, round(gpu_usage.usage), int(psutil.virtual_memory().percent),
                          int(disk_percent), int(bits_recv_per_sec), int(bits_sent_per_sec), round(temp_sensor.temperature))
    
    # print("🚀 ~ file: run.py:48 ~ message:", message)

    ser.write(message)
    ser.flush()
    counter = counter + 1
    if counter > 20000000:
        counter = 0
