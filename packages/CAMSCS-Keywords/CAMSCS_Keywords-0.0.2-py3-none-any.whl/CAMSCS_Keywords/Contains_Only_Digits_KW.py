import re

def contains_only_digits(StrValue):
    # Using regex() 
    if re.match('^[0-9]*$', StrValue): 
       return   'PASS' 
    else: 
       return   'FAIL'

