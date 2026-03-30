#!/bin/bash
for img in aligator/*.jpg; do
    echo "======================================"
    echo "Running stegseek on $img"
    stegseek -sf "$img" -wl rockyou/rockyou.txt -xf "${img}_steg_out.bin"
done
