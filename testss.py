from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=2)
 
 
def print_cube(num):
    # function to print cube of given num
    # print("Cube: {}" .format(num * num * num))
    return 100
 
 
def print_square(num):
    # function to print square of given num
    # print("Square: {}" .format(num * num))
    return 200
 

def function1():
    async_result = pool.apply_async(print_cube, ({'11':3},))
    async_result1 = pool.apply_async(print_square, ({'11':4},))
 
    
    print(async_result.get(), async_result1.get())
    # both threads completely executed
    print("Done!")
 
if __name__ =="__main__":
    # creating thread
    function1()