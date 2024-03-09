import re
import struct

def find_and_extract(pattern, data):
    matches = re.finditer(pattern, data)
    result = []

    for match in matches:
        start = match.start()
        if start >= 5:  # Ensure there are at least 5 bytes before the pattern
            extracted_bytes = data[start - 5:start]
            result.append(extracted_bytes)

    return result

def main():
    pattern_to_search = b'\x28\x02\x00\x00\x06'  # The hex pattern to search for
    file_path = '400000_Slayed.sample1-cleaned'  # Replace with the path to your binary file

    with open(file_path, 'rb') as file:
        binary_data = file.read()

    extracted_data = find_and_extract(re.escape(pattern_to_search), binary_data)

    with open('output.txt', 'w') as output_file:
        for extracted_bytes in extracted_data:
            integer_value = int.from_bytes(extracted_bytes[1:], byteorder='little')
            hex_representation = ' '.join(f'{byte:02X}' for byte in extracted_bytes)
            output_file.write(str(integer_value)+ '\n')

if __name__ == "__main__":
    main()
