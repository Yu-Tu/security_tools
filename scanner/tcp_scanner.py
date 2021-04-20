import socket
import sys


def connect(ip, port):
    """
    using socket connect to judge if the target port open
    :param ip: str
    :param port: int
    :return: None unless Exception
    """
    socket.setdefaulttimeout(0.1)
    connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPV4 且使用流式socket
    connect_socket.connect((ip, port))


def get_ip_list(ipaddress):
    """
    parse the ipaddress like 10.0.0.0/24, 10.0.0.*, 10.0.0.1-10
    :param ipaddress: 
    :return: ip list
    """
    ip_list = []
    ipaddress = ipaddress.split(',')
    for ip in ipaddress:
        if '*' in ip:
            ip_left = ip[:ip.rfind('.')]
            for i in range(256):
                ip_list.append(ip_left + '.' + str(i))
        elif '/' in ip:
            ip = ip[:ip.rfind('/')]
            ip_list.append(ip)
        elif '-' in ip:
            ip_pointer = ip.rfind('.')
            ip_left = ip[:ip_pointer]
            ip_right = ip[ip_pointer + 1:]
            low = ip_right.split('-')[0]
            high = ip_right.split('-')[1]
            for i in range(int(low), int(high) + 1):
                ip_list.append(ip_left + '.' + str(i))
        else:
            ip_list.append(ip)
    return ip_list


# ip = '192.168.2.45/24' 
# print(get_ip_list(ip))                                  

def get_port_list(port):
    port_list = []
    portlist = port.split(',')
    for port in portlist:
        if '-' in port:
            port_pointer = port.split('-')
            port_left = port[:port_pointer]
            port_right = port[port_pointer:]
            for i in range(int(port_left), int(port_right)):
                port_list.append(i)
        port_list.append(int(port))
    return port_list


if __name__ == '__main__':
    try:
        if len(sys.argv) != 3:
            raise Exception('***Error: tcp scanner need three argvs!!!')
        ip_list = get_ip_list(sys.argv[1])
        port_list = get_port_list(sys.argv[2])
        for ip in ip_list:
            for port in port_list:
                try:
                    connect(ip, port)
                    print(f'ip:{ip} port:{port} is open')
                except Exception as ex:
                    continue
    except Exception as ex:
        print(ex)
