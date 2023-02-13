

for i in range(1,10):

    count =+ i 

    try:
        if count % 2 == 0:
            print(count)
            raise Exception("ERRRRROR.")

    except Exception as e:
        print(e)

