import re

with open("stegdetect/break_jphide.c", "r") as f:
    text = f.read()

# 1. Array fix
text = re.sub(r"short coeff\[256\];", r"short coeff[30000000];", text)
text = re.sub(r"sizeof\(job->coeff\)/sizeof\(short\)", r"job->bits", text)

# 2. Add tail globals
globals_old = r"""int coef, mode, spos;
int lh, lt, lw, where;
short \*coeff;
int \*lwib, \*lhib;"""

globals_new = r"""int coef, mode, spos;
int lh, lt, lw, where;
short *coeff;
int *lwib, *lhib;

int tail_var = 0;
int tail_on = 0;
#define TAIL1 12000
#define TAIL2 6000
#define TAIL3 3000
"""
text = re.sub(globals_old, globals_new, text)

# 3. Modify get_word to support tail_on (use regex to ignore whitespace)
get_word_old = r"if \(mode > 1 && !get_code_bit\(0\)\)\s*continue;\s*}\s*\*value = y;\s*return \(0\);\s*}\s*}"
get_word_new = r"""if (mode > 1 && !get_code_bit(0))
                                continue;
                }

                if (tail_on > 0 && !get_code_bit(2)) continue;
                if (tail_on > 1 && !get_code_bit(2)) continue;
                if (tail_on > 2 && !get_code_bit(2)) continue;

                *value = y;
                return (0);
        }
}"""
text = re.sub(get_word_old, get_word_new, text)

# 4. Modify get_word to support tail variable updates
lt_update_old = r"if \(ltab\[lt\] < 0\) {\s*return \(1\);\s*}\s*coef = ltab\[lt\];"
lt_update_new = r"""if (ltab[lt] < 0) {
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
text = re.sub(lt_update_old, lt_update_new, text)

# 5. Injection of extraction loop in break_jphide_v5
extract_old = r"if \(memcmp\(iv2 \+ 4, p \+ 12, 4\)\)\s*return \(0\);\s*return \(1\);\s*}"
extract_new = r"""if (memcmp(iv2 + 4, p + 12, 4))
                return (0);

        fprintf(stderr, "Starting extraction of %d bytes...\n", length);
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
                                        fprintf(stderr, "get_bit() failed\n");  
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
                fprintf(stderr, "Extracted %d bytes to recovered.img\n", i);    
        }

        return (1);
}"""
text = re.sub(extract_old, extract_new, text)

with open("stegdetect/break_jphide.c", "w") as f:
    f.write(text)
print("Patch successful!")
