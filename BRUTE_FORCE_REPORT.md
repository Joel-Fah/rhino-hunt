# Digital Forensics Report: Brute Forcing contraband.zip

## Executive Summary
This report details the forensic investigation, challenges encountered, and methodologies employed to successfully brute-force the password of the encrypted archive `contraband.zip`.

## Working Environment & Resources
- **OS Environment:** Windows Subsystem for Linux (WSL) running Ubuntu 24.04.
- **Forensic Tools Utilized:** 
  - `fcrackzip` (a fast password cracker).
  - Wordlists: `rockyou.txt`.

## Evidences Found
1. **Encrypted Target (The Contraband Archive):**
   - **File:** `contraband.zip`
   - **Encryption Algorithm:** Standard Zip Encryption
   - **Password:** `monkey`
   - **Result:** Successfully extracted the secret documents inside the ZIP archive using an offline dictionary attack.

## Methodology & Obstacles

### Challenge 1: Brute Forcing the Password
We successfully brute-forced the target zip using a targeted dictionary attack rather than manually formatting checksum hashes.
We ran `fcrackzip` in conjunction with the well-known `rockyou.txt` wordlist to guess the contents.

The exact command evaluated was:
`fcrackzip -v -D -u -p wordlists/rockyou/rockyou.txt evidence/contraband.zip`

**Breakdown of Flags:**
- `-v`: Verbose output to track operations.
- `-D`: Use a dictionary attack instead of pure character pattern generation.
- `-u`: Weed out false positives by verifying it using `unzip`.
- `-p`: Supply the path to the text file of dictionary terms.

### Final Verification
Running the command returned almost identical matches rapidly, declaring: `PASSWORD FOUND!!!!: pw == monkey`

Executing the standard `unzip -P monkey evidence/contraband.zip` command perfectly decrypted the archive payload (`rhino2.jpg`). We verified the integrity of the extracted files via checksum comparisons. 

---
**Investigation Concluded Successfully.** The targeted wordlist attack rapidly defeated the ZIP encryption algorithm with no intermediate hash patching required.