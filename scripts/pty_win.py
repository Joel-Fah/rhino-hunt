import pty
import os
import time
import sys

pid, fd = pty.fork()
if pid == 0:
    os.execlp('./jphs_jjnzzz/jphide/jpseek.exe', 'jpseek.exe', 'aligator/f0104520.jpg', 'extracted_gator_real.jpg')
else:
    output = b''
    try:
        while True:
            data = os.read(fd, 1024)
            output += data
            if b'Passphrase:' in data:
                time.sleep(0.1)
                os.write(fd, b'gator\r\n')
                break
    except OSError:
        pass
    os.waitpid(pid, 0)
    print('Done')
