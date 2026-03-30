import sys

def run():
    with open('stegdetect/break_jphide.c', 'r') as f:
        content = f.read()

    # The current patch block:
    old_block = '''        fprintf(stderr, "Starting extraction of %d bytes...\\n", length);
        FILE *outf = fopen("recovered.img", "wb");
        if (outf) {
                int i;
                u_char v;
                int v_p = 4;
                for (i = 0; i < length; i++) {
                        if (break_jphide_getbytes(&v, 1) == -1) {
                                fprintf(stderr, "EOF reached early at %d\\n", i);
                                break;
                        }
                        v ^= iv2[v_p++];
                        if (v_p == 8) {
                                BLF_ENC((u_int32_t *)iv2, ctx);
                                v_p = 0;
                        }
                        fwrite(&v, 1, 1, outf);
                }
                fclose(outf);
                fprintf(stderr, "Extracted %d bytes to recovered.img\\n", i);
        } else {
                fprintf(stderr, "Failed to open recovered.img\\n");
        }'''
    old_block = old_block.replace("        ", "\t")

    new_block = '''        fprintf(stderr, "Starting extraction of %d bytes...\\n", length);
        FILE *outf = fopen("recovered.img", "wb");
        if (outf) {
                int i, j, b;
                u_char v;
                int v_p = 4;
                for (i = 0; i < length; i++) {
                        v = 0;
                        for(j=0; j<8; j++) {
                                if ((b = get_bit()) < 0) break;
                                b ^= get_code_bit(1);
                                v = (v << 1) | b;
                        }
                        if (j < 8) {
                                fprintf(stderr, "EOF reached early at %d\\n", i);
                                break;
                        }
                        v ^= iv2[v_p++];
                        if (v_p == 8) {
                                BLF_ENC((u_int32_t *)iv2, ctx);
                                v_p = 0;
                        }
                        fwrite(&v, 1, 1, outf);
                }
                fclose(outf);
                fprintf(stderr, "Extracted %d bytes to recovered.img\\n", i);
        } else {
                fprintf(stderr, "Failed to open recovered.img\\n");
        }'''
    new_block = new_block.replace("        ", "\t")

    if old_block in content:
        content = content.replace(old_block, new_block)
        with open('stegdetect/break_jphide.c', 'w') as f:
            f.write(content)
        print("Patched better!")
    else:
        print("Not found")

run()
