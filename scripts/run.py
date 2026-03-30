import subprocess
import time

p = subprocess.Popen(
    ['./jphs_jjnzzz/jphide/jpseek.exe', 'aligator/f0104520.jpg', 'extracted_gator_real.jpg'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

out, err = p.communicate(b'gator\r\n')
print(out.decode('ascii', errors='ignore'))
print(err.decode('ascii', errors='ignore'))
