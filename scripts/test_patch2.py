import sys

def run():
    with open('stegdetect/break_jphide.c', 'r') as f:
        content = f.read()

    old_block = '''        memcpy(iv2, iv, sizeof(iv2));
        BLF_ENC((u_int32_t *)iv2, ctx);

        if (memcmp(iv2 + 4, p + 12, 4))
                return (0);

        return (1);'''
    old_block = old_block.replace("        ", "\t")

    new_block = '''        memcpy(iv2, iv, sizeof(iv2));
        BLF_ENC((u_int32_t *)iv2, ctx);

        if (memcmp(iv2 + 4, p + 12, 4))
                return (0);

        FILE *outf = fopen("recovered.img", "wb");
        if (outf) {
                int i;
                u_char v;
                int v_p = 4;
                for (i = 0; i < length; i++) {
                        if (break_jphide_getbytes(&v, 1) == -1) break;
                        v ^= iv2[v_p++];
                        if (v_p == 8) {
                                BLF_ENC((u_int32_t *)iv2, ctx);
                                v_p = 0;
                        }
                        fwrite(&v, 1, 1, outf);
                }
                fclose(outf);
                fprintf(stderr, "Extracted %d bytes to recovered.img\\n", i);
        }

        return (1);'''
    new_block = new_block.replace("        ", "\t")

    if old_block in content:
        content = content.replace(old_block, new_block)
        with open('stegdetect/break_jphide.c', 'w') as f:
            f.write(content)
        print("Patched correctly!")
    else:
        print("Not found!")

run()
