# Goal is -
#  Write a program that prints the numbers from 1 to 100. But for
#  multiples of three print "Three" instead of the number and for
#  the multiples of five print "Five". For numbers which are multiples
#  of both three and five print "ThreeFive".

import sys

class Solution(object):
    def three_five(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        response = []
        for i in range(1,n+1):
            str = ""
            if i%3 == 0:
                str += "Three"
            if i%5 == 0:
                str += "Five"
            if not str:
                str = "%s" % i
            response.append(str)
        return response

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Provide check number of arguments passed")
    #print sys.argv, type(sys.argv[0])
    arg = int(sys.argv[1])
    cls = Solution()
    print cls.three_five(arg)


'''
Sample Outputs:

# python ThreeFive.py 12
['1', '2', 'Three', '4', 'Five', 'Three', '7', '8', 'Three', 'Five', '11', 'Three']

# python ThreeFive.py 9 00
Traceback (most recent call last):
  File "ThreeFive.py", line 29, in <module>
    raise Exception("Provide check number of arguments passed")
Exception: Provide check number of arguments passed

# python ThreeFive.py
Traceback (most recent call last):
  File "ThreeFive.py", line 29, in <module>
    raise Exception("Provide check number of arguments passed")
Exception: Provide check number of arguments passed

'''
