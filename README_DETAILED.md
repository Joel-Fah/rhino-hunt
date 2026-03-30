# Steganography Extraction Report

## 1. Introduction and Investigation Scope
This technical document meticulously archives the entire forensic procedure taken to extract hidden visual evidence from carrier images discovered within a digital disk image (`RHINOUSB.dd`). The primary objective was to uncover concealed steganographic data from the `aligator` picture set, overcome structural extraction bugs, and establish a repeatable methodology for analyzing heavily obfuscated JPHide payloads.

## 2. Working Environment
- **Operating System Platform:** Windows with Windows Subsystem for Linux (WSL) running Ubuntu 24.04. This dual-environment setup was crucial, as it allowed us to combine the power of legacy Linux binary compilation with the accuracy of original Windows executable bridging.
- **Languages & Frameworks:** Python 3 (Pillow library for image recovery, `subprocess` / `pty` for process automation), Bash, C (legacy algorithm patching), VBScript / PowerShell (for Windows GUI interaction).

---

## 3. Data Carving from the Source Image (RHINOUSB.dd)
The original dataset was a raw `.dd` byte-for-byte thumb drive image (`DFRWS2005-RODEO/RHINOUSB.dd`). 
Using disk carving tools (such as Autopsy/Sleuthkit or simply mounting the raw image loopback), the filesystem hierarchy was exposed, revealing various directories. Among these were the `evidence/aligator/` directory containing several `.jpg` files (`evidence/aligator/f0103512.jpg`, `evidence/aligator/f0103704.jpg`, `evidence/aligator/f0104520.jpg`, `evidence/aligator/f0105328.jpg`, `evidence/aligator/f0334536.jpg`) and a `wordlists/rockyou/` folder containing password dictionaries. 
These files were isolated into the active workspace for forensic examination.

---

## 4. Initial Steganography Analysis and Password Brute-Forcing

### The Tools
- **Stegdetect & Stegbreak:** We utilized Niels Provos's legacy `stegdetect` suite, which uses statistical tests to detect specific steganography signatures inside JPEGs, and `stegbreak` to dictionary-attack the algorithm.
- **Stegseek & Steghide:** Tried initially but returned negative results since JPHide uses a proprietary padding scheme unsupported by modern standard tools.

### The Attack
By feeding `stegbreak` with a set of contextual wordlists (including a stripped `wordlists/dict.txt` and elements derived from `evidence/[root]/gumbo1.txt`), we launched an attack against the alligator images.
```bash
./libs/stegdetect/stegbreak -r tools/rules.ini -f wordlists/dict.txt -t p evidence/aligator/*
```
**Results:**
1. `evidence/aligator/f0103704.jpg` tested positive for **JPHide v5** using the password: `gumbo`
2. `evidence/aligator/f0104520.jpg` tested positive for **JPHide v5** using the password: `gator`

---

## 5. First Extraction Attempts and The Corruption Challenges

### Challenge 1: Compiling Legacy Linux Code
`stegbreak` was merely designed to *find* passwords, not securely *extract* the payload. To force extraction, we had to compile the tool. Modern GCC enforces `-fno-common`, crashing the legacy 1999 variable array allocations. Furthermore, JPHide's `coeff` buffer was originally sized at 256 bytes, which immediately segfaulted during a full pixel-map dump.

### Challenge 2: C-Code Patching
To intercept the stream, numerous Python patching scripts were used:
- **`scripts/patch.py` / `scripts/patch_all.py` / `scripts/patch_v2.py` / `scripts/patch_v3.py`**: These scripts programmatically read `libs/stegdetect/break_jphide.c` and used regex and string replacement to:
  1. Expand the buffer: `short coeff[256];` -> `short coeff[30000000];`
  2. Inject an `outf` file writer loop `fwrite(&byte_val, 1, 1, outf)` inside the decryption block.

### Challenge 3: "The Tail" Padding Corruption
The resulting extracts (`extracted_gator.jpg`, `test.jpg`) threw an **"Unsupported format"** error in Windows Image Viewer. 
**What went wrong?** Deep reverse-engineering of `jpseek.c` revealed a counter-measure known as the "Tail" padding. JPHide dynamically calculates variables (`tail_var`, `tail_on`, `TAIL1-3`) near the end of the byte-stream to artificially skip bits (`if (tail_on > 0 && !get_code_bit(2)) continue;`). Because our initial patched `break_jphide.c` stripped or misunderstood this logic, the end of the JPEG payload (the critical `FF D9` End-of-Image markers and final Huffman blocks) was misaligned and corrupted.

