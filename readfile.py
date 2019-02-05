with open("testfile.txt", "r") as ins:
    array = []
    for line in ins:
        array.append(line[0:-3])
    print(array)
