import re
from functools import cmp_to_key

regex2 = r"[A-Z][A-Z]([A-Z][a-z][A-Z])[A-Z][A-Z]"
regex = r"[^A-Z][A-Z][A-Z]([A-Z][^A-Z][A-Z])[A-Z][A-Z][^A-Z]"
file_path = "data.txt"
output_file_path = "output"


def comparator(trio1, trio2):
    return (ord(trio1[0]) + ord(trio1[2])) - (ord(trio2[0]) + ord(trio2[2]))


with open(file_path, "r") as file:
    data = file.read()
regex1 = re.compile(regex)
result = regex1.findall(data)
sorted_list = sorted(result, key=cmp_to_key(comparator))
code = "".join(list(map(lambda x: x[1], sorted_list)))

with open(output_file_path, "w") as output_file:
    output_file.write(code)
