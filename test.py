dicto = {}

def myFunc(var1):
    return dicto[var1]

def maker(fun1):
    def wrapper(var1):
        dicto[var1]=0
        func = fun1(var1)
        return func
    return wrapper


#functionToCall = maker(myFunc)
#functionToCall('a')
#print(dicto)


def otherFun(label,*args,**kwargs):
    print(defaultDict[kwargs['key']])
    return defaultDict[kwargs['key']]

defaultDict = {}

def numInputWrapper(stInuputFunction):
    def wrapper(label, *args, **kwargs):
        defaultDict[kwargs['key']] = 0
        inputWidget = stInuputFunction(label,*args,**kwargs)
        #jsonValues[kwargs['key']] = inputWidget
        return inputWidget
    
    return wrapper
numInput = numInputWrapper(otherFun)
numInput('a',key='b')
print(defaultDict)