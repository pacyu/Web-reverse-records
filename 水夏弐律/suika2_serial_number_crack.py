import ctypes
import string
import random


def to_int32(val):
    return ctypes.c_int32(val).value

def reverse_permutation(s_prime):
    """
    将置换后的 11 位字符串还原为原始输入字符串
    :param s_prime: 已经匹配好校验位的字符串 (长度11)
    """
    # 原始置换表 (Index in S -> Position in S')
    perm_table = [0, 1, 5, 3, 10, 8, 7, 2, 6, 9, 4]

    # 创建一个空列表来存放结果
    original_s = [''] * 11

    # 遍历置换表：s_prime 的第 i 位，应该放回到原始字符串的第 perm_table[i] 位
    for i, original_idx in enumerate(perm_table):
        original_s[original_idx] = s_prime[i]

    return "".join(original_s)

def suika2_permute_string(input_str: str) -> str:
    # 47E110 处的索引表数据
    permutation_table = [0, 1, 5, 3, 10, 8, 7, 2, 6, 9, 4]

    # 将输入转为列表（模拟栈上的临时缓冲区 esp+4）
    # 如果输入长度不足 11，汇编代码可能会读取到内存中的脏数据
    # 这里我们确保处理前 11 个字符
    buffer = list(input_str)

    # 结果容器 (esi)
    esi = [''] * 11

    # 汇编循环部分 (0042E160 - 0042E172)
    # i 对应 eax，idx 对应 ecx
    for i in range(11):
        idx = permutation_table[i]
        esi[i] = buffer[idx]

    return "".join(esi)

def crc16_ccitt(data_str):
    crc = 0
    # 只取前 7 位，因为 push 7
    for char in data_str[:7]:
        # movzx ax, byte ptr [ecx] + shl ax, 8
        # xor word ptr [esp], ax
        crc ^= (ord(char) << 8)

        # 对应汇编中手写展开的 8 次位检查
        for _ in range(8):
            if crc & 0x8000:
                # add eax, eax + xor eax, 1021
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                # add eax, eax
                crc = (crc << 1) & 0xFFFF
    return crc

def suika2_decode(input_str: str) -> int:
    # 36进制转换逻辑 (Base36 Decode)
    esi = 0
    for char in input_str:
        val = (ord(char) - 22) if char.isdigit() else (ord(char.upper()) - 65)
        esi = (esi * 36) + val
        esi &= 0xFFFFFFFF
    return esi

def calc_asm_logic(input_ax):
    # 0042E3B0: movzx ecx, ax (将输入扩展为32位无符号)
    ecx = input_ax & 0xFFFF

    # 0042E3B3: mov eax, 51EB851F
    magic = 0x51EB851F

    # 0042E3B8: imul ecx
    # 汇编 imul 指令(单操作数)执行: EDX:EAX = EAX * ECX
    # 结果是一个64位值。EDX 存储高32位，EAX 存储低32位。
    full_mul = magic * ecx
    eax = full_mul & 0xFFFFFFFF
    edx = (full_mul >> 32) & 0xFFFFFFFF

    # 0042E3BA: sar edx, 3 (算术右移 3 位，保留符号位)
    edx_s32 = to_int32(edx)
    sar_edx = edx_s32 >> 3

    # 0042E3BD: mov eax, edx
    # 0042E3BF: shr eax, 1F (逻辑右移 31 位，获取符号位)
    # 0042E3C2: add eax, edx
    eax_sign = (sar_edx >> 31) & 1
    final_eax = to_int32(eax_sign + sar_edx)

    # 0042E3C4: mov edx, ecx
    # 0042E3C6: sub edx, eax
    # 0042E3C8: imul edx, edx, 19 (即乘以十进制 25)
    # 0042E3CB: add edx, ecx
    res_edx = to_int32(ecx - final_eax)
    res_edx = to_int32(res_edx * 0x19)
    final_edx = to_int32(res_edx + ecx)

    # 返回最终存入 EDX 用于 cmp 的值
    return final_edx & 0xFFFFFFFF

def int_to_chars(target_value):
    chars = []
    temp = target_value

    # 提取 4 个 36 进制位
    vals = []
    for _ in range(4):
        vals.append(temp % 36)
        temp //= 36
    vals.reverse() # 顺序变为 [v7, v8, v9, v10]

    for v in vals:
        # 尝试还原为数字 (val + 22)
        c_code = v + 22
        if ord('0') <= c_code <= ord('9'):
            chars.append(chr(c_code))
        else:
            # 还原为大写字母 (val + 41)
            chars.append(chr(v + 41))
    return "".join(chars)

