import re
from JackToken import *

regex = r">(.*?)</"

def jackAnalyzer():
    token = token_(path_)
    name = path_[0:-5]
    regex = r">(.*?)</"
    analyzer = open(name + '.xml', 'w')
    analyzer.write('<class>\n')
    for word in token:
        re.findall(regex, word)

jackAnalyzer()