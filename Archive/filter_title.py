with open('headline.txt', 'r') as file:
    data = file.read()

# with open('titles.txt', 'w') as file:
#
#         file.write(title)
#         file.write('\n')
#


for i in data.split('\n'):
    print('XXX')
    tokens = i.split('.')
    for idx in range(len(tokens)):
        if tokens[idx][-4:].isdigit():
            title = tokens[idx+1].strip()
            break
    names = i.split(title)[0].split('.,')[:-1]
    for i in names:
        print(i.strip() + ".", end="\n")
