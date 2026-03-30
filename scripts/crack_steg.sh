#!/bin/bash

# Clean wordlist just in case
dos2unix rockyou/rockyou_alt.txt 2>/dev/null

for img in aligator/*.jpg; do
    echo "Testing steghide on $img"
    while read -r p; do
        if steghide extract -sf "$img" -p "$p" -xf "${img}_steg_out.bin" -f &>/dev/null; then
            echo "----> Found steghide match for $img! Password: $p"
            break
        fi
    done < rockyou/rockyou_alt.txt
done

for img in aligator/*.jpg; do
    echo "Testing jpseek on $img"
    while read -r p; do
        export JP_PASS="$p"
        if ./jphs/jpseek "$img" "${img}_jp_out.bin" &>/dev/null; then
            if [ -s "${img}_jp_out.bin" ]; then
                echo "----> Found jphide match for $img! Password: $p"
                break
            fi
        fi
    done < rockyou/rockyou_alt.txt
done
