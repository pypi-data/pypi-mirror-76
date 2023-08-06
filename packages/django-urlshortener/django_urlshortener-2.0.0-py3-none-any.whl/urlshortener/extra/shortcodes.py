import string
import random


data = string.ascii_lowercase + string.digits


def get_shortcode(length):
    code_list = random.choices(data, k=length)
    return "".join(code_list)
