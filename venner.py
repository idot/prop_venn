#!/usr/bin/env python
'''
Created on Jul 13, 2010

Generates Venn diagram from 2 or three input files

one could generate output file that for each row contain the segment
i.e. A, B, AB, AmB, BmA

@author: Ido M. Tamir
'''
from mako.template import Template
from optparse import OptionParser
import urllib,re,sys

class Bunch:
    def __init__(self, d):
        for k, v in d.items():
            if isinstance(v, dict):
                v = Bunch(v)
            self.__dict__[k] = v

class VennFile():
    def __init__(self, filePath, column, name):
        self.filePath = filePath
        self.column = column
        cleanname = re.sub("/","",name)
        self.name = urllib.quote(cleanname, safe="%/:=&?~#+!$,;'@()*[]")
        self.dict = {}
    def read(self):
        dict = {}
        lineNr = 0
        for line in open( self.filePath, 'rb'):
            key = line.split("\t")[self.column].strip()
            linesList = dict.get(key, [])
            linesList.append(line+"\t"+str(lineNr))
            dict[key] = linesList
            lineNr += 1
        self.dict = dict
        return self

class Venn2:
    def __init__(self, title, size, one, two):
        self.one = one.read()
        self.two = two.read()
        self.title = title
        self.size = size
    
    def toUrl(self):
        one_keys = set(self.one.dict.keys())
        two_keys = set(self.two.dict.keys())
        
        keys_one_i_two = one_keys.intersection(two_keys)
       
        total = len(one_keys) + len(two_keys)
        sizes = [len(one_keys), len(two_keys), 0, len(keys_one_i_two)]
        sizes = self.relSizes(sizes, total)
        names = [self.one.name, self.two.name]
        return self.url(total, sizes, names)
  
    def relSizes(self, sizes, total):
        return map(lambda s: str(int(round((s/float(total) * 100)))), sizes)  

    def url(self, total, sizes, names):
        base = "http://chart.apis.google.com/chart?cht=v&chd=t:"
        counts = ",".join(sizes)
        titlep = "&chtt="+self.title
        size = "&chs="+str(self.size)+"x"+str(self.size)
        legend = "&chdl="+"|".join(names)
        url = base+counts+titlep+size+legend
        return url
    
    def toHtml(self):
        one_keys = set(self.one.dict.keys())
        two_keys = set(self.two.dict.keys())
       
        numbers = Bunch({
        "one_keys" : len(set(self.one.dict.keys())),
        "two_keys" : len(set(self.two.dict.keys())),
        "one_only" : len(one_keys.difference(two_keys)),
        "two_only" : len(two_keys.difference(one_keys)),
        "one_i_two" : len(one_keys.intersection(two_keys)),
        })
            
        template = """
<html>
  <head>
     <title>Venn diagram ${title}</title>
  </head>
  <body>
     <h3>${ title }</h3>
     <div>
        <img src="${ url }"/>
     </div>
     <div>
        <table>
           <tr><th>Segment</th><th>Count</th></tr>
           <tr><td>${ one }</td><td>${ n.one_keys }</td></tr>
           <tr><td>${ two }</td><td>${ n.two_keys }</td></tr>
           <tr><td>${ one } \ ${ two }</td><td>${ n.one_only }</td></tr>
           <tr><td>${ two } \ ${ one }</td><td>${ n.two_only }</td></tr>
           <tr><td>${ one } &cap; ${ two }</td><td>${ n.one_i_two }</td></tr>
        </table>
     </div>
  </body>
</html>"""
        result = Template(template).render(one=self.one.name, two=self.two.name, n=numbers, title=self.title, url=self.toUrl())
        return(result)



