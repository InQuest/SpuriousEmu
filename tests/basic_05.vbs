' Function definition test
Sub proc1
End Sub

Sub proc2 (v1, v2, v3)
    print v1, v2, v3
End Sub

Sub proc3 (start, end)
    For i = start To end
        print i
    Next
End Sub

Function fun1
    Set fun1 = 12
End Function

Function fun2(i, j, k)
    Set fun2 = 12 * i + (12 * 23 * j) + k
End Function