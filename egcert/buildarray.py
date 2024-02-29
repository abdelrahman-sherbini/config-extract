import re

# The provided C# array format
csharp_array = open("regex.txt","r").read(999999)

# Extracting the array elements using regex
pattern = re.compile(r'\bnew uint\[\]\s*{([\s\S]*?)\}\s*,?')
matches = pattern.findall(csharp_array)

# Converting the matched elements to Python list format
python_list = []
for match in matches:
    uint_values = [value[:-1].strip() for value in match.split(',')]
    uint_values[-1] = uint_values[-1].rstrip('U')
    uint_values = ("[{0}]".format(', '.join(map(str, uint_values))))
    python_list.append(uint_values)

# Print the Python list
print("Python List:")
python_list = ("[{0}]".format(', '.join(map(str, python_list))))
open("pythonlist.txt","w").write(python_list)