class Venn3(Venn2):
    def __init__(self, title, size, one, two, three):
        Venn2.__init__(self, title, size, one, two)
        self.three = three.read()
           
    def toUrl(self):
        one_keys = set(self.one.dict.keys())
        two_keys = set(self.two.dict.keys())
        three_keys = set(self.three.dict.keys())

        keys_one_i_two = one_keys.intersection(two_keys)
        keys_one_i_three = one_keys.intersection(three_keys)
        keys_two_i_three = two_keys.intersection(three_keys)
        keys_one_i_two_i_three = one_keys.intersection(two_keys).intersection(three_keys)
        
        total = len(one_keys)+len(two_keys)+len(three_keys)
        sizes = [len(one_keys), len(two_keys), len(three_keys), len(keys_one_i_two), len(keys_one_i_three), len(keys_two_i_three), len(keys_one_i_two_i_three)]
        sizes = self.relSizes(sizes, total)
        names = [self.one.name, self.two.name, self.three.name]
        return self.url(total, sizes, names)

    def toHtml(self):
        one_keys = set(self.one.dict.keys())
        two_keys = set(self.two.dict.keys())
        three_keys = set(self.three.dict.keys())
        
        xa = one_keys.intersection(two_keys)
        xt = two_keys.intersection(three_keys)
        xd = xt.difference(one_keys)
        
        numbers = Bunch({
        "one_keys" : len(set(self.one.dict.keys())),
        "two_keys" : len(set(self.two.dict.keys())),
        "three_keys" : len(set(self.three.dict.keys())),
        "one_only" : len(one_keys.difference(two_keys.union(three_keys))),
        "two_only" : len(two_keys.difference(one_keys.union(three_keys))),
        "three_only" : len(three_keys.difference(one_keys.union(two_keys))),
        "one_two" : len(one_keys.intersection(two_keys).difference(three_keys)),
        "one_three" : len(one_keys.intersection(three_keys).difference(two_keys)),
        "two_three" : len(two_keys.intersection(three_keys).difference(one_keys)),
        "one_i_two_i_three" : len(one_keys.intersection(two_keys).intersection(three_keys))
        })
            
        template = """
<html>
  <head>
     <title>Venn diagram ${title}</title>
  </head>
  <body>
     <h3>${ title }</h3>
     <div>
        <img src="${ url }"/>
     </div>
     <div>
        <table>
           <tr><th>Segment</th><th>Count</th></tr>
           <tr><td>${ one }</td><td>${ n.one_keys }</td></tr>
           <tr><td>${ two }</td><td>${ n.two_keys }</td></tr>
           <tr><td>${ three }</td><td>${ n.three_keys }</td></tr>
           <tr><td>${ one } \ (${ two } &cup; ${ three })</td><td>${ n.one_only }</td></tr>
           <tr><td>${ two } \ (${ one } &cup; ${ three})</td><td>${ n.two_only }</td></tr>
           <tr><td>${ three } \ (${ one } &cup; ${ two })</td><td>${ n.three_only }</td></tr>
           <tr><td>${ one } &cap; ${ two } \ ${ three } </td><td>${ n.one_two }</td></tr>
           <tr><td>${ one } &cap; ${ three } \ ${ two } </td><td>${ n.one_three }</td></tr>
           <tr><td>${ two } &cap; ${ three } \ ${ one } </td><td>${ n.two_three }</td></tr>
           <tr><td>${ one } &cap; ${ two } &cap; ${ three }</td><td>${ n.one_i_two_i_three }</td></tr>
        </table>
     </div>
  </body>
</html>"""
        result = Template(template).render(one=self.one.name, two=self.two.name, three=self.three.name, n=numbers, title=self.title, url=self.toUrl())
        return(result)




def main():
        '''main worker func'''
        parser = OptionParser()
        parser.add_option( "--files", dest="filePaths", help="file paths delimited by ,")
        parser.add_option( "--columns", dest="columns", help="0 based columnIndices delimited by ,")
        parser.add_option( "--asNames", dest="asNames", help="names of the columns for pretty print")
        parser.add_option( "--title", dest="title", help="title of plot")
        parser.add_option( "--size", dest="size", help="size plot, default 300")
        parser.add_option( "--outname", dest="outfileHtml", help="path of generated html file")
        
        (o, args) = parser.parse_args()
        errors = []
        if o.filePaths is None:
            errors.append("please add required paths to files")
        if o.columns is None:
            errors.append( "please add required columns" )
        if o.asNames is None:
            errors.append( "please add required asNames")
        if len(errors) > 0:
            print("\n".join(errors))
            sys.exit()
        filePaths = o.filePaths.split(",")
        columns = o.columns.split(",")
        columns = map(int, columns)
        asNames = o.asNames.split(",")
        if len(errors) > 0 and ( len(filePaths) != len(columns) or len(columns) != len(asNames) ):
            errors.append( "different length of filePaths, columns or names:" +o.columns+" "+" "+o.names+" "+o.filePaths )
        title = ""
        if o.title:
            title = o.title
        if o.outfileHtml is None:
            errors.append( "please add outfile name for html" )
        if len(filePaths) > 3:
            errors.append( "can only compare up to three files was:"+str(len(filePaths)))
        if len(filePaths) == 1:
            errors.append( "just one file to compare does not make sense!")
        if len(errors) > 0:
            print("\n".join(errors))
            sys.exit()
        
        size = "300"
        if o.size:
            size = o.size
        
        fileCount = len(filePaths)
        if fileCount == 2:
            venn = Venn2(title, size, VennFile(filePaths[0],columns[0],asNames[0]), VennFile(filePaths[1], columns[1], asNames[1]))
        else:
            venn = Venn3(title, size, VennFile(filePaths[0],columns[0],asNames[0]), VennFile(filePaths[1], columns[1], asNames[1]), VennFile(filePaths[2],columns[2],asNames[2]))
        htmlText = venn.toHtml()
        html = open(o.outfileHtml, 'w')
        try:
            html.write(htmlText)
        finally:
            html.close()

               
        
        
if __name__ == '__main__':
      main()

#$ python venner.py --files testFiles/fileA.tab,testFiles/fileB.tab --columns 1,1 --outname out.html --asNames As,Bs
                                               
