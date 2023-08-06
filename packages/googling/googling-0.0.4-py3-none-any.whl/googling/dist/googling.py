#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   googling.py
@Time    :   2020/08/10 13:35:31
@Author  :   LCB 
@Version :   1.0
@Contact :   2281181505@qq.com
@From    :   
@function :  
'''
# here put the import lib
import calibration 
def description():
    print('thank you for installing our package!')
def camera_calibration(a,b,c):
    d = calibration.real_calibration(a,b,c)
    print("output from realcalibration is : ",d)

if __name__ == "__main__":
    camera_calibration(1,2,3)

