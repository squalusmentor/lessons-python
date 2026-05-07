import ctypes
import ctypes.wintypes
k = ctypes.windll.kernel32
k.VirtualAlloc.restype = ctypes.c_void_p

code = open('calc.bin', 'rb').read()  # выделение памяти под инструкцию
a = k.VirtualAlloc(None, len(code), 0x3000, 0x40)
ctypes.memmove(a, code, len(code))  # занести инструкцию в память
f = ctypes.CFUNCTYPE(ctypes.c_int)(a)
print('Результат:', f())
k.VirtualFree.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.wintypes.DWORD]
k.VirtualFree(a, 0, 0x8000)  # очистка памяти
