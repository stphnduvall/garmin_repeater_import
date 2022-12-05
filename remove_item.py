def remove_from_list(list):
    print(*[f"{x}, {list[x]}\n" for x in range(0, len(list))])
    i = input("Enter a value to remove from list")
    while i != '':
        list.pop(int(i))        
        print(*[f"{x}, {list[x]}\n" for x in range(0, len(list))])
        i = input("Enter a value to remove from list")
    return list


