import random
import os
rand_list=[]
n=10
for i in range(n):
    rand_list.append(random.randint(1,9))

checker = rand_list[:]
checker.sort()
print(rand_list, checker)
while (checker != rand_list):
    for num in rand_list:
        for hash in range(num):
            print("#",end="")
        print()
    os.system('cls' if os.name == 'nt' else 'clear')
    random.shuffle(rand_list)

for num in rand_list:
    for hash in range(num):
        print("#",end="")
    print()