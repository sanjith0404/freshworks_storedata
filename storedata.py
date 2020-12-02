import sys
import threading
import os

cwd = os.getcwd()
choice = input("The file will be created in the Current Directory - '" + cwd + "\storedata.txt'\n'y' to continue or 'n' to Enter path\n")
if choice == 'y' or choice == 'Y':
    path = cwd + '\storedata.txt'
    f = open(path, "a")
else:
    path = input("Enter the path of your location ")
    path = path + '\storedata.txt'
    f = open(path, 'a')
f.close()
print("file successfully created!")

def delete(key):
    present = False
    with open(path, "r") as f:
        lines = f.readlines()
    with open(path, "w") as f:
        for line in lines:
            first = line.split(" ")[0]
            if first != key:
                f.write(line)
            elif first == key:
                present = True
                print("\nRecord '" + key + "' Deleted \n")
    if not present:
        print("\nrecord not found'" + key + "'\n")

def create(key, value, ttl=-1):
    present = False
    limit = True
    size = True
    if os.path.getsize(path) > 1000000000:
        size = False
    if len(key) > 32 or sys.getsizeof(value) > 16000:
        limit = False
    with open(path, 'r') as f:
        search = f.readlines()
        phrase = key + " -"
        for line in search:
            if phrase in line:
                present = True
    if not present and limit and size:
        with open(path, 'a') as f:
            f.write(key + ' - ' + value + '\n')
            print("\nRecord created\n")
        if ttl > -1:
            t = threading.Timer(ttl, delete, [key])
            t.start()
    elif not limit:
        print("\nParameter over limit\n")
    elif present:
        print("\n '" + key + "' already exsists \n")
    elif not size:
        print("file size over 1GB")

def read(key):
    with open(path, 'r') as f:
        search = f.readlines()
        phrase = key + " -"
        for line in search:
            if phrase in line:
                print(line)
                break
        else:
            print("\nNo Records present in '" + key + "'\n")


print("\n\n**** StoreData ****\n\n")
print("1. create(key , value , <time to live> )\n2. read(key)\n3. delete(key)\n4.exit()\n")

running = True
while (running):
    cmd = input('Enter Command ')
    cmd = cmd.split(",", 1)
    choice = cmd[0].split('(')
    key = choice[1]
    choice = choice[0]
    if choice == 'create':
        value = cmd[1].rsplit(')', 1)[0]
        li = list(value)
        if li[-1] == '}':
            create(key, value)
        else:
            value = value.rsplit(',', 1)
            ttl = int(value[1])
            value = value[0]
            create(key, value, ttl)
    elif choice == 'read':
        key = key.split(')')[0]
        read(key)
    elif choice == 'delete':
        key = key.split(')')[0]
        delete(key)
    elif choice == 'exit':
        running = False
    else:
        print("invalid")
