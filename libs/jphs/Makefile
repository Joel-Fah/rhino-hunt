HDOBJECTS = jphide.o bf.o
SKOBJECTS = jpseek.o bf.o

CFLAGS_COMMON = -O2 -m32

JP_CFLAGS = $(CFLAGS_COMMON) -DBF_BE -I./jpeg-8a
BF_CFLAGS = $(CFLAGS_COMMON) -DBF_BE

all: jphide jpseek

jphide: $(HDOBJECTS)
	gcc -m32 -o jphide $(HDOBJECTS) jpeg-8a/.libs/libjpeg.a

jpseek: $(SKOBJECTS)
	gcc -m32 -o jpseek $(SKOBJECTS) jpeg-8a/.libs/libjpeg.a

bf.o:
	gcc -m32 $(BF_CFLAGS) -c bf.c
jphide.o:
	gcc -m32 $(JP_CFLAGS) -c jphide.c
jpseek.o:
	gcc -m32 $(JP_CFLAGS) -c jpseek.c

clean:
	rm -f jphide jpseek $(HDOBJECTS) $(SKOBJECTS)
