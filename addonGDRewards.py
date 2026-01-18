import base64
import hashlib

GD_XOR_KEY_REWARDS = "59182"
GD_SALT_REWARDS = "pC26fpYaQCtg"
GD_URL_REWARDS = "www.boomlings.com/database/getGJRewards.php"
DEBUG_CONTENTS = True


def xor_str(s: str, key: str) -> str:
    return "".join(
        chr(ord(c) ^ ord(key[i % len(key)]))
        for i, c in enumerate(s)
    )

def decode_response(response: str) -> tuple[str, list[str]]:
    raw_response, _hash = response.split("|")
    prefix = raw_response[:5]
    response_encoded = raw_response[5:]

    response_encrypted = base64.urlsafe_b64decode(response_encoded).decode()
    response_content = xor_str(response_encrypted, GD_XOR_KEY_REWARDS)
    response_parts = response_content.split(":")

    return prefix, response_parts

def encode_response(prefix: str, content: list[str]):
    output_plain = ":".join(content)
    output_encoded = xor_str(output_plain, GD_XOR_KEY_REWARDS)
    output_encrypted = base64.urlsafe_b64encode(output_encoded.encode()).decode()

    sha1 = hashlib.sha1()
    sha1.update((output_encrypted + GD_SALT_REWARDS).encode())
    hash_value = sha1.hexdigest()

    return prefix + output_encrypted + "|" + hash_value


class GDRewards:
    def __init__(self, orbs: str, gems: str, item1: str, item2: str, modify_time: bool):
        self.modify_time = modify_time
        self.content_string = f"{orbs},{gems},{item1},{item2}"

    def __modify(self, original_response: str) -> str:
        prefix, content = decode_response(original_response)

        if DEBUG_CONTENTS:
            print("DEBUG: original contents: ", content)

        # overwrite contents
        content[6] = self.content_string
        content[9] = self.content_string

        if self.modify_time:
            # set remaining time to 0
            content[5] = "0"
            content[8] = "0"

            # handle opening of chests by incrementing counter
            if content[11] == "1":
                content[7] = str(int(content[7]) + 1)
            if content[11] == "2":
                content[10] = str(int(content[10]) + 1)

        if DEBUG_CONTENTS:
            print("DEBUG: modified contents: ", content)

        return encode_response(prefix, content)

    # mitmproxy response hook
    def response(self, flow):
        if GD_URL_REWARDS not in flow.request.pretty_url:
            return

        response_content = flow.response.content.decode()
        rewritten_content = self.__modify(response_content).encode()

        flow.response.set_content(rewritten_content)


addons = [
    GDRewards(
        "100",  # orbs
        "10",   # gems
        "6",    # item 1
        "6",    # item 2
        False   # modify_time
    )
]
