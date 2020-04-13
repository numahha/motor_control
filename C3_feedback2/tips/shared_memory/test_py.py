import sysv_ipc

# Create shared memory object
#memory = sysv_ipc.SharedMemory(839254863)
key = sysv_ipc.ftok("./key", 50)
memory = sysv_ipc.SharedMemory(key)

memory_value = memory.read()

print(memory_value)
import struct
print(struct.unpack('d',memory_value)[0])


memory.write(struct.pack('d',1.234567890123456789))
memory_value = memory.read()
print(memory_value)
print(struct.unpack('d',memory_value)[0])
