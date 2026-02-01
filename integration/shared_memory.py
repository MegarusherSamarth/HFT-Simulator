# Alternative IPC method
# Shared memory IPC between Python ML strategies and the C++ HFT engine.
# Uses Python's multiprocessing.shared_memory for fast data exchange.

import json
import struct
from multiprocessing import shared_memory

class SharedMemoryIPC:
    def __init__(self, name: str = "hft_shared_mem", size: int = 4096):
        # Initialize shared memory segment.
        # :param name: Shared memory block name (must match C++ side).
        # :param size: Size of the memory block in bytes.
        self.name = name
        self.size = size
        try:
            # Try to attach to existing shared memory
            self.shm = shared_memory.SharedMemory(name = self.name)
            print(f"[IPC] Attached to existing shared memory: {self.name}")
        except FileNotFoundError:
            # Create new shared memory block
            self.shm = shared_memory.SharedMemory(name = self.name, create=True, size=self.size)
            print(f"[IPC] Created new shared memory: {self.name}")
        
    def write_message(self, message: dict):
        # Write a JSON message into shared memory.
        # :param message: Python dict to serialize and store.
        
        data = json.dumps(message).encode("utf-8")
        
        if len(data) > self.size:
            raise ValueError("Message too large for shared memory block")
        
        # Pack length + data
        packed = struct.pack(f"{len(data)}s", data)
        self.shm.buf[:len(packed)] = packed
        print(f"[IPC] Wrote message: {message}")
    
    def read_message(self) -> dict:
        # Read JSON message from shared memory.
        # :return: Python dict parsed from shared memory.
        
        raw = bytes(self.shm.buf[:self.size]).rstrip(b"\x00")
        
        if not raw:
            return {}
        try:
            message = json.loads(raw.decode("utf-8"))
            print(f"[IPC] Read message: {message}")
            return message
        except json.JSONDecodeError:
            print("[ERROR] Failed to decode shared memory contents")
            return {}
    
    def close(self):
        # Close shared memory handle.
        self.shm.close()
        
    def unlink(self):
        # Destroy shared memory block (cleanup).
        self.shm.unlink()

# Example usage
if __name__ == "__main__":
    ipc = SharedMemoryIPC()

    # Write a sample tick
    ipc.write_message({"symbol": "BTCUSDT", "price": 42000.5, "quantity": 0.25})

    # Read back the message
    msg = ipc.read_message()
    print("Message received:", msg)

    # Cleanup
    ipc.close()
    ipc.unlink()