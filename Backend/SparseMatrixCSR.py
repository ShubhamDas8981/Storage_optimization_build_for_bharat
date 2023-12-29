def conversion(pin):
    return [int(digit) for digit in str(pin)]

def sparse(array):
    elements=[]
    col=[]
    for index,i in enumerate(array):
        #print(i)
        if (i!=0):
            elements.append(i)
            col.append(index+1)
    print(f"Non zero elemets in pin are: {elements}")
    print(f"Respectively column number are: {col}")


if __name__=="__main__":
    input_number=int(input("Enter the pin: "))
    array=conversion(input_number)
    print(array)
    sparse(array)


