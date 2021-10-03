"""
Run python autograder.py 
"""

def average(priceList):
    "Return the average price of a set of fruit"
    "*** YOUR CODE HERE ***"
    sum = 0
    nums = set(priceList)
    for num in nums:
     sum+=num
    avg = sum/len(nums)
    return avg
