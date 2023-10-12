# Function to compress data with a variable compression level 'A' (0-2^24)
def compress_data(data, level):
    if level < 0 or level > 2**24:
        print("Compression level must be between 0 and 2^24. Using 2^24 as the default.")
        level = 2**24

    compressed_data = []
    count = 0
    current_byte = 0
    level_power = 2**level

    for bit in data:
        current_byte = (current_byte << 1) | bit
        count += 1
        while count >= level:
            compressed_data.append(current_byte >> (count - level))
            current_byte &= (level_power - 1)
            count -= level
    if count > 0:
        compressed_data.append(current_byte << (level - count))

    return bytes(bytearray(compressed_data))

# Function to extract data with a variable compression level 'A' (0-2^24)
def extract_data(compressed_data, level):
    if level < 0 or level > 2**24:
        print("Extraction level must be between 0 and 2^24. Using 2^24 as the default.")
        level = 2**24

    extracted_data = []
    current_byte = 0
    count = 0
    level_power = 2**level

    for byte in compressed_data:
        current_byte = (current_byte << 8) | byte
        count += 8
        while count >= level:
            extracted_data.extend(((current_byte >> (count - level)) & 0xFF).to_bytes(1, byteorder='big'))
            current_byte &= (level_power - 1)
            count -= level

    return bytes(extracted_data)

if __name__ == "__main__":
    while True:
        print("Options:")
        print("1. Compress data")
        print("2. Extract data")
        print("3. Quit")

        option = input("Choose an option (1/2/3): ")

        if option == '1':
            file_name = input("Enter the name of the file for compression: ")
            try:
                with open(file_name, "rb") as file:
                    content = file.read()

                success_threshold = 0.01  # Set a fixed threshold of 0.01

                best_level = None
                best_compressed_data = None
                best_success_rate = 0.0

                for A in range(0, 2**24 + 1):
                    compressed_data = compress_data(content, A)
                    extracted_data = extract_data(compressed_data, A)

                    correct_bits = sum(1 for a, b in zip(content, extracted_data) if a == b)
                    success_rate = correct_bits / len(content)

                    if success_rate >= success_threshold and success_rate > best_success_rate:
                        best_level = A
                        best_compressed_data = compressed_data
                        best_success_rate = success_rate

                if best_level is not None:
                    print(f"Best compression level found: {best_level}")

                    # Save the compressed data
                    compression_filename = f"compressed_data_{best_level}.bin"
                    with open(compression_filename, "wb") as compressed_file:
                        compressed_file.write(best_compressed_data)
                    print(f"Compressed data saved as '{compression_filename}'")
                else:
                    print(f"No suitable compression level found. Defaulting to level 1.")

                    # Default to level 1
                    best_level = 1
                    compressed_data = compress_data(content, 1)

                    # Save the compressed data with level 1
                    compression_filename = f"compressed_data_1.bin"
                    with open(compression_filename, "wb") as compressed_file:
                        compressed_file.write(compressed_data)
                    print(f"Compressed data saved as '{compression_filename}'")

            except FileNotFoundError:
                print(f"File '{file_name}' not found.")
        elif option == '2':
            file_name = input("Enter the name of the file for extraction: ")
            try:
                with open(file_name, "rb") as file:
                    compressed_data = bytearray(file.read())
                extraction_level = int(input(f"Enter extraction level (0-{2**24}): "))

                # Extraction
                extracted_data = extract_data(compressed_data, extraction_level)
                extracted_filename = f"extracted_{file_name}"
                with open(extracted_filename, "wb") as extracted_file:
                    extracted_file.write(extracted_data)
                print(f"Data extracted and saved as '{extracted_filename}'")

            except FileNotFoundError:
                print(f"File '{file_name}' not found.")
        elif option == '3':
            break