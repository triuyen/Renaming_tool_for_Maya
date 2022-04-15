import sys
import imp

# PUT in DIECTOY BELOW
dir1 = ['C:/Users/Tri Uyen/Desktop/Tools_Developped/renaming']

for each in dir1:   
    if each not in sys.path:
        sys.path.append(each)
    else:
        pass


import renaming_sys
imp.reload(renaming_sys)
