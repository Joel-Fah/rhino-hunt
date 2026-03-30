with open("stegdetect/break_jphide.c", "r") as f: content = f.read()

content = content.replace("short coeff[256];", "short coeff[4000000];")
content = content.replace("sizeof(job->coeff)/sizeof(short)", "job->bits")

new_block = r"""	fprintf(stderr, "Starting extraction of %d bytes...\n", length);
	FILE *outf = fopen("raw_bits.bin", "wb");
	if (outf) {
		int i, j, b;
		u_char byte_val;
		
		for (i = 0; i < length; i++) {
			byte_val = 0;
			for(j=0; j<8; j++) {
				b = get_bit();
				if (b < 0) {
					fprintf(stderr, "get_bit() failed\n");
					break;
				}
				
				byte_val = (byte_val << 1) | b;
			}
			if (j < 8) break;
			fwrite(&byte_val, 1, 1, outf);
		}
		fclose(outf);
		fprintf(stderr, "Extracted %d RAW bytes\n", i);
	}

	return (1);
}"""

old_block = "\tif (memcmp(iv2 + 4, p + 12, 4))\n\t\treturn (0);\n\n\treturn (1);\n}"
target_block = "\tif (memcmp(iv2 + 4, p + 12, 4))\n\t\treturn (0);\n\n" + new_block

if old_block in content:
    content = content.replace(old_block, target_block)
    with open("stegdetect/break_jphide.c", "w") as f: f.write(content)
else:
    print("Cannot find old_block")
