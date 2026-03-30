with open("stegdetect/break_jphide.c", "r") as f: content = f.read()

new_block = r"""	fprintf(stderr, "Starting extraction of %d bytes...\n", length);
	FILE *outf = fopen("recovered.img", "wb");
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
				
				b ^= get_code_bit(1);
				byte_val = (byte_val << 1) | b;
			}
			if (j < 8) break;
			fwrite(&byte_val, 1, 1, outf);
		}
		fclose(outf);
		fprintf(stderr, "Extracted %d bytes to recovered.img\n", i);
	}

	return (1);
}"""

old_block = r"""	fprintf(stderr, "Starting extraction of %d bytes...\n", length);
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

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("stegdetect/break_jphide.c", "w") as f: f.write(content)
else:
    print("Cannot find old_block")
