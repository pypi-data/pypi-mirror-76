def mean(arr):
    s = 0
    for i in arr:
        s+=i
    return s/len(arr)
def median(arr):
    n = len(arr)
    arr1 = arr.copy()
    arr1.sort()
    if n%2==1:
        return arr1[n//2]
    else:
        return arr1[n//2-1,n//2]
def mode(arr):
    arr1 = arr.copy()
    arr1.sort()
    c = 1
    m = 0
    k =0
    for i in len(arr1):
        if arr1[i]!=arr1[i+1]:
            c = 1
            if m<c:
                m = c
                k = i
        c+=1
    if m<c:
        m=c
        k = len(arr1)-1
    return arr[k]