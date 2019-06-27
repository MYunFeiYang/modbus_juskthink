import sys
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
LOGGER = modbus_tk.utils.create_logger("console")

if __name__ == "__main__":
    try:
        #连接从机地址,这里要注意端口号和IP与从机一致
        MASTER = modbus_tcp.TcpMaster(host="127.0.0.1", port=1100)
        MASTER.set_timeout(50)
        LOGGER.info("connected")
        #读取从机1的0-4保持寄存器
        LOGGER.info(MASTER.execute(1, cst.READ_HOLDING_REGISTERS, 0, 4))
        #读取从机1的4-14保持寄存器，因为寄存器独立分块了，所以不能直接连通读取，强行结果是会出现数据越界
        LOGGER.info(MASTER.execute(1, cst.READ_HOLDING_REGISTERS, 4, 14))
        # 需要按照execute格式
        LOGGER.info(MASTER.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0, output_value=[0, 1, 2]))
        LOGGER.info(MASTER.execute(1, cst.READ_HOLDING_REGISTERS, 0, 4))

        LOGGER.info(MASTER.execute(2, cst.READ_COILS, 0, 8))
        LOGGER.info(MASTER.execute(2, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 0, 0, 0, 1]))
        LOGGER.info(MASTER.execute(2, cst.READ_COILS, 0, 8))
        LOGGER.info(MASTER.execute(2, cst.READ_HOLDING_REGISTERS, 0, 4))
        # 线圈和寄存器地址不是同一区块的
    except Exception as e:
        print("---异常---：", e)
