prop_venn
---------

crates proportional venn diagrams from 2 or 3 files using google charts.
pure python implementation

contains galaxy tool xml (prop_venn.xml)

cli interface expects all arguments for the inputs concatenated
with , i.e. file1,file2,file3  ...

contains an integration test for the cli interface (vennerTest.py), no galaxy unit tests.



Proportional Venn Diagram:
--------------------------
Creates a proportional Venn diagram from 2 or 3 tab delimited input files.
The 0 based column index decides which column is used for extracting the sets to compare between the files.
Multiple items with the same value per column are counted as one.

Requirements:
-------------
- 2-3 tab delimited input files.
- 0 based index of the columns to extract for each file

Outputs:
--------
- Html page with the proportional Venn diagram and a table for the counts in each section.


