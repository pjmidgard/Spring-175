import base64

# Ask the user for an option
choice = input("Choose an option:\n1. Compress a file\n2. Extract a file\nEnter 1 or 2: ")

if choice == "1":
    # Compression
    file_name = input("Enter the name of the file you want to compress: ")

    with open(file_name, "rb") as file:
        file_content = file.read()

    compressed_content = file_content
    encoded_content = base64.b64encode(compressed_content)
   

    output_file_name = input("Enter the name of the output file for the compressed data: ")

    with open(output_file_name, "wb") as output_file:
        output_file.write(encoded_content)

    print(f"File '{file_name}' compressed and saved as '{output_file_name}'.")
elif choice == "2":
    # Extraction
    file_name = input("Enter the name of the file you want to extract: ")

    with open(file_name, "rb") as file:
        file_content = file.read()

    decoded_content = base64.b64decode(file_content)
    decompressed_content = decoded_content

    extracted_file_name = input("Enter the name of the output file for the extracted data: ")

    with open(extracted_file_name, "wb") as extracted_file:
        extracted_file.write(decompressed_content)

    print(f"File '{file_name}' extracted and saved as '{extracted_file_name}'.")
else:
    print("Invalid option. Please choose 1 or 2.")