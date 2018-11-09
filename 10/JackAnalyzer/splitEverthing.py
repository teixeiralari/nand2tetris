import re


def split(a):
        mylist = []
        for i in a:
                token = re.findall(r'''[\w']+|[/{}&~=\[\]<>+*|\-().,!?;]|"[^"]*"''', i)#re.findall(r'''[\w']+|[{}=\[\]<>/+-*|().,!?;]|"[^"]*"''',i)
                mylist.append(token)

        flat_list = [] 
        for sublist in mylist:
                for item in sublist:
                        flat_list.append(item)
        return flat_list


