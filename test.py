f1 = []
with open('requirements.txt', 'r') as file:
    for line in file:
        line = line.rstrip()
        f1.append(line)

print(f1)
