_string = "oi amor8b"

_length = len(_string)

def isDigit(c):
        return ((ord(c) > 47) and (ord(c) < 58))


def intValue():
        value = 0; 
        _break = False 
        i = 0   
           
        while((i < _length) and (_break == False)):
            digit = ord(_string[i]) - 48 #48 a 57
            value =  digit
            if((digit > -1) and (digit < 10)):
                _break = True
            else:
                i = i + 1
        return value

print(intValue())

