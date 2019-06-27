import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

LOGGER = modbus_tk.utils.create_logger("console")

def master():
    """"创建modbus主机监听从机，获取从机保存寄存器的数据"""
    try:
        MASTER = modbus_tcp.TcpMaster(host="192.168.123.51", port=1100)
        MASTER.set_timeout(50)
        feedback = MASTER.execute(1, cst.READ_HOLDING_REGISTERS, 0, 47)

        print(feedback);
    except Exception as e:
        print("---异常---：", e)
if __name__ == "__main__":
    master()