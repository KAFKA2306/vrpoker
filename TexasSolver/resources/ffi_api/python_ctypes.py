import ctypes
import os
libname = os.path.abspath(os.path.join(os.getcwd(), "api.dll"))
c_lib = ctypes.CDLL(libname)
c_lib.api.restype = ctypes.c_int
c_lib.api.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
input_file = b"resources/text/commandline_sample_input.txt"
resource_dir = bytes("./resources", 'utf-8')
result = c_lib.api(input_file, resource_dir, b"holdem")
