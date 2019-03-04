#Longxing_Tan
#
import re

a='LE4WG4CB0JL356677 LE40G4GB6JL222160 LE40G4GB6JL208534；'
b=re.findall(r'[0-9a-zA-Z]{11}\d{6}',a)
print(b)