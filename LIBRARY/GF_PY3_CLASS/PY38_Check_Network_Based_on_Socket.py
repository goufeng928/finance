# GF_PY3_CLASS/PY38_Check_Network_Based_on_Socket.py
# Create by GF 2025-09-19 16:53

import socket
import sys

# ##################################################

class PY38_Check_Network_Based_on_Socket():

    # Examples (Check Host Port):
    # >>> Network_Check = PY38_Check_Network_Based_on_Socket()
    # >>> Network_Check.Check_Host_and_Port(Host = "8.8.8.8", Port = 53)
    # [DEBUG] Cheking: Connecting to 8.8.8.8:53
    # [DEBUG] Cheking: Connecting to 8.8.8.8:53, Success!
    # 1
    # >>> Network_Check.Check_Host_and_Port(Host = "127.0.0.1", Port = 5432)
    # [DEBUG] Cheking: Connecting to 127.0.0.1:5432
    # [DEBUG] Cheking: Connecting to 127.0.0.1:5432, Success!
    # 1
    # >>> Network_Check.Check_Host_and_Port(Host = "127.0.0.1", Port = 3306)
    # [DEBUG] Cheking: Connecting to 127.0.0.1:3306
    # [DEBUG] Cheking: Connecting to 127.0.0.1:3306, Failure!
    # 0

    def Check_Host_and_Port(self, Host = "8.8.8.8", Port = 53, Timeout = 3) -> int:

        try:
            sys.stdout.write(f"[DEBUG] Cheking: Connecting to {Host}:{Port}\n")
            # ......................................
            socket.setdefaulttimeout(Timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((Host, Port))
            # ......................................
            sys.stdout.write(f"[DEBUG] Cheking: Connecting to {Host}:{Port}, Success!\n")
            return 1
        except socket.error as e:
            sys.stdout.write(f"[DEBUG] Cheking: Connecting to {Host}:{Port}, Failure!\n")
            return 0

# EOF Signed by GF.
