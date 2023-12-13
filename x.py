'''

N = int(input(f"\nEnter the no till which you want to display the results of a fibonacci sequence  "))
fib_no=0
fib=[0,1]
for k in range(N-2):
    fib_next = fib[k+1]+fib[k]
    fib.append(fib_next)
print(f"\nFor {N}, highets value of fibonacci sequence is {fib[-1]}")
print(f"\n{fib}")

'''