import pty
import os
import sys

pid, fd = pty.fork()

if pid == 0:
    os.execlp('./jphs/jpseek', 'jpseek', 'aligator/f0104520.jpg', 'extracted_gator_pty.jpg')
else:
    output = b''
    try:
        while True:
            data = os.read(fd, 1024)
            output += data
            if b'Passphrase:' in data:
                os.write(fd, b'gator\n')
                break
    except OSError:
        pass
    os.waitpid(pid, 0)
    print("Done")
