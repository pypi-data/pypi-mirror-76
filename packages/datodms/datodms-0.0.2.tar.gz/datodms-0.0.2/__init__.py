def dms(x):
    if x % 1 == 0:
        print(x, "degree")
        
    if x % 1 != 0:
        a = x % 1
        degree = x - a
        minute = a * degree
        c = minute % 1
        d = minute - c
        second = c * d

        if second >= 60:
            var_sec_a = int(second) % 60
            var_sec_b = int(second) - int(var_sec_a)
            var_sec_c = int(var_sec_b) / 60
            second = int(var_sec_a)
            minute += int(var_sec_c)
        
        if minute >= 60:
            var_min_a = int(minute) % 60
            var_min_b = int(minute) - int(var_min_a)
            var_min_c = int(var_min_b) / 60
            minute = int(var_min_a)
            degree += int(var_min_c)

        print(int(degree), "degree", int(minute), "minutes", int(second), "seconds")