import zlib
from PIL import Image, ImageDraw, ImageFont


def simulate_canvas_fingerprint(ha_value):
    width, height = 220, 30
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    text = f"BrowserLeaks,com <canvas> 1.0{ha_value}"
    font = ImageFont.truetype("arial.ttf", 14)

    draw.rectangle([125, 1, 125 + 62, 1 + 20], fill=(255, 102, 0, 255))
    draw.text((2, 15), text, font=font, fill=(0, 102, 153, 255), anchor="la")
    draw.text((4, 17), text, font=font, fill=(102, 204, 0, 178), anchor="la")

    pixel_data = img.tobytes()
    img.save('img/canvas.png')
    adler32_val = zlib.adler32(pixel_data) & 0xffffffff

    type_part = b"IDAT"
    adler_bytes = adler32_val.to_bytes(4, byteorder='big')
    data_part = b"\x03\x00" + adler_bytes

    target_crc = zlib.crc32(type_part + data_part) & 0xffffffff
    return f"{target_crc:08X}"


ha = "d4dfc"  # 你的动态 ha 值
print(f"生成的指纹 (CRC32): {simulate_canvas_fingerprint(ha)}")
