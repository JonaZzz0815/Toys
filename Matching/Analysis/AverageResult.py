'''
Author: your name
Date: 2021-06-18 16:53:17
LastEditTime: 2021-06-19 16:48:29
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /Toys/Matching/Analysis/AverageResult.py
'''
import functools
import xlrd
import xlwt
import random

def GenerateData(num_std,num_section,RandomFun1,RandomFun2):
    ApplicantsPreference = [[ j for j in range(num_section)] for i in range(num_std)]

    for i in range(0,num_std):
        random.shuffle(ApplicantsPreference[i],RandomFun1)
        #print(ApplicantsPreference[i])

    DepartmentPreference = [ [j for j in range(num_std)] for i in range(num_section)]

    for i in range(0,num_section):
        random.shuffle(DepartmentPreference[i],RandomFun2)
        #print(DepartmentPreference[i])
            
    return [ApplicantsPreference , DepartmentPreference]


def StudentProposing(Std:list,Sec:list,SecCapacity:list,IsStdMatched:list,Pair:list,SectionGroup:list):
    # std and sec give preference from best to worst
    """ 
    The input of this function is defined by two lists Student and Section
    Student and Section are numbered 0 through n-1
    Std[i] encodes the ith Students's preferences. It is simply a list
    containing the numbers 0, 1, ... , n-1 in some order
    Sec[i] encodes the ith sections preferences. It is simply a list
    containing the numbers 0, 1,... , n-1 in some order
    The output is defined by a list of pairs of the form (i,j)
    indicating that student i enter certain section
    Your output should be the student-optimal stable matching found by the
    GS-algorithm. 
    """
    NumStd = len(Std)
    NumSec = len(Sec)
    # IsStdMatched = [False]*NumStd
    IsStdProposed = [ [False for i in range(NumSec)] for j in range(NumStd)]
    # Pair = [(-1,-1)]*NumStd
    # SectionGroup = [[] for i in range(NumSec)]

    while(False in IsStdMatched):
        indexStd = IsStdMatched.index(False)
        if (False in IsStdProposed[indexStd]):
            # find the section not being proposed
            indexSec = -1
            for i in range(NumSec):
                sec = int(Std[indexStd][i])
                if (IsStdProposed[indexStd][sec]== False):
                    indexSec = sec
                    break
            IsStdProposed[indexStd][indexSec] = True
            # have proposed to join certain section
            
            if (len(SectionGroup[indexSec])<int(SecCapacity[indexSec])):
                # the section is not full
                IsStdMatched[indexStd] = True
                SectionGroup[indexSec].append([Sec[indexSec].index(indexStd),indexStd])
                Pair[indexStd] = (indexStd,indexSec)
            else:
                # the section is full
                SectionGroup[indexSec].sort()
                if (SectionGroup[indexSec][-1][0] > Sec[indexSec].index(indexStd)):
                    # if the section like the student more
                    popone = SectionGroup[indexSec].pop()
                    # pity one being kicked off the section
                    IsStdMatched[popone[1]] = False
                    # add the lucky guy to the group
                    IsStdMatched[indexStd] = True
                    SectionGroup[indexSec].append([Sec[indexSec].index(indexStd),indexStd])
                    Pair[indexStd] = (indexStd,indexSec)

