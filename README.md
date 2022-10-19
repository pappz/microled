# Microled

## WebREPL

Default port: 8266

[Webrepl repo](https://github.com/micropython/webrepl)

[Webrepl online](http://micropython.org/webrepl)

## Micropython env

https://github.com/micropython/micropython/wiki/Getting-Started

## Command line tips

Connect to serial port. Exit with **Control+a+x**
```commandline
picocom /dev/ttyUSB0 -b115200
```

File manipulation
```
ampy -p /dev/ttyUSB0 put main.py 
```

## Send color command
`
```commandline
mosquitto_pub -h 192.168.0.2 -u username -P secret -m "{'r': 0, 'g': 50, 'b': 20 }" -t "kesmarki/led"
```