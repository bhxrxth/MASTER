def find_max(numbers):
    
    maximum = numbers[0]
    for numbers in numbers:
        if numbers > maximum:
            maximum = numbers
    return maximum
