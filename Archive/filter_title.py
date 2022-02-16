with open('headline.txt', 'r') as file:
    data = file.read()

with open('titles.txt', 'w') as file:
    for i in data.split('\n'):
        #print(i)
        tokens = i.split('.')
        for idx in range(len(tokens)):
            if tokens[idx][-4:].isdigit():
                title = tokens[idx+1].strip()
                break
        file.write(title)
        file.write('\n')