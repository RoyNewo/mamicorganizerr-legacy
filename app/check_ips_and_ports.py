#!/usr/bin/env python
import socket
from multiprocessing import Process, Queue
import time
import argparse

"""
Tools to scan network from python.
Mostly taken from stack overflow and mixed together.

Author: Sammy Pfeiffer <Sammy.Pfeiffer at student.uts.edu.au>
"""


def check_server(address, port, queue):
    """
    Check an IP and port for it to be open, store result in queue.
    Based on https://stackoverflow.com/a/32382603
    """
    # Create a TCP socket
    s = socket.socket()
    try:
        s.connect((address, port))
        # print("Connection open to %s on port %s" % (address, port))
        queue.put((True, address, port))
    except socket.error as e:
        # print("Connection to %s on port %s failed: %s" % (address, port, e))
        queue.put((False, address, port))


def get_own_ip():
    """
    Get the own IP, even without internet connection.
    From https://stackoverflow.com/a/1267524
    """
    return ((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])


def check_subnet_for_open_port(subnet, port, timeout=3.0):
    """
    Check the subnet for open port IPs.
    :param subnet str: Subnet as "192.168.1".
    :param port int: Port as 9559.

    :returns [str]: List of IPs with port open found.
    """
    q = Queue()
    processes = []
    for i in range(1, 255):
        ip = subnet + '.' + str(i)
        # print("Checking ip: " + str(ip))
        p = Process(target=check_server, args=[ip, port, q])
        processes.append(p)
        p.start()
    # Give a bit of time...
    time.sleep(timeout)

    found_ips = []
    for idx, p in enumerate(processes):
        # If not finished in the timeout, kill the process
        if p.exitcode is None:
            p.terminate()
        else:
            # If finished check if the port was open
            open_ip, address, port = q.get()
            if open_ip:
                found_ips.append(address)

    #  Cleanup processes
    for idx, p in enumerate(processes):
        p.join()

    return found_ips


def check_own_subnet_for_open_port(port, timeout=3.0):
    """
    Check our own subnet for open port.
    """
    own_ip = get_own_ip()
    print("Got own ip: " + str(own_ip))
    ip_split = own_ip.split('.')
    subnet = ip_split[:-1]
    subnetstr = '.'.join(subnet)
    return check_subnet_for_open_port(subnetstr, port)


def check_naoqi_port():
    """
    Check on our local network for naoqi port open IPs (9559).
    """
    return check_own_subnet_for_open_port(9559)


def check_ROS_master_port():
    """
    Check on our local network for ROS master port open IPs (11311).
    """
    return check_own_subnet_for_open_port(11311)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("subnet",
                        help="subnet to scan for port",
                        type=str)
    parser.add_argument("port",
                        help="port number to scan in your local network",
                        type=int)
    args = parser.parse_args()
    print(check_subnet_for_open_port(args.subnet, args.port))
