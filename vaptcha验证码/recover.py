import os
import hashlib
import requests
import subprocess
import numpy as np
import matplotlib.pyplot as plt


def solve_pow(challenge_str):
    level = 5
    i = 0
    while True:
        str_to_hash = challenge_str + str(i)
        hash_value = hashlib.sha256(str_to_hash.encode()).hexdigest()
        if is_ok(hash_value, level):
            return i
        i += 1

def is_ok(hash_str, level):
    if len(hash_str) < level:
        return False

    target_prefix = "0" * level
    return hash_str.startswith(target_prefix)

def decrypt(_0x96cb41, _0x27dab6):
    _0x1beceb = ""
    _0x1beceb = str(int(_0x96cb41) - _0x27dab6)
    if len(_0x1beceb) < 10:
        _0x1beceb = "0" + _0x1beceb
    return _0x1beceb

def get_canvas_mock(input_str):
    try:
        process = subprocess.run(
            ['node', r'C:\Users\gxst\PycharmProjects\PythonProject\VaptchaImage\js\fp.js', input_str],
            capture_output=True,
            text=True,
            check=True
        )
        hex_result = process.stdout.strip()
        print(hex_result)
        return int(hex_result, 16)
    except subprocess.CalledProcessError as e:
        print(f"Node运行报错: {e.stderr}")
        return None

def get_revert_order(img_order, r, ha, hb):
    _ha = int('BB6110D3', 16) # int(str(get_canvas_mock(ha)), 16)
    _hb = 0 # int(str(get_canvas_mock(hb)), 16)
    p = solve_pow(r)
    _0x5c63ec = _ha + _hb + 8549731620 + p
    _0x3ff040 = decrypt(img_order, _0x5c63ec)
    return _0x3ff040

def recover_frames_by_order(images, img_order, r, ha, hb):
    real_order = get_revert_order(img_order, r, ha, hb)
    print(real_order)
    frames = [images[int(_)] for _ in real_order]
    return frames

def recover_image(frames):
    _image = np.concatenate([np.concatenate(frames[i:i+5], axis=1) for i in range(0, 10, 5)], axis=0)
    return _image

def clip_image(_image):
    tile_width = 80
    tile_height = 115
    num_cols = 5  # 400 / 80
    num_rows = 2  # 230 / 115
    _tiles = [_image[r * tile_height:(r + 1) * tile_height, c * tile_width:(c + 1) * tile_width] for r in range(num_rows) for c in range(num_cols)]
    return _tiles

if __name__ == '__main__':
    data = {
        "hb": "",
        "img_order": "13641810615",
        "img": "https://img-cn.vaptcha.net/vaptcha/d62b89814aa64f9e85e3e7c73ee61534.jpg",
        "frequency": 0.35,
        "aso": "",
        "is_vip": 0,
        "adt": 0,
        "r": "7dfe1025119b64d",
        "u": "",
        "ut": "",
        "token": "",
        "ha": "2d68b",
        "a_t": 0,
        "a_p": "",
        "a_i": ""
    }
    filename = data['img'].split('/')[-1]
    if not os.path.exists(rf'img/{filename}'):
        with open(rf'img/{filename}', 'wb') as f:
            f.write(requests.get(data['img']).content)
    image = plt.imread(rf'img/{filename}')

    tiles = recover_frames_by_order(clip_image(image), data['img_order'], data['r'], data['ha'], data['hb'])
    plt.imshow(recover_image(tiles))
    plt.show()


