import sys
from pathlib import Path

def b2i(b):
    return int.from_bytes(b, byteorder="little")

def b2s(b):
    return str(b2i(b))

f = open(sys.argv[1], "rb")

path = Path(sys.argv[1].rstrip(".dat"))
path.mkdir(parents=True, exist_ok=True)

piece_size = 4096

sign = f.read(0x0C)

filenames = []
index = []

if sign.decode() == "GAMEDAT PAC2":
    nbfile = b2i(f.read(0x04))
    print("Nb file : " + str(nbfile))

    for i in range(0, nbfile):
        filename = f.read(0x20)
        filenames.append(path / (filename.decode().rstrip('\x00')))
    
    for i in range(0, nbfile):
        offset = b2i(f.read(0x04))
        size = b2i(f.read(0x04))
        index.append((offset, size))
    
    
    for i in range(0, nbfile):
        print("Extracting " + str(filenames[i]), flush=True)
        outfile = open(filenames[i], "wb")
        remaining = index[i][1]

        while remaining > 0:
            if remaining > piece_size:
                piece = f.read(piece_size)
            else:
                piece = f.read(remaining)

            outfile.write(piece)
            remaining = remaining - len(piece)
        
        outfile.close()




f.close()
