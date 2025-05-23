import os
import argparse
from PIL import Image
import numpy as np

ANIMATIONS_DIR = "animations"
FRAME_SEPARATOR = "--space--"
FRAME_WIDTH = 80
FRAME_HEIGHT = 30

# Плотности символов из оригинального скрипта
CHAR_DENSITIES = {
    ' ': 0.0000, ' ': 0.0000, '¸': 0.0159, '`': 0.0208, '´': 0.0208, '·': 0.0248,
    '.': 0.0249, '¯': 0.0256, '-': 0.0292, '­': 0.0292, '¨': 0.0338, '\'': 0.0391,
    ':': 0.0457, '_': 0.0550, ',': 0.0572, '¬': 0.0584, '~': 0.0725, '^': 0.0726,
    '"': 0.0754, ';': 0.0801, '¡': 0.0819, '=': 0.0841, '°': 0.0901, '!': 0.0909,
    '>': 0.0943, '<': 0.0943, '«': 0.0953, '»': 0.0966, '+': 0.0972, '³': 0.0987,
    '¹': 0.0988, '¿': 0.1026, 'c': 0.1031, '¦': 0.1042, 'r': 0.1051, '/': 0.1054,
    '\\': 0.1055, '²': 0.1078, '?': 0.1100, 'z': 0.1119, '×': 0.1126, '*': 0.1133,
    'v': 0.1151, 'L': 0.1159, 's': 0.1202, 'ç': 0.1207, 'º': 0.1237, 'T': 0.1258,
    'i': 0.1260, '7': 0.1263, '|': 0.1282, 'ª': 0.1283, ')': 0.1300, 'J': 0.1301,
    '(': 0.1302, 'x': 0.1306, 't': 0.1362, 'n': 0.1378, 'u': 0.1381, '}': 0.1395,
    'l': 0.1399, '{': 0.1402, 'C': 0.1403, 'F': 0.1417, 'o': 0.1421, '1': 0.1435,
    '±': 0.1444, 'y': 0.1444, 'Y': 0.1450, '[': 0.1454, 'I': 0.1468, ']': 0.1468,
    '3': 0.1476, 'f': 0.1482, 'j': 0.1485, 'Z': 0.1499, 'e': 0.1525, 'a': 0.1529,
    '5': 0.1537, '2': 0.1546, 'Ç': 0.1551, 'w': 0.1557, 'S': 0.1592, 'Ý': 0.1659,
    'Í': 0.1678, 'Ì': 0.1678, 'E': 0.1688, '£': 0.1707, 'k': 0.1707, 'h': 0.1722,
    '¤': 0.1724, 'P': 0.1725, 'µ': 0.1727, '®': 0.1731, 'à': 0.1737, 'á': 0.1738,
    'V': 0.1776, 'Ï': 0.1786, 'Þ': 0.1794, 'Î': 0.1796, 'q': 0.1798, 'p': 0.1806,
    '6': 0.1808, 'K': 0.1821, 'm': 0.1827, 'U': 0.1831, '9': 0.1833, 'â': 0.1839,
    '4': 0.1855, 'b': 0.1855, 'G': 0.1865, 'ä': 0.1867, 'd': 0.1879, 'É': 0.1897,
    'È': 0.1897, 'ã': 0.1913, 'æ': 0.1930, 'å': 0.1939, '¢': 0.1946, '¥': 0.1984,
    'X': 0.1991, 'A': 0.1993, 'O': 0.1996, 'Ë': 0.2005, '¼': 0.2007, '½': 0.2009,
    'H': 0.2010, 'Ê': 0.2015, 'R': 0.2026, 'Ú': 0.2040, 'Ù': 0.2041, 'D': 0.2113,
    '#': 0.2118, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148,
    '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148,
    '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148,
    '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148,
    '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148,
    '': 0.2148, '': 0.2148, '': 0.2148, '': 0.2148, 'Ü': 0.2148, '¾': 0.2149,
    '8': 0.2154, 'Û': 0.2159, 'ß': 0.2183, '§': 0.2201, 'Á': 0.2202, 'À': 0.2203,
    'Ó': 0.2206, 'Ò': 0.2206, 'Æ': 0.2216, 'N': 0.2216, '0': 0.2231, 'Ð': 0.2264,
    'M': 0.2278, 'B': 0.2279, 'W': 0.2299, 'Ä': 0.2310, 'Ö': 0.2314, 'Â': 0.2321,
    'Ô': 0.2324, '©': 0.2335, '$': 0.2348, 'g': 0.2357, 'Ã': 0.2377, 'Õ': 0.2380,
    'Å': 0.2384, '%': 0.2389, 'Q': 0.2418, '&': 0.2544, 'Ñ': 0.2600, 'Ø': 0.2822,
    '¶': 0.2916, '@': 0.3090
}

def intensity_to_char(intensity):
    """Map intensity (0 to 1) to the closest character by density."""
    closest_char = min(CHAR_DENSITIES.items(), key=lambda x: abs(x[1] - intensity))
    return closest_char[0]

def image_to_ascii(image, width=FRAME_WIDTH, height=FRAME_HEIGHT):
    """Convert an image to ASCII art."""
    # Resize image to desired dimensions
    image = image.resize((width, height), Image.LANCZOS)
    # Convert to grayscale
    image = image.convert('L')
    # Get pixel data as numpy array
    pixels = np.array(image)
    # Normalize pixel intensities to 0-1
    pixels = pixels / 255.0
    # Map intensities to characters
    ascii_frame = [[intensity_to_char(pixels[y][x]) for x in range(width)] for y in range(height)]
    # Convert to list of strings
    ascii_lines = [''.join(row) for row in ascii_frame]
    return ascii_lines

def gif_to_ascii_animation(input_file, output_file):
    """Convert a GIF to ASCII animation."""
    try:
        with Image.open(input_file) as gif:
            frames = []
            try:
                while True:
                    # Convert each frame to ASCII
                    ascii_lines = image_to_ascii(gif)
                    frames.append('\n'.join(ascii_lines))
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass  # End of frames
            
            if not frames:
                print(f"Error: No frames found in '{input_file}'.")
                return
            
            # Save ASCII animation
            if not os.path.exists(ANIMATIONS_DIR):
                os.makedirs(ANIMATIONS_DIR)
            
            output_path = os.path.join(ANIMATIONS_DIR, output_file)
            with open(output_path, "w", encoding='utf-8') as f:
                f.write(FRAME_SEPARATOR.join(frames))
            
            print(f"ASCII animation generated in {output_path}")
            print(f"Run server.py and try: curl http://localhost:8000/{os.path.splitext(output_file)[0]}/")
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"Error processing GIF: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Convert GIF to ASCII animation")
    parser.add_argument('--input', default='input.gif', help="Input GIF file")
    parser.add_argument('--output', default='gif.txt', help="Output ASCII animation file")
    args = parser.parse_args()
    
    gif_to_ascii_animation(args.input, args.output)

if __name__ == "__main__":
    main()