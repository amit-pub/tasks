#
# Goal is - 
# Validate post-codes of United-Kingdom.
# 

import re

# pos_allowd_letters : position wise allowed letters are mentioned here
pos_allowd_letters = {
  "first": "ABCDEFGHIJKLMNOPRSTUWYZ",
  "second": "ABCDEFGHKLMNOPQRSTUVWXY",
  "third": "ABCDEFGHJKPSTUW",
  "fourth": "ABEHMNPRVWXY",
  "final": "ABDEFGHJLNPQRSTUWXYZ"
}

# list of allowd patterns
pattern_list = [
"^[{first}][1-9]\d[{final}][{final}]$",
"^[{first}][1-9]\d\d[{final}][{final}]$",
"^[{first}][{second}]\d\d[{final}][{final}]$",
"^[{first}][{second}][1-9]\d\d[{final}][{final}]$",
"^[{first}][1-9][{third}]\d[{final}][{final}]$",
"^[{first}][{second}][1-9][{fourth}]\d[{final}][{final}]$"
]

class Solution():
    def __init__(self):
        # create formatted list
        format_list = [str.format(**pos_allowd_letters) for str in pattern_list]
        # Add OR in between all the formated patterns
        pattern = "|".join(format_list)
        # create a validation compiler using regex "re" module
        self.valid_pcode_pattern = re.compile(pattern)

    def validate(self, pcode):
        return self.valid_pcode_pattern.match(pcode) is not None

if __name__ == "__main__":
    cls = Solution()
    filename = "postcodes.lst"
    print "--------------------"
    print "Post-code -- Result"
    print "--------------------"
    try:
        with open(filename) as f:
            for line in f.readlines():
                pcode = line.strip("")
                pcode = pcode.replace(" ", "")
                result = cls.validate(pcode)
                print pcode.strip(), " -- ", result
        print "--------------------"
    except IOError:
        raise Exception("File '%s' not present" % filename)


'''
Sample output:

# python uk_postcode_validator.py
--------------------
Post-code -- Result
--------------------
B338TH  --  True
B601LU  --  True
B976AF  --  True
B976GZ  --  True
B976QX  --  True
CR26XH  --  True
DN551PT  --  True
M11AE  --  True
W1A0AX  --  True
--------------------

'''
