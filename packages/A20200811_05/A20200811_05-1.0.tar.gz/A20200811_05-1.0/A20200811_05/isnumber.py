#coding=utf-8
# 测试是否为数字
def isNumber(x):
    '''
    测试一个字符串是否为数字
    :param x: 要测试的字符串
    :return: True，表示是数字，Flase，表示不是数字
    '''
    if(type(x)==type(1)):
        return True;
    elif(type(x)==type("")):
        if (0 <= str(x).count(".") <= 1):
            if (str(x).replace(".", "").isdigit()):
                return True;
    return False
