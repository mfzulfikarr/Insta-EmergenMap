# Wagner-Fischer Algorithm to find closest word that are potentially the correct root word
def wagnerFischer(s1,s2):
    m = len(s1)
    n = len(s2)
    arr = [[0 for i in range(n+1)] for j in range(m+1)]
    for i in range(m+1):
        arr[i][0] = i
    for j in range(n+1):
        arr[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                arr[i][j] = arr[i-1][j-1]
            else:
                arr[i][j] = 1+min(arr[i-1][j-1],
                                  arr[i-1][j],
                                  arr[i][j-1])
    return arr[m][n]