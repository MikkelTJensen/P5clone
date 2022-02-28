#Methods to flatten

#Flattening data and appending to list of results
def flatten(ylist, maxflat):
    result = []
    length = len(ylist)
    if(length < 3):
        print("ERROR cannot compute")
        return
    if(maxflat % 2 == 0):
        print("ERROR not uneven cannot compute")
        return

    result.append(ylist[0])

    number = 3
    index = 1
    while(index < length - 1):
        result.append(calcValue(ylist, index, number))
        if int(number / 2) + index == length - 1:
            number -= 2
        elif number != maxflat:
            number += 2
        index += 1

    result.append(ylist[-1])

    return result


#Calculates the average and appends it
def calcValue(ylist, middle_numb, n):
    summation = 0
    diff = int((n-1)/2)
    for k in range(n):
        summation += ylist[middle_numb + k - diff]
    return summation/n