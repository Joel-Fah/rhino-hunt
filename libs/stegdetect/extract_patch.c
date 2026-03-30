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
                fprintf(stderr, "Extracted %d bytes to recovered.img\n", i);
        }
