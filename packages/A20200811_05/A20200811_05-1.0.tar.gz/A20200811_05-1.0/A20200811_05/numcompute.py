#coding=utf-8
from . import isnumber
def sum(*num):
    '''
    将传入的所有数字加起来，并返回
    :param num: 要传入的参数(可以多种类型)
    :return: 数字参数之和
    '''
    result=0
    for n in num:
        if(isnumber.isNumber(n)):
            result+=n
    return n
def multiple(*num):
    '''
    将传入的所有数字乘起来，并返回
    :param num: 要传入的参数(可以多种类型)
    :return: 数字参数之积
    '''
    result=1
    for n in num:
        if(isnumber.isNumber(n)):
            result*=n
    return n