
ERR_CONTAINER=-1
def convert_container_character(character):
    if character=='A' or character=='a':
        return 10
    if character>='B' and character<='K':
        return (ord(character)-ord('B')+12)
        
    if character>='L' and character<='U':
        return (ord(character)-ord('L')+23)
        
    if character>='V' and character<='Z':
        return (ord(character)-ord('V')+34)
        
    if character>='b' and character<='k':
        return (ord(character)-ord('b')+12)
        
    if character>='l' and character<='u':
        return (ord(character)-ord('l')+23)
        
    if character>='v' and character<='z':
        return (ord(character)-ord('v')+34)
        
    if character>='0' and character<='9':
        return (ord(character)-ord('0'))
    return ERR_CONTAINER   

def convert_container_number(container_number_string):
    container_number_digital=[]
    container_number_string=container_number_string[0:11]
    for i in container_number_string:
        container_number_digital.append(convert_container_character(i))
    return container_number_digital
'''计算箱号最后一位的值'''
def cal_container_check_mark(container_number_string):
    if len(container_number_string)!=11:
        print("container_number_string len error")
        return ERR_CONTAINER 
    container_number_digital=convert_container_number(container_number_string)
    if ERR_CONTAINER in container_number_digital :
        return ERR_CONTAINER
    result=0
    for i in range(10):
        result+=container_number_digital[i]*(2**i)
    result=result%11%10
    return result
'''仅仅判断箱号是否正确'''
def verify_container_number(container_number_string):
    cal_result=cal_container_check_mark(container_number_string)
    if cal_result== ERR_CONTAINER:
        return False
    if cal_result==convert_container_character(container_number_string[10]):
        return True
    else :
        return False
'''根据箱号其他位置信息推测index位可能的数字值，仅支持数字值'''   
def delect_container_number(container_number_string,index):
    if index<4 or index>11 :
        print("index error")
        return
    result=[]
    for i in range(10) :
        container=container_number_string[0:index]+str(i)+container_number_string[index+1:]
        if cal_container_check_mark(container)==convert_container_character(container[10]):    
            result.append(container)
    return result   

def test_number(container):
    dd=[]
    print(container)
    for a in range(10):
        s=container[0:4]+str(a)+container[5:]
        #print(s)
        result=cal_container_check_mark(convert_container_number(s))
        #print(result)
        dd.append((a,result))
    for ss in dd:
        print(ss)
def test_index4():
    for i in range(10):
        dd=[]
        print(i,">>>>>>>>>>>")
        for v in range(10):
            r=v*(2**4)+i
            r=r%11%10
            dd.append((v,r))
            print(v,r)
        print("******")
import sys
def parse_cmd():
    l=len(sys.argv)
    print(sys.argv)
    if l==1 :
        print('命令提示：')
        print('-c container_number :cal_container_check_mark')
        print('-v container_number :verify_container_numbe')
        print('-d container_number :delect_container_number from index4 to 10')
        print('-d container_number index:delect_container_number index')
    pass
    if l==3 :
        if sys.argv[1]=="-v" :
            r=verify_container_number(sys.argv[2])
            print('校验集装箱是否正确：',r)
        if sys.argv[1]=="-c" :
            r=cal_container_check_mark(sys.argv[2])
            print('计算结果：',r)
        if sys.argv[1]=="-d" :
            container=sys.argv[2]
            for i in range(4,11):
                print("**start:**")
                print("if change the index[",i,"] ,then valid container number list:",delect_container_number(container,i))
                print("----------------")
    if l==4  :
        container=sys.argv[2]
        i=int(sys.argv[3])
        if sys.argv[1]=="-d" :
            print("**start:**")
            print("if change the index[",i,"] ,then valid container number list:",delect_container_number(container,i))
            print("----------------")
            
            
if __name__=='__main__'    :
        parse_cmd()