def final_check_logic(esi):
    # --- 阶段 A: 计算除以 10^7 的变换 ---
    # 0042E269: mov eax, 6B5FCA6B; imul esi
    magic1 = 0x6B5FCA6B
    full_mul1 = magic1 * esi
    edx1 = (full_mul1 >> 32) & 0xFFFFFFFF

    # 0042E270 - 0042E278: 优化除法的后期处理 (sar, shr, add)
    # 本质是: eax = esi // 10,000,000
    sar_edx1 = to_int32(edx1) >> 22  # C1FA 16 是右移 22 位
    sign_eax1 = (sar_edx1 >> 31) & 1
    q1 = to_int32(sign_eax1 + sar_edx1)

    # 0042E27A: imul eax, eax, 989680 (0x989680 = 10,000,000)
    eax_product1 = to_int32(q1 * 10000000)

    # 0042E282: sub ecx, eax (计算 esi % 10,000,000)
    ecx = to_int32(esi - eax_product1)

    # --- 阶段 B: 计算除以 6 的变换 ---
    # 0042E284: mov eax, 2AAAAAAB; imul ecx
    magic2 = 0x2AAAAAAB
    full_mul2 = magic2 * ecx
    edx2 = (full_mul2 >> 32) & 0xFFFFFFFF

    # 0042E28D - 0042E290: 逻辑类似于除以 6
    # 本质是: eax = ecx // 6
    sar_edx2 = to_int32(edx2)  # 这里没写 sar, 说明直接用 edx
    sign_eax2 = (to_int32(edx2) >> 31) & 1
    q2 = to_int32(sign_eax2 + edx2)

    # 0042E294: imul eax, eax, 3938700 (0x3938700 = 60,000,000)
    # 0042E29A: imul edx, edx, 989681 (0x989681 = 10,000,001)
    eax_final = to_int32(q2 * 60000000)
    edx_final = to_int32(ecx * 10000001)

    # 0042E2A0: sub edx, eax
    result_edx = to_int32(edx_final - eax_final)

    return result_edx

def generate_serial_number():
    """
    还原游戏校验逻辑，游戏校验分为 4 个部分：
    1. 输入的序列号长度必须为 11 位，且只能是数字+字母组合。
    2. 第二步会将序列号根据映射表进行变换。
    3. 第三步是拆分变换后的序列号，以及计算 CRC + 取模运算，具体如下：
        1) 第一段是固定的: 'DW'
        2) 第二段调用函数计算的结果值必须要小于 10000000 且能被6整除
        3) 第三段是 CRC 校验结果值，它等于第一段+第二段的字符串进行 CRC 计算结果
    4. 最后会检查依次第三段、第二段、第一段的值是否合法。
    """
    charset = string.digits + string.ascii_uppercase

    print("正在搜索合法序列号...")
    attempts = 0
    while True:
        attempts += 1


        # 随机生成中间 5 位
        transformed_str = 'DW' + ''.join(random.choices(charset, k=5))
        print(f"变换后的序列号: {transformed_str}")

        if attempts % 100000 == 0:
            print(f"已尝试 {attempts} 次...")

        segment1 = suika2_decode(transformed_str[:2])
        print(f"字符串 '{transformed_str[:2]}' 的计算结果: {hex(segment1)}")

        segment2 = suika2_decode(transformed_str[2:7])
        print(f"字符串 '{transformed_str[2:7]}' 的计算结果: {hex(segment2)}")

        crc_value = crc16_ccitt(transformed_str)
        print(f"'{transformed_str[:7]}' 的 CRC 运算结果: {hex(crc_value)}")

        final_value = calc_asm_logic(crc_value)
        print(f"对 CRC 值 {hex(crc_value)} 的运算结果: {hex(final_value)}")

        recover_chars = int_to_chars(final_value)
        print(f"{hex(final_value)} -> {recover_chars}")

        reverse_value = suika2_decode(recover_chars)
        print(f"{recover_chars} -> {hex(reverse_value)}")

        if reverse_value == final_value and segment2 < 10000000 and segment2 % 6 == 0 and recover_chars.isalnum():
            serials = transformed_str[:7] + recover_chars
            print("找到合法序列号:", serials)
            print("序列号还原:", reverse_permutation(serials))
            break

        print('=' * 25)

def test():
    transformed_str = 'DW7L3F0AB43'
    print(f"变换后结果: {transformed_str}")
    segment1 = suika2_decode(transformed_str[:2])
    print(f"字符串 '{transformed_str[:2]}' 的计算结果: {hex(segment1)}") # 00000475

    segment2 = suika2_decode(transformed_str[2:7])
    print(f"字符串 '{transformed_str[2:7]}' 的计算结果: {hex(segment2)}") # 01BD70F4

    segment3 = suika2_decode(transformed_str[7:])
    print(f"字符串 '{transformed_str[7:]}' 的计算结果: {hex(segment3)}") # 00160709

    crc_value = crc16_ccitt(transformed_str)
    print(f"'{transformed_str[:7]}' 的 CRC 运算结果: {hex(crc_value)}")

    final_value = calc_asm_logic(crc_value)
    print(f"对 CRC 值 {hex(crc_value)} 的运算结果: {hex(final_value)}")

    recover_chars = int_to_chars(final_value)
    print(f"{hex(final_value)} -> {recover_chars}")

    reverse_value = suika2_decode(recover_chars)
    print(f"{recover_chars} -> {hex(reverse_value)}")

    if reverse_value == final_value and segment2 < 10000000 and segment2 % 6 == 0 and recover_chars.isalnum():
        serials = transformed_str[:7] + recover_chars
        print("找到合法序列号:", serials)
        print("序列号还原:", reverse_permutation(serials))

if __name__ == "__main__":
    generate_serial_number()
    # test()