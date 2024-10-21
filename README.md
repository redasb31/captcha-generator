# CAPTCHA Generator and Validator with AES Encryption
A Python script to generate CAPTCHA images with scrambled text and noise, encrypted using AES for validation. This project is designed for generating CAPTCHA images and verifying user input using a unique `GUID` that is encrypted with AES-ECB. The `GUID` is a hex string representing the encrypted combination of the CAPTCHA text and creation timestamp, providing an added layer of security.

## Features

- Generates CAPTCHA images with random scrambled text and noise for increased difficulty.
- Uses AES encryption to create a `GUID` based on the CAPTCHA text and generation time.
- Validates user input against the generated CAPTCHA using the `GUID` and text.
- Allows expiration.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/captcha-generator.git
   cd captcha-generator
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your AES key:
   ```
   AES_KEY=your_aes_key_in_hex
   ```
   - The key must be a 16, 24, or 32 bytes hex string (128, 192, or 256 bits).

## Usage

Run the script:
```bash
python captcha_generator.py
```

This will generate a CAPTCHA image, print the `GUID`, and test the validation function with both correct and incorrect inputs.

## Example Output

- **Generated CAPTCHA Image:**

  ![Generated CAPTCHA](captcha.jpg)

- **GUID and Validation Example:**
  ```
  GUID: d09b1c7e0e8d2a6f...
  Text: ABCD
  {'Success': True, 'Message': 'Valid Captcha'}
  {'Success': False, 'Message': 'Invalid Text'}
  {'Success': False, 'Message': 'Expired Captcha'}
  ```