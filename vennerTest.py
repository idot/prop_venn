'''
Created on Jul 13, 2010

@author: Ido M. Tamir
'''
import unittest
import venner

'''By hand:
A:
1    A
2    B
3    C
4    D
6    A
7    A
8    E

B:
1    D
2    A
3    E
5    F

C:
4    C
5    D
2    A
3    A
8    F
9    G

A B C:
A = ABCDE 5
B = ADEF 4
AB unique = ABCDEF 6
C = ACDFG 5
ABC unique = ABCDEFG 7

Venn AB
A I B = ADE 2
A \ B = BC 2
B \ A = F 1
Sum = 6

Venn ABC
A \ ( B U C ) = B 1
B \ ( A U C ) =   0
C \ ( A U B ) = G 1
A I B \ C = E 1
A I C \ B = C 1
B I C \ A = F 1
A I B I C = AD 2
Sum = 7

A I B = ADE 3
A I C = ACD 3
B I C = ADF 3


'''


class Test(unittest.TestCase):


    def testTwo(self):
         venn = venner.Venn2("", 300, venner.VennFile("testFiles/fileA.tab",1,"As"), venner.VennFile("testFiles/fileB.tab", 1, "Bs"))
         url = venn.toUrl()
         self.assertEquals("""http://chart.apis.google.com/chart?cht=v&chd=t:56,44,0,33&chtt=&chs=300x300&chdl=As|Bs""", url)
         actual = venn.toHtml()
         expected = open('testFiles/out.2.expected.html', 'r').read()
         self.assertEquals(expected, actual)
         
    def testThree(self):
         venn = venner.Venn3("", 300, venner.VennFile("testFiles/fileA.tab",1,"As"), venner.VennFile("testFiles/fileB.tab", 1, "Bs"), venner.VennFile("testFiles/fileC.tab", 1, "Cs"))
         url = venn.toUrl()
         self.assertEquals("""http://chart.apis.google.com/chart?cht=v&chd=t:36,29,36,21,21,21,14&chtt=&chs=300x300&chdl=As|Bs|Cs""",url)
         actual = venn.toHtml()
         expected = open('testFiles/out.3.expected.html', 'r').read()
         self.assertEquals(expected, actual)
                  
         

if __name__ == "__main__":
    unittest.main()