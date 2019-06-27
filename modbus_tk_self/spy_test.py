import serial

with serial.serial_for_url('spy:///dev/ttyUSB0?file=test.txt', timeout=1) as s:
    s.dtr = False
    s.write('hello world'.encode('ascii'))
    s.read(20)
    s.dtr = True
    s.write(serial.to_bytes(range(256)))
    print(s.read(400))
    s.send_break()

with open('test.txt') as f:
    print(f.read())