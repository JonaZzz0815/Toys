
import functools
import xlrd
import xlwt
import random
# def my_compare(x,y):
#     if x[1]>y[1]:
#         return 1
#     elif x[1]<y[1]:
#         return -1
#     return 0

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
            #print("try to match std:%d and sec:%d" %(indexStd,indexSec))
            #print(IsStdProposed[indexStd])
            
            if (len(SectionGroup[indexSec])<int(SecCapacity[indexSec])):
                # the section is not full
                IsStdMatched[indexStd] = True
                SectionGroup[indexSec].append([Sec[indexSec].index(indexStd),indexStd])
                Pair[indexStd] = (indexStd,indexSec)
            else:
                # the section is full
                SectionGroup[indexSec].sort()
                #print("Full")
                #print(SectionGroup[indexSec][-1])
                #print(indexStd)
                if (SectionGroup[indexSec][-1][0] > Sec[indexSec].index(indexStd)):
                    # if the section like the student more
                    popone = SectionGroup[indexSec].pop()
                    # pity one being kicked off the section
                    IsStdMatched[popone[1]] = False
                    # add the lucky guy to the group
                    IsStdMatched[indexStd] = True
                    SectionGroup[indexSec].append([Sec[indexSec].index(indexStd),indexStd])
                    Pair[indexStd] = (indexStd,indexSec)
        
    print("after STD Proposing")
    for i in range(NumSec):
        print([ item[1] for item in SectionGroup[i]]) 

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
                print(std)
                if (IsGroupProposed[indexSec][j]== False):
                    indexStd = std
                    break
            IsGroupProposed[indexSec][j] = True
            # have proposed to certain std
            #print("try to match std:%d and sec:%d" %(indexStd,indexSec))
            #print(IsStdProposed[indexStd])
            
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

    print("after SEC Proposing")
    for i in range(NumSec):
        print([ item[1] for item in SectionGroup[i]]) 


def MixedProposing(Std:list,Sec:list,SecCapacity,SecPrefer):
    NumStd = len(Std)
    NumSec = len(Sec)
    IsStdMatched = [False]*NumStd
    Pair = [(-1,-1)]*NumStd
    SectionGroup = [[] for i in range(NumSec)]
    SectionProposing(Std,Sec,SecPrefer,IsStdMatched,Pair,SectionGroup)
    StudentProposing(Std,Sec,SecCapacity,IsStdMatched,Pair,SectionGroup)
    return Pair
    


def Test():
    table = xlrd.open_workbook("Source.xlsx")
    STD_ws = table.sheet_by_index(0)
    SEC_ws = table.sheet_by_index(1)

    Std = []
    for i in range(STD_ws.nrows - 1):
        Std.append(STD_ws.row_values(i+1,2,STD_ws.ncols))
    
    Sec = []
    for i in range(SEC_ws.nrows - 1):
        Sec.append(SEC_ws.row_values(i+1,3,SEC_ws.ncols))

    SecCap = SEC_ws.col_values(2,1,SEC_ws.ncols)
    print(Std)
    print(Sec)
    print(SecCap)
    ans = MixedProposing(Std,Sec,SecCap,5)
    workbook =  xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Mixed Proposing',cell_overwrite_ok=True)

    worksheet.write(0,0,label="index of Student")
    worksheet.write(0,1,label="Name")
    worksheet.write(0,2,label="Section")
    worksheet.write(0,3,label="Preference Rank")

    for i in range(len(Std)):
        worksheet.write(i+1,0,i)
        worksheet.write(i+1,2,ans[i][1])
        worksheet.write(i+1,3,Std[i].index(ans[i][1]))

    workbook.save("MixedResult.xlsx")


if __name__=="__main__":
    # TestMatching1()
    # TestMatching2()
    # TestMatching3()
    Test()

