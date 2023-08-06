import re

def Format_Validator(FieldFormat, FieldValue): 
    Regex_Match = re.match(FieldFormat, FieldValue)
    if Regex_Match: 
       return    Regex_Match
    else: 
       return    'FAIL'