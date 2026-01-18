import base64
import hashlib

def xor_str(s: str, key: str) -> str:
    return "".join(
        chr(ord(c) ^ ord(key[i % len(key)]))
        for i, c in enumerate(s)
    )


def gdhook(input_value: str) -> str:
    input_parts = input_value.split("|")
    input_raw = input_parts[0][5:]
    decoded = base64.urlsafe_b64decode(input_raw).decode("latin1")
    input_decoded = xor_str(decoded, "59182")

    content = input_decoded.split(":")
    # small chest
    # content[5] = "0" 
    content[6] = "2500000,40000,6,6"
    # large chest
    # content[8] = "0"
    content[9] = "2500000,40000,6,6"
    # number increments
    # if content[11] == "1":
    #     content[7] = str(int(content[7]) + 1)
    # if content[11] == "2":
    #     content[10] = str(int(content[10]) + 1)
    print(content)

    output_plain = ":".join(content)
    prefix = input_parts[0][:5]
    xor_encoded = xor_str(output_plain, "59182")
    output_enc = base64.urlsafe_b64encode(xor_encoded.encode("latin1")).decode()

    magic_suffix = "pC26fpYaQCtg"
    sha1 = hashlib.sha1()
    sha1.update((output_enc + magic_suffix).encode())
    hash_value = sha1.hexdigest()

    return prefix + output_enc + "|" + hash_value


class GDRewards:
    def response(self, flow):
        if "getGJRewards.php" not in flow.request.url:
            return

        str_content = flow.response.content.decode("utf-8")
        flow.response.set_content(gdhook(str_content).encode())

addons = [GDRewards()]

