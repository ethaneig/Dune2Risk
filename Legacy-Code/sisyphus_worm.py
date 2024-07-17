import os
import time
import random

def main():
    rand_list=[]
    n=8
    for i in range(n):
        rand_list.append(random.randint(1,9))

    checker = rand_list[:]
    checker.sort()
    while (checker != rand_list):
        lister(rand_list)
        timer = 0.1
        print("                      /######\ ")
        print("      /#######\     /#### #####\     /#####\ ")
        print("    /#####/  \###\ /####/  \####\__/####  ###\ ")
        print("   /####/     \###V####/     \###############/")
        print(" /####/        \######/         \###########/   ")
        print(" ###                               ######")

        time.sleep(timer)

        os.system('cls' if os.name == 'nt' else 'clear')
        lister(rand_list)
        print("       /#####\      ")
        print("      /#######\      /########\     /#####\ ")
        print("    /#####/  \###\ /####/ \####\__/###  ###\ ")
        print("   /####/     \###V####/    \#############/")
        print(" /####/        \######/        \#########/   ")
        print("                 ###             ######")

        time.sleep(timer)
        os.system('cls' if os.name == 'nt' else 'clear')
        lister(rand_list)
        print("                      /######\ ")
        print("      /#######\     /#### #####\     /#####\ ")
        print("    /#####/  \###\ /####/  \####\__/####  ###\ ")
        print("   /####/     \###V####/     \###############/")
        print(" /####/        \######/         \###########/   ")
        print(" ###                               ######")

        time.sleep(timer)
        os.system('cls' if os.name == 'nt' else 'clear')
        lister(rand_list)
        print("       /#####\      ")
        print("      /#######\      /########\     /#####\ ")
        print("    /#####/  \###\ /####/ \####\__/###  ###\ ")
        print("   /####/     \###V####/    \#############/")
        print(" /####/        \######/        \#########/   ")
        print("                 ###             ######")
        
        time.sleep(timer)
        os.system('cls' if os.name == 'nt' else 'clear')
        lister(rand_list)
        print("                      /######\ ")
        print("      /#######\     /#### #####\     /#####\ ")
        print("    /#####/  \###\ /####/  \####\__/####  ###\ ")
        print("   /####/     \###V####/     \###############/")
        print(" /####/        \######/         \###########/   ")
        print(" ###                               ######")
        
        time.sleep(timer)
        os.system('cls' if os.name == 'nt' else 'clear')
        lister(rand_list)

        print("       /#####\      ")
        print("      /#######\      /########\     /#####\ ")
        print("    /#####/  \###\ /####/ \####\__/###  ###\ ")
        print("   /####/     \###V####/    \#############/")
        print(" /####/        \######/        \#########/   ")
        print("                 ###             ######")

        time.sleep(timer)
        os.system('cls' if os.name == 'nt' else 'clear')
        lister(rand_list)

        print("                      /######\ ")
        print("      /#######\     /#### #####\     /#####\ ")
        print("    /#####/  \###\ /####/  \####\__/####  ###\ ")
        print("   /####/     \###V####/     \###############/")
        print(" /####/        \######/         \###########/   ")
        print(" ###                               ######")

        time.sleep(timer)
        os.system('cls' if os.name == 'nt' else 'clear')
        lister(rand_list)

        print("       /#####\      ")
        print("      /#######\      /########\     /#####\ ")
        print("    /#####/  \###\ /####/ \####\__/###  ###\ ")
        print("   /####/     \###V####/    \#############/")
        print(" /####/        \######/        \#########/   ")
        print("                 ###             ######")

        time.sleep(timer)
        os.system('cls' if os.name == 'nt' else 'clear')

    for num in rand_list:
        for hash in range(num):
            print("#",end="")
        print()

    print("                      /######\ ")
    print("      /#######\     /#### #####\     /#####\ ")
    print("    /#####/  \###\ /####/  \####\__/####  ###\ ")
    print("   /####/     \###V####/     \###############/")
    print(" /####/        \######/         \###########/   ")
    print(" ###                               ######")



def lister(rand_list):
    for num in rand_list:
        for hash in range(num):
            print("#",end="")
        print()
    random.shuffle(rand_list)

main()