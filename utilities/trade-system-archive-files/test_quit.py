import time

def q():
    for i in range(15):

        time.sleep(1)
        print(i)

        if i == 5:
            print("QUIT")
            quit()

q()

print("IM StILL ALIvE")