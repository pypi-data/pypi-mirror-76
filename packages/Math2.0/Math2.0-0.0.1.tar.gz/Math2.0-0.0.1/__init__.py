#Welcome to Python Module for standard maths
import math

def sum(number1,number2):
    add = number1 + number2
    return add;

def suminf(*x):
    total = 0
    for n in x:
        total += n
    
    return total

def subtract(number_to_subtract_from,number_to_subtract):
    sub = number_to_subtract_from - number_to_subtract
    return sub

def multiply(number1,number2):
    pro = number1*number2
    return pro

def divide(divisor,dividend):
    Quotent = divisor/dividend
    ab = float(Quotent*dividend)
    bc = float(divisor)
    if(ab==bc):
        Remainder = 0
    else:
        Remainder = divisor%dividend
    
    return Quotent,Remainder

def average(number1,number2):
    ab = number1 + number2
    bc = ab/2
    return bc

def prob(No_of_possible_outcomes,total_number_of_outcomes):
    ab = No_of_possible_outcomes
    bc = total_number_of_outcomes
    cd = float(ab/bc)
    return cd

def areaTri(base,height,unit_as_string):
    ab = (base*height)
    bc = float(0.5*ab)
    cd = str(bc)+" "+unit_as_string + " "+"square"
    return cd

def areaRect(length,breadth,unit_as_string):
    ab = float(length*breadth)
    bc = str(ab)
    cd = bc + " " + unit_as_string + " " + "square"
    return cd

def pythagoras(base, perpendicular, hypotenuse):
    if(base=="x"):
        ab = float(hypotenuse*hypotenuse)
        bc = float(perpendicular*perpendicular)
        cd = ab - bc
        da = math.sqrt(cd)
        ef = da
        return ef

    elif(perpendicular=="x"):
        ab = float(hypotenuse*hypotenuse)
        bc = float(base*base)
        cd = ab - bc
        da = math.sqrt(cd)
        ef = da
        return ef

    elif(hypotenuse=="x"):
        ab = float(perpendicular*perpendicular)
        bc = float(base*base)
        cd = ab+bc
        da = math.sqrt(cd)
        ef = da
        return ef


    else:
        return "Wrong Value Provided"
    
def angleTriangle(Angle1,Angle2,Angle3):
    if(Angle1=="x"):
        ab = 180
        bc = float(Angle2 + Angle3)
        cd = float(ab) - bc
        da = cd
        return da

    elif(Angle2=="x"):
        ab = 180
        bc = float(Angle1 + Angle3)
        cd = float(ab) - bc
        da = cd
        return da

    elif(Angle3=="x"):
        ab = 180
        bc = float(Angle1 + Angle2)
        cd = float(ab) - bc
        da = cd
        return da

    else:
        return "Invalid Command Passed"

def angleQuad(L1,L2,L3,L4):
    if(L1=="x"):
        ab = 360
        bc = float(L2 + L3 + L4)
        cd = float(ab) - bc
        da = cd
        return da

    elif(L2=="x"):
        ab = 360
        bc = float(L1 + L3 + L4)
        cd = float(ab) - bc
        da = cd
        return da

    elif(L3=="x"):
        ab = 360
        bc = float(L2 + L1 + L4)
        cd = float(ab) - bc
        da = cd
        return da

    elif(L4=="x"):
        ab = 360
        bc = float(L2 + L3 + L1)
        cd = float(ab) - bc
        da = cd
        return da

    else:
        return "Invalid Command Passed"

def max(num1, num2):
    if(num1>num2):
        return num1
    elif(num1==num2):
        return str(num1)+" "+"="+" "+str(num2)+" "+","+"both are equal."
    elif(num1<num2):
        return num2
    else:
        return "Invalid Values Given"

def min(num1, num2):
    if(num1<num2):
        return num1
    elif(num1==num2):
        return str(num1)+" "+"="+" "+str(num2)+" "+","+"both are equal."
    elif(num1>num2):
        return num2
    else:
        return("Invalid Values Given")



#Ends Here
