import sys
import logging
import threading
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
import modbus_tk.modbus_tcp as modbus_tcp
LOGGER = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")
if __name__ == "__main__":
    try:
        # server里的address需要写的树莓派的IP和需要开放的端口，注意开放相应的端口
        SERVER = modbus_tcp.TcpServer(address="127.0.0.1", port=1100)
        LOGGER.info("running...")
        LOGGER.info("enter 'quit' for closing the server")
        # 服务启动
        SERVER.start()
        # 建立第一个从机
        SLAVE1 = SERVER.add_slave(1)
        SLAVE1.add_block('A', cst.HOLDING_REGISTERS, 0, 4)#地址0，长度4
        SLAVE1.add_block('B', cst.HOLDING_REGISTERS, 4, 14)

        #建立另一个从机2
        SLAVE2 = SERVER.add_slave(2)
        SLAVE2.add_block('C', cst.COILS, 0, 10)   #地址0，长度10
        SLAVE2.add_block('D', cst.HOLDING_REGISTERS, 0, 10)#地址0，长度10

        SLAVE1.set_values('A', 0, 4) #改变在地址0处的寄存器的值
        SLAVE1.set_values('B', 4, [1, 2, 3, 4, 5, 5, 12, 1232])     #改变在地址4处的寄存器的值
        SLAVE2.set_values('C', 0, [1, 1, 1, 1, 1, 1])
        SLAVE2.set_values('D', 0, 10)

        while True:
            CMD = sys.stdin.readline()
            if CMD.find('quit') == 0:
                sys.stdout.write('bye-bye\r\n')
                break
            else:
                sys.stdout.write("unknown command %s\r\n" % (args[0]))
    finally:
        SERVER.stop()