def read_int1(bytes, offset):
    return bytes[offset], 1

def read_int2(bytes, offset):
    return (bytes[offset] & 0xff << 8) | (bytes[offset+1] & 0xff), 2

def read_int4(bytes, offset):
    return (bytes[offset] & 0xff) << 24 | (bytes[offset+1] & 0xff) << 16 | (bytes[offset+2] & 0xff) << 8 | (bytes[offset+3] & 0xff) , 4

def read_string(bytes, offset):
    string_len = bytes[offset]
    return slice(bytes, offset+1, string_len).decode('iso8859-1'), 1 + string_len

# 从offset 开始 读取 len 个
def slice(bytes, offset, len):
    return bytes[offset: offset + len]

def int1(num):
    return [num]

def int2(num):
    return [ (num >> 8 & 0xff), (num & 0xff)]

def int4(num):
    return [(num >> 24 & 0xff), (num >> 16 & 0xff), (num >> 8 & 0xff), (num & 0xff)]

def string(str):
    return int1(len(str)) + list(str.encode('iso8859-1'))

def message(bytes_list):
    # 组合消息体
    message_body_bytes = []
    for bytes in bytes_list:
        message_body_bytes += bytes
    # 加上两字节的消息头
    return int2(len(message_body_bytes)) + message_body_bytes