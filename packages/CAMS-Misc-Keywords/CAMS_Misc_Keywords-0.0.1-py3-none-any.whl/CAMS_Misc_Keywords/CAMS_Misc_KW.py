def Convert(string): 
    ConvLst = list(string.split(" ")) 
    return ConvLst 

def StrPos(str,fnd): 
    pos = 0

    ind = str.find(fnd)
    pos += str.find(fnd)
    return pos

def getUniqueItems(iterable):
  for x in ints_list:
      if ints_list.count(x) > 1:
         ints_list.remove(x)

  return result