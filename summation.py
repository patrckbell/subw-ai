def factorial(n):
    fact = 1
 
    for i in range(1, n+1):
        fact = fact * i
    
    return fact

def sum(n):
    sum = 0

    for i in range(n+1):
        sum += factorial(n)/(factorial(i)*factorial(n-i))
    
    return sum

value = (7 * sum(14) * sum(14) * sum(3) * sum(20)) - 7

def sum2(n):
    sum = 0
    if n == 0 or n == 1:
        sum = 0
    elif n == 2:
        sum = 1
    else:
        for i in range(n):
            sum += (n-(i+1))
    return sum

def sum3():
    sum = 0
    for i in range(57):
        sum += sum2(i)
        print("Ingredients: " + str(i) + "\nConnections: " + str(sum2(i)) + "\n")
    return sum

print(sum3())