### File description
# The file contains autofocusing algorithm

from low_level_soft.gpio_objects import bipolar, bipolar_go_0, bipolar_start
from Autofocus.modules_focus.Camera_focus import Capture_image_pi
from Autofocus.modules_focus.Variance import Variance as Focus
from math import sqrt

def Autofocus():
    def Result_focus(k):
        #print(k)
        bipolar(k)
        image = Capture_image_pi()
        return Focus(image)

    def F(n):
        return int(((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5)))

    print("The stage will go down until bottom detected\n\
          then return to focus position\n")
    bipolar_go_0()
    start_focus = 105
    bipolar_start(start_focus)

    print("And now the focusing begins!\n")
    n = 60
    div_step = 0.1
    a = 0
    temp = a
    b = n
    k = 0
    Foc = []
    Coord  = []


    for k in range(0,n):    
        if (k == 0):
            x1 = a + (F(n-k-1)/F(n-k+1))*(b-a)
            Coord.append(x1)
            mv_x1 = x1 - temp
            focus_x1 = Result_focus((mv_x1)*div_step)
            Foc.append(focus_x1)
            temp = x1
               
            x2 = b - (F(n-k-1)/F(n-k+1))*(b-a)
            Coord.append(x2)
            mv_x2 = x2 - temp
            focus_x2 = Result_focus((mv_x2)*div_step)
            Foc.append(focus_x2)
            temp = x2   
        
        if (focus_x1 < focus_x2):
            a = x1
            b = b
            x1 = x2
            focus_x1 = focus_x2
            x2 = b - (F(n-k-1)/F(n-k+1))*(b-a)
            Coord.append(x2)
            mv_x2 = x2 - temp
            focus_x2 = Result_focus((mv_x2)*div_step)
            Foc.append(focus_x2)
            temp = x2
        
        else:
            a = a
            b = x2
            x2 = x1
            focus_x2 = focus_x1
            x1 = a + (F(n-k-1)/F(n-k+1))*(b-a)
            Coord.append(x1)
            mv_x1 = x1 - temp
            focus_x1 = Result_focus((mv_x1)*div_step)
            Foc.append(focus_x1)
            temp = x1
        
        if ((b - a) < 2):###############2
            ind_foc = Foc.index(max(Foc))
            bipolar((Coord[ind_foc]-Coord[len(Coord)-1])*div_step)
            temp = (Coord[ind_foc])
            break

