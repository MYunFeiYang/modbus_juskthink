import binascii
import codecs

import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import serial


def pumpAndPc():
    """
    模拟机器和pc通过RS232通信，机器收集电气特征写入串口，pc通过串口读到机器电气特征数据，
    处理后通过modbus写入pc（从机）的保存`寄存器，供客户端主机读取
    """
    try:
        ser = serial.Serial('/dev/ttyUSB0')
        ser.baudrate = 9600
        ser.bytesize = serial.EIGHTBITS
        ser.stopbits = serial.STOPBITS_ONE
        ser.parity = serial.PARITY_NONE
        ser.timeout = 1
        print(ser.write("@00READ_RUN_PARA".encode('ascii')))
        if (ser.readline().decode() == "@00READ_RUN_PARA"):
            print(ser.write("@00RUN_PARA000003003100102000144\x00\x00\x00\x00\x00\x00\r\n".encode('ascii')))
        str = ser.readline().decode()

        fdpCurrent = str[11:13]
        fdpCurrent = int(fdpCurrent)

        rootsCurrent = str[13:15]
        rootsCurrent = int(rootsCurrent)

        fdpTemp = str[15:18]
        fdpTemp = int(fdpTemp)

        rootsTemp = str[18:21]
        rootsTemp = int(rootsTemp)

        n2Flow = str[21:23]
        n2Flow = int(n2Flow)

        pressure = str[23:27]
        pressure = int(pressure)

        runTime = str[27:32]
        runTime = int(runTime)

        errSta = errStaProgress(str)

        writeHoldingRegisters(fdpCurrent, rootsCurrent, fdpTemp, rootsTemp, n2Flow, pressure, runTime, errSta)
    except Exception as e:
        print("---异常---：", e)


def writeHoldingRegisters(fdpCurrent, rootsCurrent, fdpTemp, rootsTemp, n2Flow, pressure, runTime, errSta):
    """
    modbus监听pc，创建从机，并将从机收集到的信息写入从机保存寄存器
    """
    try:
        # 创建监听本地pc的modbus服务
        server = modbus_tcp.TcpServer(address="192.168.123.51", port=1100)
        # 启动服务
        server.start()
        # 创建从机1
        slave = server.add_slave(1)
        # 给从机1在寄存器中申请一块存储空间，传入空间的起始地址和存储长度
        slave.add_block('feedback', cst.HOLDING_REGISTERS, 0, 47)
        # 将处理好的信息写入保存寄存器
        slave.set_values('feedback', 0,
                         [fdpCurrent, rootsCurrent, fdpTemp, rootsTemp, n2Flow, pressure, runTime] + errSta)

    except Exception as e:
        print("---异常---：", e)


def errStaProgress(str):
    """
    字符串切片获得五个错误状态的ascii码，将ascii码转化为int，int转化为八位的二进制，获得40位代表机器的四十中状态
    """
    errSta = []
    for i in range(32, 37):
        errStaByte = str[i:i + 1]
        errStaBit = binascii.a2b_uu(errStaByte.encode('ascii'))
        # errStaBit='{:08b}'.format(ord(errStaByte.encode('ascii')))
        for i in range(8):
            if (i == 1):
                errSta.append(int(3))
            else:
                errSta.append(int(errStaBit[i:i + 1]))
    return errSta


if __name__ == "__main__":
    pumpAndPc()
    print(writeHoldingRegisters.__doc__)
