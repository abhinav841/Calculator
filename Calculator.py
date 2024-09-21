from tkinter import *

r=Tk()
r.title("Calculator™")    # (unregistered) trademark
r.geometry("279x471+300+80")
r.resizable(0,0)    # make window unresizable
r.config(bg="#D9D9D9")

v1=StringVar()
Label(r,text="Calculator",bg="#D9D9D9",fg='#333333',font="Dubai 18 bold").place(x=14,y=-5)
v2=StringVar()
g=Entry(r,textvariable=v2,width=13,font="dubai 25",relief=FLAT)
g.place(x=18,y=51)
g.config(state='disabled',disabledforeground="#222222",disabledbackground="#D9D9D9")
h=Entry(r,textvariable=v1,width=26,font="dubai 13",relief=FLAT)
h.place(x=18,y=34)
h.config(state='disabled',disabledforeground="#222222",disabledbackground="#D9D9D9")

Label(r,text=" ",bg="#D9D9D9",font="arial 636").place(x=18,y=95)
Label(r,text="abhinav anand",bg="#D9D9D9",font="dubai 7",fg='grey').place(x=110,y=450)


def operator(opr):    # handles operators
    if v1.get()!='':
        check(opr)
    elif opr in '-(√':
        v1.set(v1.get()+opr)


def undo():    # rolls-back
    v1.set(v1.get()[0:-1])
    if v1.get()=='':
        v2.set('')
    else:
        result()


def clear():    # clears all
    v1.set('')
    v2.set('')


def decimal():    # inserts decimal appropriately
    if length():
        ubox=v1.get()
        if ubox[-1:] in '-+×÷√^()%':
            v1.set(ubox+'0.')
        elif '.' not in ubox:
            v1.set(ubox+'.')
        else:
            for i in ubox[ubox.rfind('.'):]:
                if i in '-+×÷√^()%':
                    v1.set(ubox+'.')
                    break


def number(num):    # inserts numbers
    if length():
        if v1.get()[-1:]=='0' and v1.get()[-2:-1] in '-+×÷√^()%':
            undo()
        v1.set(v1.get()+num)
        result()


def check(opr):    # inerts opertors appropriately
    a=v1.get()
    if a[-1]=='.' or a[-2:-1] not in '-+×÷√^(' and (a[-1] in '-+×÷√^(' and opr in '×÷^)%' or a[-1] in '×÷√^(' and opr=='+') or a[-1]+opr in '-+-' and a[-2:-1] not in '√(×÷^':
        v1.set(a[:-1]+opr)
    elif a[-1] in '0123456789)%' or a[-1] in '-+' and opr in '√(' or a[-1] in '×÷√^(' and opr in '-(√':
        v1.set(a+opr)
    if v1.get()[-1]=='%':
        result()


def length():    # checks number's length for the limit (max. 12)
    a,ubox=0,v1.get().replace(',','')[::-1]
    for i in ubox:
        if i not in '0123456789.':
            break
        a+=1
    if a<12:
        return 1


def power(n,p):    # returns power in rational
    a,b=n
    x,y=p
    if type(a)==complex or type(b)==complex or a<0 and  x/y%1:
        n=(a/b)**(x/y)
        return n.real+eval(f'{n.imag}j'),1
    else:
        if x/y%1:
            p=x/y
        else:
            p=int(x)//int(y)
        try:
            a**float(p),b**float(p)
            return divide(rational(a**p),rational(b**p))
        except:
            return rational((a/b)**(x/y))


def divide(a,b):    # returns division in rational
    return a[0]*b[1],a[1]*b[0]


def multiply(a,b):    # returns multiplication in rational
    return a[0]*b[0],a[1]*b[1]


