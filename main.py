from machine import UART, Pin
import time
from gb2312 import utf8_gb2312

uart1 = UART(1, baudrate=115200, tx=17, rx=16) # UART1, TX=GPIO17, RX=GPIO16, baudrate=115200


# 发送 TTS 消息的函数
def send_tts_message(message):
    # 将 UTF-8 字符串转换为 GB2312 字节
    print(message)
    font = utf8_gb2312()
    gb2312_bytes = font.str(message)
#     gb2312_bytes = utf8_gb2312(message)
    print(gb2312_bytes)
    
    # 构建要发送的数据包（这里假设了一个简单的协议）
    # 注意：这里的协议可能与你的实际设备要求不符，请根据实际情况调整
    header = bytearray([0xFD, (len(gb2312_bytes) + 2) >> 8, (len(gb2312_bytes) + 2) & 0xFF, 0x01, 0x01])
    packet = header + gb2312_bytes
    
    uart = uart1
    uart.write(packet)
    print(f"Sent on UART: {packet}")
    



def read_data():
    uart = uart1
    if uart.any():
        data = uart.read(uart.any())  # 读取所有可用的数据
        print(f"Received on UART: {data}")
        return data
    return None

if __name__ == "__main__":
    # 示例用法
    try:
        while True:
            
            
            
            # 将字节对象转换回十六进制字符串，并转换为大写
            #hex_string_upper = byte_data.hex().upper()
            data_str = "你好,很高兴为你服务"
            
            send_tts_message(data_str)
            time.sleep(2)
            read_data()
            
            time.sleep(10)  # 等待一秒再读取
            
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        uart1.deinit()  # 清理资源