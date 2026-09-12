from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageDraw
import html

def generate_ascii():
    # Load crop_test2.png (380x380)
    img = Image.open('crop_test2.png')
    w, h = img.size

    # Create subject mask: center is person, edges fade out softly
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    # Head & shoulders ellipse
    draw.ellipse([(15, 10), (365, 375)], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=20))

    # Convert to grayscale
    gray = img.convert('L')
    
    # Sharpen to emphasize glasses frame, eyes, smile, hair texture
    gray_sharp = gray.filter(ImageFilter.UnsharpMask(radius=2.5, percent=220, threshold=2))
    
    # Increase contrast
    contrasted = ImageOps.autocontrast(gray_sharp, cutoff=1.5)
    contrasted = ImageEnhance.Contrast(contrasted).enhance(1.45)
    
    # Background in photo is light (around 220-255). Outside mask, fade to 255 (white)
    bg = Image.new('L', (w, h), 255)
    blended = Image.composite(contrasted, bg, mask)

    COLS = 91
    ROWS = 53
    resized = blended.resize((COLS, ROWS), Image.Resampling.LANCZOS)
    
    # Carefully tuned ramp matching Sushmita's visual density
    # Background / empty: space and dots . :
    # Skin highlights: - =
    # Midtones: + *
    # Dark features (hair, glasses, eyes, top): # % @
    RAMP = "   ....::::--==++**#%%@@"
    pixels = resized.load()

    lines = []
    y_start = 79.98
    line_step = 7.55
    
    tspans = []
    raw_lines = []
    for y in range(ROWS):
        line_chars = []
        for x in range(COLS):
            val = 255 - pixels[x, y]
            idx = int((val / 255) * (len(RAMP) - 1))
            line_chars.append(RAMP[idx])
        line_str = "".join(line_chars)
        raw_lines.append(line_str)
        escaped = html.escape(line_str)
        curr_y = round(y_start + y * line_step, 2)
        tspans.append(f'<tspan x="30" y="{curr_y}" xml:space="preserve">{escaped}</tspan>')
        
    return "\n".join(tspans), "\n".join(raw_lines)

if __name__ == "__main__":
    tspans, raw = generate_ascii()
    with open("khushboo_tspans.txt", "w", encoding="utf-8") as f:
        f.write(tspans)
    with open("khushboo_raw_ascii.txt", "w", encoding="utf-8") as f:
        f.write(raw)
    print("ASCII generated successfully. First 15 lines:")
    print("\n".join(raw.splitlines()[:15]))
