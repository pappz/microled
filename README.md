# WebREPL

https://github.com/micropython/webrepl

http://micropython.org/webrepl

# Micropython env

https://github.com/micropython/micropython/wiki/Getting-Started

# Command line tips

```commandline
picocom /dev/ttyUSB0 -b115200
ampy -p /dev/ttyUSB0 put main.py 
```

# switch led

```commandline
mosquitto_pub -h 192.168.0.2 -u username -P secret -m "{'r': 0, 'g': 50, 'b': 20 }" -t "kesmarki/led"
```