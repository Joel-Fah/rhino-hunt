import re

with open("stegdetect/break_jphide.c", "r") as f:
    text = f.read()

get_word_old = r"""                }

                *value = y;
                return (0);
        }
}"""

get_word_new = r"""                }

                if (tail_on > 0 && !get_code_bit(2)) continue;
                if (tail_on > 1 && !get_code_bit(2)) continue;
                if (tail_on > 2 && !get_code_bit(2)) continue;

                *value = y;
                return (0);
        }
}"""

if get_word_old in text:
    text = text.replace(get_word_old, get_word_new)
else:
    print("Cannot find get_word_old")

init_old = r"""int coef, mode, spos;
int lh, lt, lw, where;
short *coeff;
int *lwib, *lhib;"""

init_new = r"""int coef, mode, spos;
int lh, lt, lw, where;
short *coeff;
int *lwib, *lhib;
int tail_var = 0;
int tail_on = 0;
#define TAIL1 12000
#define TAIL2 6000
#define TAIL3 3000
"""

if init_old in text:
    text = text.replace(init_old, init_new)
else:
    print("Cannot find init_old")

lt_update_old = r"""                                if (ltab[lt] < 0) {
                                        return (1);
                                }

                                coef = ltab[lt];"""

lt_update_new = r"""                                if (ltab[lt] < 0) {
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

if lt_update_old in text:
    text = text.replace(lt_update_old, lt_update_new)
else:
    print("Cannot find lt_update_old")

extract_old = r"""        fprintf(stderr, "Starting extraction of %d bytes...\n", length);
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
        }"""

extract_new = r"""        fprintf(stderr, "Starting extraction of %d bytes...\n", length);
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
        }"""

if extract_old in text:
    text = text.replace(extract_old, extract_new)
else:
    print("Cannot find extract_old")

open("stegdetect/break_jphide.c", "w").write(text)
print("done")
