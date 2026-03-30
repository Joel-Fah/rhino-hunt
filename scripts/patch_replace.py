import os

with open("stegdetect/break_jphide.c", "r") as f:
    text = f.read()

text = text.replace("short coeff[256];", "short coeff[30000000];")
text = text.replace("sizeof(job->coeff)/sizeof(short)", "job->bits")

globals_old = """int coef, mode, spos;
int lh, lt, lw, where;
short *coeff;
int *lwib, *lhib;"""

globals_new = """int coef, mode, spos;
int lh, lt, lw, where;
short *coeff;
int *lwib, *lhib;

int tail_var = 0;
int tail_on = 0;
#define TAIL1 12000
#define TAIL2 6000
#define TAIL3 3000
"""
text = text.replace(globals_old, globals_new)


get_word_old = """                        if (mode > 1 && !get_code_bit(0))
                                continue;
                }

                *value = y;
                return (0);
        }
}"""

get_word_new = """                        if (mode > 1 && !get_code_bit(0))
                                continue;
                }

                if (tail_on > 0 && !get_code_bit(2)) continue;
                if (tail_on > 1 && !get_code_bit(2)) continue;
                if (tail_on > 2 && !get_code_bit(2)) continue;

                *value = y;
                return (0);
        }
}"""
text = text.replace(get_word_old, get_word_new)


lt_update_old = """                                if (ltab[lt] < 0) {
                                        return (1);
                                }

                                coef = ltab[lt];"""

lt_update_new = """                                if (ltab[lt] < 0) {
                                        return (1);
                                }

                                if (tail_var < 0) {
                                        if (tail_on == 2) {
                                                tail_on = 3;
                                                tail_var = 999999;
                                        }
                                        if (tail_on == 1) {
                                                tail_on = 2;
                                                tail_var = TAIL3;
                                        }
                                        if (tail_on == 0) {
                                                tail_on = 1;
                                                tail_var = TAIL2;
                                        }
                                }

                                coef = ltab[lt];"""
text = text.replace(lt_update_old, lt_update_new)


extract_old = """        if (memcmp(iv2 + 4, p + 12, 4))
                return (0);

        return (1);
}"""

extract_new = """        if (memcmp(iv2 + 4, p + 12, 4))
                return (0);

        fprintf(stderr, "Starting extraction of %d bytes...\\n", length);
        tail_var = length * 8 - TAIL1;
        tail_on = 0;
        
        FILE *outf = fopen("recovered.img", "wb");
        if (outf) {
                int i, j, b;
                u_char byte_val;

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
                                tail_var--;
                        }
                        if (j < 8) break;
                        fwrite(&byte_val, 1, 1, outf);
                }
                fclose(outf);
                fprintf(stderr, "Extracted %d bytes to recovered.img\\n", i);    
        }

        return (1);
}"""
text = text.replace(extract_old, extract_new)

with open("stegdetect/break_jphide.c", "w") as f:
    f.write(text)
print("done")