def SectionProposing(Std:list,Sec:list,SecCapacity,IsStdMatched:list,Pair:list,SectionGroup:list):
    # std and sec give preference from best to worst
    """ 
    The input of this function is defined by two lists Student and Section
    Student and Section are numbered 0 through n-1
    Std[i] encodes the ith Students's preferences. It is simply a list
    containing the numbers 0, 1, ... , n-1 in some order
    Sec[i] encodes the ith sections preferences. It is simply a list
    containing the numbers 0, 1,... , n-1 in some order
    The output is defined by a list of pairs of the form (i,j)
    indicating that student i enter certain section
    Your output should be the Section-optimal stable matching found by the
    GS-algorithm. 
    """
    NumStd = len(Std)
    NumSec = len(Sec)
    # IsStdMatched = [False]*NumStd
    IsSecFull = [False]*NumSec
    IsGroupProposed = [ [False for i in range(SecCapacity)] for j in range(NumSec)]
    # Pair = [(-1,-1)]*NumStd
    # SectionGroup = [[] for i in range(NumSec)]

    while(False in IsSecFull):
        indexSec = IsSecFull.index(False)
        if (False in IsGroupProposed[indexSec]):
            # find the section not being proposed
            indexStd = -1
            j = 0
            for j in range(SecCapacity):
                std = int(Sec[indexSec][j])
                if (IsGroupProposed[indexSec][j]== False):
                    indexStd = std
                    break
            IsGroupProposed[indexSec][j] = True
            
            if (IsStdMatched[indexStd]== False):
                # the section is not full
                IsStdMatched[indexStd] = True
                SectionGroup[indexSec].append([Sec[indexSec].index(indexStd),indexStd])
                Pair[indexStd] = (indexStd,indexSec)
            else:
                indexSec1 = -1
                for j in range(NumStd):
                    if (Pair[j][0] == indexStd):
                        indexSec1 = Pair[j][1]
                        break
                if (Std[indexStd].index(indexSec)<Std[indexStd].index(indexSec1)):
                    # std like the section more
                    # pity section remove std
                    SectionGroup[indexSec1].remove([Sec[indexSec1].index(indexStd),indexStd])
                    # lucky section get the std
                    SectionGroup[indexSec].append([Sec[indexSec].index(indexStd),indexStd])
                    Pair[indexStd] = (indexStd,indexSec)
        for i in range(NumSec):
            if (False in IsGroupProposed[i]):
                IsSecFull[i]= False
            else:
                IsSecFull[i]= True

def ApplicantProposing(Std:list,Sec:list,SecCapacity,SecPrefer):
    NumStd = len(Std)
    NumSec = len(Sec)
    IsStdMatched = [False]*NumStd
    Pair = [(-1,-1)]*NumStd
    SectionGroup = [[] for i in range(NumSec)]
    
    StudentProposing(Std,Sec,SecCapacity,IsStdMatched,Pair,SectionGroup)
    return Pair

def DepartmentProposing(Std:list,Sec:list,SecCapacity,SecPrefer):
    # std and sec give preference from best to worst
    """ 
    The input of this function is defined by two lists Student and Section
    Student and Section are numbered 0 through n-1
    Std[i] encodes the ith Students's preferences. It is simply a list
    containing the numbers 0, 1, ... , n-1 in some order
    Sec[i] encodes the ith sections preferences. It is simply a list
    containing the numbers 0, 1,... , n-1 in some order
    The output is defined by a list of pairs of the form (i,j)
    indicating that student i enter certain section
    Your output should be the Section-optimal stable matching found by the
    GS-algorithm. 
    """
    NumStd = len(Std)
    NumSec = len(Sec)
    IsStdMatched = [False]*NumStd
    IsSecFull = [False]*NumSec
    IsGroupProposed = [ [False for i in range(NumStd)] for j in range(NumSec)]
    Pair = [(-1,-1)]*NumStd;
    SectionGroup = [[] for i in range(NumSec)];

    while(False in IsSecFull):
        indexSec = IsSecFull.index(False)
        if (False in IsGroupProposed[indexSec]):
            # find the section not being proposed
            indexStd = -1
            for i in range(NumStd):
                std = int(Sec[indexSec][i])
                if (IsGroupProposed[indexSec][std]== False):
                    indexStd = std
                    break
            IsGroupProposed[indexSec][indexStd] = True
            
            if (IsStdMatched[indexStd]== False):
                # the section is not full
                IsStdMatched[indexStd] = True
                SectionGroup[indexSec].append(indexStd)
                Pair[indexStd] = (indexStd,indexSec)
            else:
                indexSec1 = -1
                for j in range(NumStd):
                    if (Pair[j][0] == indexStd):
                        indexSec1 = Pair[j][1]
                        break
                if (Std[indexStd].index(indexSec)<Std[indexStd].index(indexSec1)):
                    # std like the section more
                    # pity section remove std
                    SectionGroup[indexSec1].remove(indexStd)
                    # lucky section get the std
                    SectionGroup[indexSec].append(indexStd)
                    Pair[indexStd] = (indexStd,indexSec)
        for i in range(NumSec):
            if (len(SectionGroup[i])<int(SecCapacity[i])):
                IsSecFull[i]= False
            else:
                IsSecFull[i]= True
    return Pair

    