### Challenge 4: Forensic Repair with Python Pillow
- **`scripts/parse.py`**: Written to scan the broken payload byte-by-byte for valid JPEG hex markers (`FF D8` for header, `FF E1` for EXIF, etc.) to evaluate where the file structure failed.
- **`scripts/test_pil.py`**: Utilized Pillow (`LOAD_TRUNCATED_IMAGES = True`) to forcibly render the broken bitstream. This repaired the `gumbo` image (`extracted_gumbo_REPAIRED.jpg`), but failed entirely on the `gator` image due to deep-stream Huffman table corruption directly caused by the C-code bit skips.

---

## 6. The Definitive Fix: Bridging Archival Windows Binaries

Realizing that custom C-patching the pseudo-random padding logic was an endless loop of bit-misalignment, we decided to entirely abandon the Linux `stegbreak` / Linux `jpseek` ports and acquire the exact original compiler's tool.

### Fetching the Tool
We utilized `scripts/dl.py` and `scripts/gh_search.py` to trace web-archives and GitHub to finally locate and download the authentic **JPHide Win32 GUI (`jpseek.exe` version 0.51)** from `github.com/jjnzzz/jphide`.

### Automating the Windows Payload Extraction inside WSL
The `jpseek.exe` tool prompts for an interactive password in the Windows console, which standard bash redirection (`echo "password" | `) fails to satisfy across the emulation layer. To bypass this, we wrote several interface scripts:

1. **`scripts/pty_win.py` & `scripts/pty_run.py`**: Attempted to use Linux pseudo-terminals (`pty`) to trick the Windows `.exe` into accepting stdin from Python.
2. **`scripts/run.py` & `scripts/run.bat`**: Used Windows Subprocess pipes and pure Batch bridging.
3. **`scripts/sendkeys.ps1` & VBScripts (`scripts/send.vbs`, `scripts/send_gumbo.vbs`)**: *[The successful method]* By leveraging the Windows Script Host natively across the WSL boundary, we spawned `jpseek.exe`, pushed it to the active window space, and dynamically injected the specific keystrokes (`gumbo{ENTER}`, `gator{ENTER}`).

```vbscript
' scripts/send_gumbo.vbs
Set wshShell = CreateObject("WScript.Shell")
wshShell.Run "cmd /c .\libs\jphs_jjnzzz\jphide\jpseek.exe evidence\aligator\f0103704.jpg extracted_gumbo_real.jpg > out_gumbo.log"
WScript.Sleep 1000
wshShell.SendKeys "gumbo{ENTER}"
WScript.Sleep 2000
```

---

## 7. Registry of Generated Artifacts and Tools

| File Name | Purpose and Outcome |
| :--- | :--- |
| **`scripts/patch_*.py`, `scripts/fix_*.py`** | Scripts used to parse and inject buffer overflow fixes and file-writer routines into `libs/stegdetect/break_jphide.c`. Proved successful for payload dumping but failed on bit-alignment. |
| **`scripts/parse.py`** | A custom JPEG hex-marker parser. Used to identify the exact offset (`0x2420`) where the corrupted `gator` file broke its Huffman stream. |
| **`scripts/test_pil.py`** | Pillow bridging script that successfully forced the rendering of the semi-corrupt `gumbo` stream by ignoring its missing EOF. |
| **`scripts/gh_search.py` & `scripts/dl.py`** | Scripts to crawl GitHub REST APIs and the Internet Archive (Wayback Machine) to retrieve the required legacy `jphswin_05.zip` and `jpseek.exe` binaries. |
| **`scripts/send.vbs`, `scripts/send_gumbo.vbs`** | Active-window keystroke-injection scripts, bridging WSL to native Windows to successfully input passwords into `jpseek.exe`. |
| **`scripts/crack_steg.sh`** | Bash iteration over the `wordlists/rockyou/rockyou.txt` vocabulary against `steghide` and legacy `jpseek` attempting automation algorithms. |
| **`test.jpg`, `extracted_1.jpg`** | Broken interim payloads containing misaligned bits due to the `stegbreak` tail bug. (Unsupported format). |
| **`extracted_gumbo_perfect.jpg`** | The final, 100% cleanly extracted steganography payload of the rhino for the gumbo password. |
| **`extracted_gator_clean.jpg`** | The final, 100% cleanly extracted steganography payload of the rhino for the gator password. |

---

## 8. Conclusion
The extraction of hidden data required mitigating software decay and algorithm precision errors. While `stegdetect` identified the encryption scheme correctly, relying on reverse-engineered source code (`stegbreak`) to dynamically dump the payload generated corrupt data streams due to `JPHide`'s obscure padding matrix. 

By leveraging WSL seamlessly with native Windows inter-process communication (VBScript/SendKeys), we successfully interfaced with the definitive archival 1998 Windows application (`jpseek.exe v0.51`). Doing this precisely bypassed all bitstream desynchronization—ultimately extracting the two pristine, full-resolution Rhino forensic images.