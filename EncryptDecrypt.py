# Function to read the content of a file
def read_raw_file(file_path):
    try:
        # Try opening the file in read mode to fetch its content
        with open(file_path, "r") as f:
            return f.read()  # Return the content of the file as a string
    except FileNotFoundError:
        # If the file is not found, print an error message and stop the program
        print(f"Error: The file '{file_path}' was not found.")
        exit()  # Exit the program if the file is not found

# Function to write the encrypted text to a file
def write_encrypted_file(file_path, content):
    # Open the file in write mode and write the encrypted content to it
    with open(file_path, "w") as f:
        f.write(content)

# Function to encrypt the text based on user input values n and m
def encrypt_text(text, n, m):
    encrypted = ""  # Create an empty string to hold the encrypted text
    shift_info = []  
    # Loop through each character in the input text
    for char in text:
        if char.islower():  # Check if the character is a lowercase letter
            # If the letter is in the first half of the alphabet (a-m)
            if char <= 'm':
                shift = n * m  # Shift forward by n * m
                encrypted += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))  
                shift_info.append(('l_fwd', shift))  # Record the shift info for later use in decryption
            else:
                shift = n + m  # Shift backward by n + m for letters in the second half of the alphabet (n-z)
                encrypted += chr((ord(char) - ord('a') - shift) % 26 + ord('a')) 
                shift_info.append(('l_bwd', shift))  # Record the shift info for later use in decryption
        elif char.isupper():  # Check if the character is an uppercase letter
            # If the letter is in the first half of the alphabet (A-M)
            if char <= 'M':
                shift = -n  # Shift backward by n
                encrypted += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))  
                shift_info.append(('u_bwd', abs(shift)))  # Record the shift info for later use in decryption
            else:
                shift = m ** 2  # Shift forward by m^2 for letters in the second half of the alphabet (N-Z)
                encrypted += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                shift_info.append(('u_fwd', shift))  # Record the shift info for later use in decryption
        else:  # For non-alphabet characters (like spaces or punctuation)
            encrypted += char  # Leave the non-alphabet character unchanged
            shift_info.append(('non', 0))  # Record that there was no shift for non-alphabet characters

    # Return the encrypted text and the shift information (for later decryption)
    return encrypted, shift_info

# Function to decrypt the text based on the shift information
def decrypt_text(text, shift_info):
    decrypted = ""  # Create an empty string to store the decrypted text

    # Loop through each character and its corresponding shift information
    for idx, char in enumerate(text):
        rule, shift = shift_info[idx]  # Get the shift rule for the current character
        
        # Decrypt each character based on the stored shift information
        if rule == 'l_fwd':  # If the letter was shifted forward in the lowercase 'a-m' range
            decrypted += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        elif rule == 'l_bwd':  # If the letter was shifted backward in the lowercase 'n-z' range
            decrypted += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        elif rule == 'u_bwd':  # If the letter was shifted backward in the uppercase 'A-M' range
            decrypted += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        elif rule == 'u_fwd':  # If the letter was shifted forward in the uppercase 'N-Z' range
            decrypted += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:  # For non-letter characters (spaces, punctuation, etc.), just add them unchanged
            decrypted += char

    return decrypted  # Return the fully decrypted text

# Function to get valid input from the user (either integer or float)
def get_valid_input(prompt, allow_float=False):
    while True:
        user_input = input(prompt)  # Prompt the user to enter a value
        
        try:
            # If the input is allowed to be a float
            if allow_float:
                user_input_float = float(user_input)  # Try converting the input to a float
                if user_input_float < 0:  # Check if the number is positive
                    print("Invalid input. Please enter a positive number.")
                else:
                    return user_input_float  # Return the valid float value
            else:
                # If the input is expected to be an integer
                user_input_int = int(user_input)  # Try converting the input to an integer
                if user_input_int < 0:  # Check if the number is positive
                    print("Invalid input. Please enter a positive integer.")
                else:
                    return user_input_int  # Return the valid integer value
        except ValueError:
            # If the user enters something that isn't a valid number, print an error message
            print("Invalid input. Please enter a valid number (no letters, symbols, or invalid characters).")

# Main function to execute the program
def main():
    # Read the original raw text from a file
    raw_text = read_raw_file("raw_text.txt")
    print("\nContent of raw_text.txt:")
    print(raw_text)  # Print the content of the raw text file

    # Get valid values of n and m (both should be positive integers)
    n = get_valid_input("Enter value for n (positive integer): ", allow_float=False)
    m = get_valid_input("Enter value for m (positive integer): ", allow_float=False)

    # Encrypt the text using the values of n and m provided by the user
    encrypted_text, shift_info = encrypt_text(raw_text, n, m)
    write_encrypted_file("encrypted_text.txt", encrypted_text)  # Save the encrypted text to a file
    print("\nEncrypted content written to encrypted_text.txt")

    # Decrypt the text using the stored shift information
    decrypted_text = decrypt_text(encrypted_text, shift_info)
    print("\nDecrypted Text:")
    print(decrypted_text)  # Print the decrypted text to check if it matches the original text

    # Compare the decrypted text with the original raw text to verify correctness
    if decrypted_text == raw_text:
        print("\n Decryption successful. Text matches the original.")
    else:
        print("\n Decryption failed. Text does not match the original.")
        print("Original:", repr(raw_text))  # Show the original text to compare
        print("Decrypted:", repr(decrypted_text))  # Show the decrypted text for comparison

if __name__ == "__main__":
    main()  # Call the main function to run the program
