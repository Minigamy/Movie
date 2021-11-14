
def diagonalDifference(arr):
    left = 0
    right = 0
    for i in range(len(arr)):
        left += arr[i][i]
        right += arr[i][len(arr)-1-i]
    res = abs(left - right)
    return res
