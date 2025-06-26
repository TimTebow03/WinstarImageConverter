import sys
from PIL import Image
import numpy as np
from pathlib import Path

def ImageToByteArray(image_path):
    try:
        img = Image.open(image_path).convert("L")
        width, height = img.size
        pixel_data = list(img.getdata())
        bit_array = np.array(pixel_data)
        bit_array = 1 - ((bit_array > 127).astype(int))
        bit_array = bit_array.reshape((height, width))
        return bit_array
    except FileNotFoundError:
        print(f"Error: image file was not found at {image_path}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
imageName = sys.argv[1]
#image_path = Path(Rf"C:\Users\4Matt\Documents\AsepriteExports\{imageName}.png")
image_path = Path(Rf"InputFolder\{imageName}.png")
bit_array = ImageToByteArray(image_path)

if bit_array is not None:
    np.savetxt(Rf"OneBitOutput\{imageName}_1_bit.txt", bit_array, fmt="%d", delimiter="")
    valCounter = 0
    hexBox = []
    for z in range(4):

        for i in range(100):
            binaryString = ""
            binaryInt = 0
            
            for j in range(8):
                bit = str(bit_array[j + (z*8)][i])
                binaryString += bit

            binaryString = binaryString[::-1]
            intVal = int(binaryString, 2)
            hexVal = f"0x{intVal:02x}"
            hexBox.append(hexVal)

    hexBox = ["0x" + val[2:].upper() for val in hexBox]
    
with open(Rf"OutputFolder\{imageName}_Hex.txt", "w") as f:
    for i in range(0, len(hexBox), 8):
        line_items = hexBox[i:i+8]
        line = ",".join(line_items)

        is_last_line = (i + 8 >= len(hexBox))
        
        if is_last_line:
            f.write(line)
        else:
            f.write(line + ",\n")