def addlast(seq):    # returns sum in rational
    nums,comp=[],[]
    for a,b in seq:
        if type(a)==type(b)==int:
            nums+=[(a,b)]
        else:
            comp+=[a/b]
    a,b=0,1
    for i in nums:
        b*=i[1]
    for i in nums:
        a+=b//i[1]*i[0]
    if comp:
        return a/b+sum(comp),1
    else:
        return (a,b) if a%b else (a//b,1)


def rational(num):    # returns rational form
    if type(num)!=str:
        num=str(num)
        if 'e+' in num:
            b=num.find('e')
            num=str(int(num[:b].replace('.',''))*10**(int(num[b+2:])-(num[:b][::-1].find('.') if '.' in num else 0)))
        elif 'e-' in num:
            num=f'%.{int(num[num.find("e")+2:])}f'%eval(num)

    return int(num.replace('.','')),10**(num[::-1].find('.') if '.' in num else 0)


def comma(expr):    # inserts comma wherever necessary
    def co(seq):
        res=''
        for i in seq:
            if res and len(res.replace(',',''))%3==0:
                i=','+i
            res+=i
        return res

    test=''
    while expr:
        if expr[-1] in '-+×÷√^()%':
            i=expr[-1]
        else:
            i=''
            for a in expr[::-1]:
                if a in '-+×÷√^()%':
                    break
                i+=a
            x=i.find('.')+1 if '.' in i else None
            i=(i[:x] if '.' in i else '')+co(i[x:])

        test=i[::-1]+test
        expr=expr[:-len(i.replace(',',''))]
    return test

def roundoff(n):
    a,b=n
    if type(a)==complex and a.imag/a.real<0.000000000000001:
            a=a.real
    if type(b)==complex and b.imag/b.real<0.000000000000001:
            b=b.real
    if type(a/b)==float:
        n='%.16e'%(a/b)
        n=int(n[n.find('e')+1:])
        n=round(a/b,16-n)
    return (a,b) if type(a+b)==complex else rational(n)

def result(equal=0):    # equal argument to check if to auto-correct the expression 

    ubox=v1.get().replace(',','')
    if equal==0:
        v1.set(comma(ubox))

    ubox=ubox.rstrip('.-+×÷√^(')    # to remove leftovers

    # adding '×' at wherever necessary
    expr=''
    for i in ubox:
        if expr and expr[-1] in '0123456789)%' and i in '(√0123456789' and not (i+expr[-1]).isdigit():
            i='×'+i
        expr+=i

    # validating parenthesis
    test=expr
    while '(' in test:
        i=test.rfind('(')
        if ')' in test[i:]:
            test=test[:i]+test[i+test[i:].find(')')+1:]
        else:
            expr+=')'
            test=test[:i]

    if expr.count('(')<expr.count(')'):
        expr=(expr.count(')')-expr.count('('))*'('+expr

    if equal==1:
        v1.set(comma(expr))

    # creating list having numbers and operators separated
    test,term=[],''
    while expr:
        i=expr[0]
        if i in '0123456789.':
            if test and test[-1] in ('-','+'):
                term+=test.pop()
            term+=i
            if expr[1:2] in '-+×÷√^()%':
                if '-' in term and expr[1:2]=='^':
                    test+=['-',rational(term[1:])]
                else:
                    test+=[rational(term)]
                term=''
        else:
            test+=[i]
        expr=expr[1:]

    try:
        #######################################***** evaluating the result *****#######################################
        while any(type(a)!=tuple for a in test):
            if '(' in test:
                br1=len(test)-test[::-1].index('(')-1    # same as rfind but for list
                br2=br1+test[br1:].index(')')+1
                expr=test[br1+1:br2-1]
            else:
                br1,br2=0,len(test)
                expr=test[br1:br2]
            
            while any(type(a)!=tuple for a in expr):
                # conditional statements acc. to operator precedence
                if '√' in expr:
                    x=len(expr)-expr[::-1].index('√')-1
                    expr[x:x+2]=[power(expr[x+1],(1,2))]
                    if x and expr[x-1]=='-':
                        expr[x-1:x+1]=[(-expr[x][0],expr[x][1])]

                elif '%' in expr:
                    x=expr.index('%')
                    expr[x-1:x+1]=[multiply(expr[x-1],(1,100))]

                elif '^' in expr:
                    x=len(expr)-expr[::-1].index('^')-1
                    a,b=expr[x-1],expr[x+1]
                    expr[x-1:x+2]=[power(a,b)]
                    if expr[x-2:x-1]==['-']:
                        expr[x-2:x]=[(-expr[x-1][0],expr[x-1][1])]

                elif '÷' in expr:
                    x=expr.index('÷')
                    expr[x-1:x+2]=[divide(expr[x-1],expr[x+1])]

                elif '×' in expr:
                    x=expr.index('×')
                    expr[x-1:x+2]=[multiply(expr[x-1],expr[x+1])]

                for x,a in enumerate(expr):
                    if type(a)==tuple:
                        expr[x]=roundoff(a)

            test[br1:br2]=[addlast(expr)]
            if br1 and test[br1-1]=='-':
                test[br1-1:br1+1]=[(-test[br1][0],test[br1][1])]

        res=addlast(test)

        if type(res[0]/res[1])==complex:
            v2.set('Complex number')
        else:
            a='%.16e'%(res[0]/res[1])
            a=int(a[a.find('e')+1:])
            res=round(res[0]/res[1],10-(a if a<11 else 10))
            if 'e' not in str(res):
                res=eval(str(res).rstrip('0').rstrip('.'))

            if 0<abs(res)<0.0001 or abs(res)>999999999999:
                res=f'%.7e'%res
                a=res.find('e')
                res=res[:a].rstrip('.0')+res[a:]
    
            if v1.get().rstrip('-√('):
                v2.set(comma(str(res)))
            else:
                v2.set('')

    except ZeroDivisionError:
        if equal:
            v2.set('Not defined')
        else:
            v2.set('Cannot ÷0')

    except OverflowError:    # or simply except:
        v2.set('Overflow')
 # Button functions (as in your original code)
def one(x):
    if x in '-(√' or v1.get() != '':
        v1.set(v1.get() + x)
    check()
    if x == '%':
        result()

def nine():
    v1.set(v1.get()[0:-1])
    if v1.get() == '':
        v2.set('')
    else:
        result()

def clear():
    v1.set('')
    v2.set('')

def add(x):
    if v1.get()[-1:] == '0' and v1.get()[-2:-1] in '-+×÷√^()%':
        nine()
    v1.set(v1.get() + x)
    check()
    result()

def equal():
    o, a = result()
    if o == 3:
        v2.set('Not defined')
    if a != '':
        v1.set(a)

def result():
    try:
        a = v1.get().replace(',', '')
        if a[-1:] in '.-+×÷√^(':
            v2.set('')
        else:
            v2.set(eval(a.replace('×', '*').replace('÷', '/')))  # Simple eval for demonstration
    except ZeroDivisionError:
        v2.set('Cannot ÷0')
    except Exception as e:
        v2.set('Error')
    return 0, v1.get()

# Function to handle key presses
def key_event(event):
    key = event.char  # Get the pressed key
    if key in '0123456789':
        add(key)  # Add digits
    elif key in '+-*/':
        if key == '*':
            add('×')  # Map * to ×
        elif key == '/':
            add('÷')  # Map / to ÷
        else:
            add(key)
    elif key == '\r':  # Enter key is pressed
        equal()  # Perform calculation
    elif key == '\b':  # Backspace key is pressed
        nine()  # Simulate delete (backspace)
    elif key == '.':
        add('.')  # Add decimal
    elif key == '%':
        one('%')  # Add percentage
    elif key.lower() == 'c':
        clear()  # Clear screen
    elif key == '(' or key == ')':
        add(key)  # Add parentheses

# Bind keyboard events
r.bind('<Key>', key_event)

Button(r,text="+",command=lambda:one('+'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=20,y=105)
Button(r,text="-",command=lambda:one('-'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=80,y=105)
Button(r,text="÷",command=lambda:one('÷'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=140,y=105)
Button(r,text="×",command=lambda:one('×'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=200,y=105)
Button(r,text="(",command=lambda:one('('),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=200,y=163)
Button(r,text=")",command=lambda:one(')'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=200,y=221)
Button(r,text="^",command=lambda:one('^'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=200,y=279)
Button(r,text="√",command=lambda:one('√'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=200,y=337)
Button(r,text=".",command=dec,width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=140,y=337)
Button(r,text="<<",command=nine,width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=20,y=337)
Button(r,text="=",command=equal,width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=200,y=395)
Button(r,text="C",command=clear,width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=20,y=395)
Button(r,text="7",command=lambda:add('7'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=20,y=163)
Button(r,text="8",command=lambda:add('8'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=80,y=163)
Button(r,text="9",command=lambda:add('9'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=140,y=163)
Button(r,text="4",command=lambda:add('4'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=20,y=221)
Button(r,text="5",command=lambda:add('5'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=80,y=221)
Button(r,text="6",command=lambda:add('6'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=140,y=221)
Button(r,text="1",command=lambda:add('1'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=20,y=279)
Button(r,text="2",command=lambda:add('2'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=80,y=279)
Button(r,text="3",command=lambda:add('3'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=140,y=279)
Button(r,text="0",command=lambda:add('0'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=80,y=337)
Button(r,text="00",command=lambda:(add('0'),add('0')),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=80,y=395)
Button(r,text="%",command=lambda:one('%'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=140,y=395)
r.mainloop()


Button(r,text="+",command=lambda:operator('+'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=20,y=105)
Button(r,text="-",command=lambda:operator('-'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=80,y=105)
Button(r,text="÷",command=lambda:operator('÷'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=140,y=105)
Button(r,text="×",command=lambda:operator('×'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=200,y=105)
Button(r,text="(",command=lambda:operator('('),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=200,y=163)
Button(r,text=")",command=lambda:operator(')'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=200,y=221)
Button(r,text="^",command=lambda:operator('^'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=200,y=279)
Button(r,text="√",command=lambda:operator('√'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=200,y=337)
Button(r,text=".",command=decimal,width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=140,y=337)
Button(r,text="<<",command=undo,width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=20,y=337)
Button(r,text="=",command=lambda:result(1),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=200,y=395)
Button(r,text="C",command=clear,width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=20,y=395)
Button(r,text="7",command=lambda:number('7'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=20,y=163)
Button(r,text="8",command=lambda:number('8'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=80,y=163)
Button(r,text="9",command=lambda:number('9'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=140,y=163)
Button(r,text="4",command=lambda:number('4'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=20,y=221)
Button(r,text="5",command=lambda:number('5'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=80,y=221)
Button(r,text="6",command=lambda:number('6'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=140,y=221)
Button(r,text="1",command=lambda:number('1'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=20,y=279)
Button(r,text="2",command=lambda:number('2'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=80,y=279)
Button(r,text="3",command=lambda:number('3'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=140,y=279)
Button(r,text="0",command=lambda:number('0'),width=3,height=1,bg="#444444",fg="white",font="calbri 20",relief=FLAT).place(x=80,y=337)
Button(r,text="00",command=lambda:(number('0'),number('0')),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=80,y=395)
Button(r,text="%",command=lambda:operator('%'),width=3,height=1,bg="#666666",fg="white",font="calbri 20",relief=FLAT).place(x=140,y=395)
r.mainloop()

# Abhinav Anand #


