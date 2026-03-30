# Digital Forensics Investigation: The Rhino Hunt Challenge

## Overall Project Overview
This repository contains the full methodology, documentation, scripts, and findings for resolving the **Rhino Hunt Challenge**, a comprehensive digital forensics and steganography exercise. The focus of the investigation spans disk image data carving, network packet analysis, and deep-level password brute-forcing and steganographic extraction.

Our mission primarily centered on uncovering hidden "rhino" images concealed within a complex set of carrier items—including `dd` system images, intercepted `.pcap`/`.log` packet captures, and password-protected zip archives.

## Core Forensics Phases

### Phase 1: Disk Image Data Carving
In the first phase of the investigation, we analyzed the raw disk image `RHINOUSB.dd` to uncover hidden and deleted files.
- We utilized **Autopsy** to investigate the contents of the `dd` file and ran deep Carver ingests (using *PhotoRec*). 
- We extracted the hidden `crocodile` and `aligator` `.jpg` images from the unallocated space. 

### Phase 2: Network Forensics & PCAP Analysis 
Secondarily, the challenge required us to act as a "digital microscope" on several network captures (`rhino.log`). 
- Using **Wireshark**, we filtered and isolated unencrypted FTP and Telnet sessions. 
- By following the TCP streams and viewing the raw hexadecimal data, we carved out several images directly from the network packets, including `rhino1.jpg` and `rhino3.jpg`.
- We additionally recovered an encrypted file, `contraband.zip`, sent over the intercepted traffic.

### Phase 3: Archive Brute-Forcing (`contraband.zip`)
The intercepted `contraband.zip` was subjected to an offline dictionary attack to retrieve its internal payloads.
- We utilized Linux tool `fcrackzip` paired with the standard `rockyou.txt` dictionary. 
- The targeted dictionary attack quickly cracked the passkey (which was `monkey`) and extracted a hidden `rhino2.jpg` file.
- **Detailed Report:** Please review our [BRUTE_FORCE_REPORT.md](BRUTE_FORCE_REPORT.md) for step-by-step methodologies surrounding the ZIP encryption attack.

### Phase 4: Defeating Legacy Steganography 
For the `.jpg` files carved initially (`f0103704.jpg` and `f0104520.jpg`), we recognized the presence of hidden JPHide and Steghide payloads utilizing passwords recovered from network traffic (`gumbo` and `gator`). 
- **Legacy Roadblocks:** Modern tools could check the files but could not structurally extract the hidden rhinos without corrupting the JPEG Huffman tables. We had to mitigate severe software decay from a 1999 Linux application (`stegdetect/stegbreak`). 
- **The Solution:** We successfully circumvented the bitstream desynchronization errors by bridging the native legacy Windows binary `jpseek.exe v0.51` to WSL (Ubuntu 24.04) executing Python and VBScript interface scripts to successfully render out the clean image payloads (`extracted_gumbo_perfect.jpg` and `extracted_gator_clean.jpg`).
- **Detailed Report:** Please explore the extensive [README_DETAILED.md](README_DETAILED.md) to delve into the custom Python `.dll` patching and VBScript inter-process communication built inside WSL to safely fetch the images.

---
## Tooling Environment
* **Platform:** Windows (Host) and Windows Subsystem for Linux (WSL on Ubuntu 24.04) 
* **Primary Applications:** FTK Imager, Autopsy, Wireshark  
* **CLI/Hacking Arsenal:** `stegdetect`, `stegbreak`, `steghide`, `fcrackzip`
* **Custom Patching Tooling:** Python 3 (Pillow), `sendkeys.ps1`, VBScript 

## File Directory Reference
* `/evidence` Space for network caps (`.pcap`), base images (`dd`), and carved images.
* `/libs` Compilable binaries and legacy repositories (`stegdetect`, `jpseek.c`).
* `/scripts` Custom Python patching syntax and automated `VBScript` keys.
* `/wordlists` Dictionaries utilized for the attack (`rockyou.txt` & `dict.txt`).

---

## Conclusion & Key Observations

### Conclusion
The Rhino Hunt challenge effectively demonstrated the necessity for a multi-disciplinary approach in digital forensics. What began as a standard disk image carve escalated into network packet reconstruction, archive brute-forcing, and ultimately fighting legacy code rot to extract hidden steganographic data. By the end of the investigation, we successfully recovered all the hidden rhino images from across the network traffic, the encrypted zip file, and the heavily obfuscated JPEGs.

### Key Observations
1. **The Vulnerability of Cleartext Protocols:** Discovering credentials and entire files passed via Telnet and unencrypted FTP highlights the critical security flaws of legacy network protocols. The passwords intercepted here (`gumbo`, `gator`) became the linchpin for the rest of an otherwise highly secure steganographic attack.
2. **Software Decay is a Real Forensic Hurdle:** Modern forensic tools are fantastic, but when dealing with niche or older algorithms like JPHide v5, modern compilers and environments (like GCC 10+) can outright fail. The investigator must be prepared to patch C code, manipulate dependencies, or find creative ways to run 20+ year-old binaries safely.
3. **Cross-Environment Synchronization (WSL + Win32):** Relying solely on a Linux terminal or solely on a Windows GUI was insufficient for the final extraction. Bridging WSL bash environments with native Windows GUI automation (VBScript/SendKeys) proved to be an invaluable technique for controlling interactive legacy extraction tools without sacrificing the power of Linux forensic pipelines.