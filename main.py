from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
import dotenv
import random
import string
import io
from base64 import b64encode, b64decode
from PIL import Image, ImageDraw, ImageFont

# Load the AES key from the .env file
dotenv.load_dotenv()
KEY = bytes.fromhex(dotenv.get_key(".env", "AES_KEY"))

# Characters not included in the CAPTCHA text to avoid confusion
unused = ['0', 'O', 'o', 'I', 'l', '1', '2', 'S', 's', '5', '7']
ALPHABET = (string.ascii_letters + string.digits)
for char in unused:
    ALPHABET = ALPHABET.replace(char, '')

def generate_captcha():
    """
    Generate a CAPTCHA image and GUID.
    Returns a dictionary containing:
    - 'data': Base64-encoded image.
    - 'guid': GUID for CAPTCHA validation.
    - 'text': The text of the CAPTCHA.
    """
    text = ''.join(random.choices(ALPHABET, k=4))
    image = generate_captcha_image(text)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='jpeg')
    img_byte_arr = b64encode(img_byte_arr.getvalue()).decode()
    t = hex(int(time.time()))
    guid = generate_captcha_guid(text, t)
    return {'data': img_byte_arr, 'guid': guid, 'text': text}

def generate_captcha_guid(text, t):
    """
    Generate a GUID by encrypting the CAPTCHA text and timestamp using AES.
    """
    cipher = AES.new(KEY, AES.MODE_ECB)
    data = pad((text + '#' + t).encode(), 16)
    return cipher.encrypt(data).hex()

def generate_dark_color(threshold=200, alpha=True):
    # Generate a random dark color.
    threshold = random.randint(0, threshold)
    colors = [random.randint(0, threshold) for _ in range(3)]
    random.shuffle(colors)
    if alpha:
        colors.append(255)
    return tuple(colors)

def generate_light_color(threshold=120, alpha=False):
    # Generate a random light color.
    colors = [random.randint(threshold, 255) for _ in range(3)]
    random.shuffle(colors)
    if alpha:
        colors.append(255)
    return tuple(colors)

def generate_captcha_image(text):
    """
    Generate a CAPTCHA image with noise and scrambled text.
    """
    height = 200
    width = 100
    image = Image.new('RGB', (height, width), color=generate_light_color())
    d = ImageDraw.Draw(image)
    font_size = 50
    font = ImageFont.truetype("fonts/font.ttf", font_size)
    start_x = 0
    y = (width - font_size) // 2

    measure = int(image.size[0] / len(text))

    # Draw each character with a different dark color
    for char in text:
        bbox = font.getbbox(char)
        bbox_width = bbox[2] - bbox[0]
        bbox_height = bbox[3]
        color = generate_dark_color()
        txt = Image.new('RGBA', (bbox_width, bbox_height), color=(0, 0, 0, 0))
        k = ImageDraw.Draw(txt)
        k.text((0, 0), char, font=font, fill=color)
        w = txt.rotate(round(random.random() - 0.5, 2) * 80, expand=round(2.5 + random.random(), 2)).resize((measure, bbox_height))
        image.paste(w, (int(start_x), y), w)
        start_x += measure

    # Add noise lines and points
    for _ in range(random.randint(10, 20)):
        color = generate_dark_color() if random.random() > 0.5 else generate_light_color(threshold=200, alpha=False)
        start = (random.randint(0, height), random.randint(0, width))
        end = (random.randint(0, height), random.randint(0, width))
        d.line([start, end], fill=color, width=random.randint(1, 2))

    for _ in range(random.randint(4000, 5000)):
        x = random.randint(0, height)
        y = random.randint(0, width)
        color = generate_dark_color() if random.random() > 0.5 else generate_light_color(threshold=200, alpha=False)
        d.point((x, y), fill=color)

    return image

def check_captcha_text(guid, text, expire=100):
    """
    Validate the CAPTCHA using the GUID and text.
    Checks if theCaptcha text matches and if the CAPTCHA is still valid based on the expiration time.
    """
    try:
        cipher = AES.new(KEY, AES.MODE_ECB)
        data = cipher.decrypt(bytes.fromhex(guid))
        data = unpad(data, 16).decode()
        d_text, t = data.split('#')
        t = int(t.strip(), 16)
        if t + expire < int(time.time()):
            return {'Success': False, 'Message': 'Expired Captcha'}
        if d_text.upper() == text.upper():
            return {'Success': True, 'Message': 'Valid Captcha'}
        return {'Success': False, 'Message': 'Invalid Text'}
    except:
        return {'Success': False, 'Message': 'Invalid GUID'}

if __name__ == '__main__':
    # Generate a CAPTCHA
    data = generate_captcha()
    image_b64 = data['data']
    guid = data['guid']
    text = data['text']

    print(f'GUID: {guid}')
    print(f'Text: {text}')

    # Decode and save the CAPTCHA image to a file
    with open('captcha.jpg', 'wb') as f:
        f.write(b64decode(image_b64))

    # Validate the CAPTCHA with the correct text
    print("Validation with correct text:", check_captcha_text(guid, text))

    # Validate the CAPTCHA with incorrect text
    print("Validation with incorrect text:", check_captcha_text(guid, 'fake'))

    # Validate the CAPTCHA with invalid GUID
    print("Validation with invalid GUID:", check_captcha_text('invalid', text))

    # Wait for 2 seconds and try to validate again with expiration time set to 1 second
    time.sleep(2)
    print("Validation after expiration:", check_captcha_text(guid, text, expire=1))