def MixedProposing(Std:list,Sec:list,SecCapacity,SecPrefer):
    NumStd = len(Std)
    NumSec = len(Sec)
    IsStdMatched = [False]*NumStd
    Pair = [(-1,-1)]*NumStd
    SectionGroup = [[] for i in range(NumSec)]
    SectionProposing(Std,Sec,SecPrefer,IsStdMatched,Pair,SectionGroup)
    StudentProposing(Std,Sec,SecCapacity,IsStdMatched,Pair,SectionGroup)
    return Pair

def Analysis(Result:list,APreference:list,Pair:list):
    for i in range(len(Pair)):
        now_pair = Pair[i]
        Result[APreference[now_pair[0]].index(now_pair[1])] += 1

def RandomFunc1():
    return random.random()
def RandomFunc2():
    return random.betavariate(2,2)
def RandomFunc3():
    return random.betavariate(0.5,0.5)
def RandomFunc4():
    return random.betavariate(5,1)
def RandomFunc5():
    return random.betavariate(1,3)
def FormatForLatex(Result:list):
    for item in Result:
        print("\t",end="")
        print(item,end="")
        print("&",end="")
    print()

def TestWithRandomFunc(RandomFunc1,RandomFunc2,FuncName):
    ApplicantResult = [0 for i in range(5)]
    DepartmentResult = [0 for i in range(5)]
    MixedResult = [0 for i in range(5)]
    DepCap = [10 for i in range(5)]
    SetNum = 1000
    for i in range(SetNum):
        # print("generating ",end="")
        # print(i)
        # generate data with random distribution 
        ans = GenerateData(50,5,RandomFunc1,RandomFunc2)
        APreference = ans[0]
        DPreference = ans[1]
        # Applicant Proposing
        pair = ApplicantProposing(APreference,DPreference,DepCap,10) 
        Analysis(ApplicantResult,APreference,pair)
        # Department Proposing
        pair = DepartmentProposing(APreference,DPreference,DepCap,10) 
        Analysis(DepartmentResult,APreference,pair)
        # Mixed Proposing
        pair = MixedProposing(APreference,DPreference,DepCap,10) 
        Analysis(MixedResult,APreference,pair)
    
    for i in range(5):
        ApplicantResult[i] /=SetNum
        DepartmentResult[i] /=SetNum
        MixedResult[i] /=SetNum
    print("Result with RandomFunc: "+FuncName)
    FormatForLatex(ApplicantResult)
    FormatForLatex(DepartmentResult)
    FormatForLatex(MixedResult)

    # print(ApplicantResult)
    # print(DepartmentResult)
    # print(MixedResult)


if __name__=="__main__":
    TestWithRandomFunc(RandomFunc1,RandomFunc1,"Even+Even")
    # TestWithRandomFunc(RandomFunc2,RandomFunc1,"Beta(2,2)+Even")
    # TestWithRandomFunc(RandomFunc3,RandomFunc1,"Beta(0.5,0.5)+Even")
    TestWithRandomFunc(RandomFunc4,RandomFunc1,"Beta(5,1)+Even")
    TestWithRandomFunc(RandomFunc5,RandomFunc1,"Beta(1,3)+Even")

    TestWithRandomFunc(RandomFunc1,RandomFunc4,"Even+Beta(5,1)")
    # TestWithRandomFunc(RandomFunc2,RandomFunc1,"Beta(2,2)+Even")
    # TestWithRandomFunc(RandomFunc3,RandomFunc1,"Beta(0.5,0.5)+Even")
    # TestWithRandomFunc(RandomFunc4,RandomFunc4,"Beta(5,1)+Beta(5,1)")
    # TestWithRandomFunc(RandomFunc5,RandomFunc4,"Beta(1,3)+Beta(5,1)")
    
    TestWithRandomFunc(RandomFunc1,RandomFunc5,"Even+Beta(1,3)")
    # TestWithRandomFunc(RandomFunc2,RandomFunc1,"Beta(2,2)+Even")
    # TestWithRandomFunc(RandomFunc3,RandomFunc1,"Beta(0.5,0.5)+Even")
    # TestWithRandomFunc(RandomFunc4,RandomFunc5,"Beta(5,1)+Beta(1,3)")
    # TestWithRandomFunc(RandomFunc5,RandomFunc4,"Beta(1,3)+Beta(1,3)")

