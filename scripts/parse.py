def parse_jpeg(filename):
    data = open(filename, 'rb').read()
    idx = 0
    while idx < min(len(data), 1000000):
        if data[idx] == 0xff:
            marker = data[idx+1]
            if marker != 0x00 and marker != 0xff:
                print(f'Marker: {hex(marker)} at {idx}')
                if marker not in (0xd8, 0xd9, 0x01, 0xd0, 0xd1, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7):
                    length = (data[idx+2] << 8) + data[idx+3]
                    print(f'Length: {length}')
                    idx += length + 2
                    continue
        idx += 1

parse_jpeg("test.jpg")
