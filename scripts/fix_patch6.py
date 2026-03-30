import sys, re
with open("stegdetect/break_jphide.c", "r") as f: content = f.read()

new_block = """	fprintf(stderr, "Starting extraction of %d bytes...\\n", length);
	FILE *outf = fopen("recovered.img", "wb");
	if (outf) {
		int i, j, b;
		u_char byte_val;
		int v_p = 4;
		u_char *iv2_bytes = (u_char *)iv2;
		
		for (i = 0; i < length; i++) {
			byte_val = 0;
			for(j=0; j<8; j++) {
				b = get_bit();
				if (b < 0) {
					fprintf(stderr, "get_bit() failed\\n");
					break;
				}
				b ^= get_code_bit(1);
				byte_val = (byte_val << 1) | b;
			}
			if (j < 8) {
				fprintf(stderr, "EOF reached early at %d\\n", i);
				break;
			}
			
			if (v_p == 8) {
				BLF_ENC((u_int32_t *)iv2, ctx);
				v_p = 0;
			}
			byte_val ^= iv2_bytes[v_p++];
			
			fwrite(&byte_val, 1, 1, outf);
		}
		fclose(outf);
		fprintf(stderr, "Extracted %d bytes to recovered.img\\n", i);
	} else {
		fprintf(stderr, "Failed to open recovered.img\\n");
	}"""

content = re.sub(r"\tif \(memcmp\(iv2 \+ 4, p \+ 12, 4\)\)\n\t\treturn \(0\);.*?return \(1\);",
                 "\tif (memcmp(iv2 + 4, p + 12, 4))\n\t\treturn (0);\n\n" + new_block + "\n\n\treturn (1);",
                 content, flags=re.DOTALL)

with open("stegdetect/break_jphide.c", "w") as f: f.write(content)