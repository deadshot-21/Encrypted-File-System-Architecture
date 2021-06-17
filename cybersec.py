import os
import pickle
import random 
import string
import binascii
import base64
from twofish import Twofish

IMP = dict()
PATH = dict()
EX = dict()
KEY = dict()
LIST = dict()

def listToString(l):
    s = ''
    for char in l:
        s+=str(char)
    return s
def listToStringD(l):
    s = ''
    for char in l:
        s+=str(char.decode('utf8'))
    return s

def equilizer(n, data, FileName):
    rem = len(data)//n
    list=[]
    k=0
    j=n
    for i in range(rem+1):
        if i == rem:
            x = len(data[k:])
            y = n - x
            EX[FileName]=y
            sub = rand_pass(y)
            temp = data[k:]+sub
            list.append(temp)
            break
        temp = data[k:j]
        k+=n
        j+=n
        list.append(temp)
    clist = twofishEn(list,FileName)
    return clist

def dequilizer(FileName):
    plist=[]
    clist = LIST[FileName]
    key = KEY[FileName]
    t = Twofish(key)
    for byte in clist:
        plist.append((t.decrypt(byte)))
    z = EX[FileName]
    n = len(clist[0])
    y = n - z
    tot = len(clist)
    temp = plist[tot-1]
    temp = temp[:y]
    plist[tot-1] = temp
    return plist
        
def rand(size):
    ra = base64.b16encode(random.getrandbits(size).to_bytes(16, byteorder='little'))
    return ra
def rand_pass(size): 
    generate_pass = ''.join([random.choice( string.ascii_uppercase + string.ascii_lowercase + string.digits)for n in range(size)]) 
    return generate_pass

def twofishEn(elist,FileName):
    key = rand(16)
    key = binascii.unhexlify(key)
    KEY[FileName]=key
    t = Twofish(key)
    clist = []
    for bits in elist:
        clist.append((t.encrypt(bits.encode('utf8'))))
    return clist


def MisplaceData(data):
    if len(data)%2!=0:
        data+='`'
    rev = data[::-1]
    even = rev[0::2]
    odd = rev[1::2]
    return even + odd

def AntiMisplaceData(data):
    even = list(data[:len(data)//2])
    odd = list(data[len(data)//2:])
    final = [even,odd]
    string=[]
    for j in range(len(final[0])):
        for i in range(2):
            string.append(final[i][j])
    for char in string:
        if char == '`':
            string.remove('`')
    str1 = ''
    return str1.join(string[::-1])

def Mail(receiver_email,OTP):
    import smtplib, ssl
    from email.message import EmailMessage
    port = 465  
    smtp_server = "smtp.gmail.com"
    sender_email = "YOUR EMAIL"
    password = 'YOUR PASSWORD'
    msg = EmailMessage()
    msg.set_content('YOUR OTP FOR ACCESSING THE FILE IS {}'.format(OTP))
    msg['Subject'] = 'OTP'
    msg['From'] = 'YOUR EMAIL'
    msg['To'] = receiver_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)

def rand_pass(size): 
    generate_pass = ''.join([random.choice( string.ascii_uppercase + string.ascii_lowercase + string.digits)for n in range(size)]) 
    return generate_pass 

######################################### DRIVER CODE #################################################################

parent_dir = 'V:\Cyber Security Project'
IMP = pickle.load(open(parent_dir+'/save1.p','rb'))
PATH = pickle.load(open(parent_dir+'/save2.p','rb'))
EX = pickle.load(open(parent_dir+'/save3.p','rb'))
KEY = pickle.load(open(parent_dir+'/save4.p','rb'))
LIST = pickle.load(open(parent_dir+'/save5.p','rb'))
os.chdir(parent_dir)
choice = 0
while choice!=4:
    print(' WELCOME ')
    print('1: HEAD')
    print('2: MANAGER')
    print('3: EMPLOYEE')
    print('4: EXIT')
    choice = int(input('ENTER YOUR CHOICE: '))
    if choice == 1:
        email = 'sohamfaldu@gmail.com'
        path = os.path.join(os.getcwd(),'HEAD')
        temp = 0
        while temp!=5:
            print('1: OPEN FOLDER')
            print('2: SHOW FILE CONTENT')
            print('3: LIST FILES AND FOLDERS')
            print('4: GO BACK')
            print('5: EXIT')
            temp = int(input('ENTER YOUR CHOICE: '))
            if temp == 1:
                name = input('ENTER FOLDER NAME: ').upper()
                if name[0:3] == 'MNG':
                    path = os.path.join(parent_dir,'HEAD',name)
                    print(os.listdir(path))
                elif name[0:3] == 'EMP':
                    mng = input('ENTER MANAGER\'S NAME: ').upper()
                    path = os.path.join(parent_dir,'HEAD',mng,name)
                    print(os.listdir(path))

            elif temp == 2:
                FileName = input('ENTER FILE NAME: ')
                otp = rand_pass(6)
                receiver = email
                Mail(receiver,otp)
                temp_otp = input('ENTER YOUR OTP: ')
                if temp_otp == otp:
                    path = PATH[username]
                    with open(os.path.join(path, FileName)+'.txt', 'r') as fp:
                        x = fp.read()
                        y = dequilizer(FileName)
                        z = listToStringD(y)
                        print(AntiMisplaceData(z))
                    fp.close()
                else:
                    break
            elif temp == 3:
                print(os.listdir(path))
            elif temp==4:
                os.chdir('../')
                
    elif choice == 2:
        temp = 0
        while temp!=3:
            print(' WELCOME ')
            print('1: OLD MANAGER')
            print('2: NEW MANAGER')
            print('3: END')
            temp = int(input('ENTER YOUR CHOICE: '))
            if temp == 2:
                username = input('ENTER YOUR USERNAME: ').upper()
                directory = username
                email = input('ENTER YOUR EMAIL FOR VERIFICATION: ').lower()
                IMP[username]= email
                path = os.path.join(parent_dir, 'HEAD',directory)
                os.mkdir(path)
                PATH[username] = path
                pickle.dump(IMP,open(parent_dir+'/save1.p','wb'))
                pickle.dump(PATH,open(parent_dir+'/save2.p','wb'))
            elif temp == 1:
                username = input('ENTER YOUR USERNAME: ').upper()
                temp1=0
                while temp1!=6:
                    print('1: CREATE FILE')
                    print('2: SHOW FILE CONTENT')
                    print('3: LIST ALL FILE')
                    print('4: DELETE FILE')
                    print('5: REVIEW EMPLOYEE\'S WORK')
                    print('6: EXIT')
                    temp1 = int(input('ENTER YOUR CHOICE: '))
                    if temp1 == 1:
                        path = PATH[username]
                        FileName = input('ENTER FILENAME: ')
                        with open(os.path.join(path, FileName)+'.txt', 'w') as fp:
                            x = input('ENTER THE DATA: ')
                            y = MisplaceData(x)
                            z = equilizer(16,y,FileName)
                            LIST[FileName] = z
                            w = listToString(z)
                            fp.write(w)
                        fp.close()
                        pickle.dump(EX,open(parent_dir+'/save3.p','wb'))
                        pickle.dump(KEY,open(parent_dir+'/save4.p','wb'))
                        pickle.dump(LIST,open(parent_dir+'/save5.p','wb'))
                    elif temp1==2:
                        FileName = input('ENTER FILENAME: ')
                        otp = rand_pass(6)
                        receiver = IMP[username]
                        Mail(receiver,otp)
                        temp_otp = input('ENTER YOUR OTP: ')
                        if temp_otp == otp:
                            path = PATH[username]
                            with open(os.path.join(path, FileName)+'.txt', 'r') as fp:
                                x = fp.read()
                                y = dequilizer(FileName)
                                z = listToStringD(y)
                                print(AntiMisplaceData(z))
                            fp.close()
                        else:
                            break
                    elif temp1==3:
                        path = PATH[username]
                        print(os.listdir(path))
                    elif temp1==4:
                        FileName=input('ENTER FILENAME: ')
                        path = PATH[username]
                        os.remove(os.path.join(path, FileName)+'.txt')
                    elif temp1==5:
                        t=0
                        path = os.path.join(parent_dir,'HEAD',username)
                        print(os.listdir(path))
                        while t!=4:
                            print('1: LIST CONTENTS OF AN EMPLOYEE\'S FOLDER')
                            print('2: OPEN FILE OF AN EMPLOYEE')
                            print('3: GO BACK')
                            print('4: EXIT')
                            t = int(input('ENTER YOUR CHOICE: '))
                            if t == 1:
                                emp = input('ENTER EMPLOYEE\'S USERNAME: ').upper()
                                path = os.path.join(parent_dir,'HEAD',username,emp)
                                print(os.listdir(path))
                            elif t == 2:
                                emp = input('ENTER EMPLOYEE\'S USERNAME: ').upper()
                                path = os.path.join(parent_dir,'HEAD',username,emp)
                                fn = input('ENTER FILENAME: ')
                                otp = rand_pass(6)
                                receiver = IMP[username]
                                Mail(receiver,otp)
                                temp_otp = input('ENTER YOUR OTP: ')
                                if temp_otp == otp:
                                    with open(os.path.join(path, fn)+'.txt', 'r') as fp:
                                        x = fp.read()
                                        y = dequilizer(fn)
                                        z = listToStringD(y)
                                        print(AntiMisplaceData(z))
                                    fp.close()
                            elif t==3:
                                os.chdir('../')
                    
    elif choice == 3:
        temp=0
        while temp!=3 :
            print(' WELCOME ')
            print('1: OLD EMPLOYEE')
            print('2: NEW EMPLOYEE')
            print('3: END')
            temp = int(input("YOUR CHOICE: "))
            if temp == 2:
                username = input('ENTER YOUR USERNAME = ').upper()
                directory = username
                email = input('ENTER YOUR EMAIL FOR VERIFICATION = ').lower()
                IMP[username]= email
                temp_mng = input('ENTER YOUR MANAGER\'S USERNAME: ').upper()
                path = os.path.join(parent_dir,'HEAD',temp_mng, directory)
                os.mkdir(path)
                PATH[username] = path
                pickle.dump(IMP,open(parent_dir+'/save1.p','wb'))
                pickle.dump(PATH,open(parent_dir+'/save2.p','wb'))
            elif temp == 1:
                username = input('ENTER YOUR USERNAME = ').upper()
                temp1=0
                while temp1!=5:
                    print('1: CREATE FILE')
                    print('2: SHOW FILE CONTENT')
                    print('3: LIST ALL FILE')
                    print('4: DELETE FILE')
                    print('5: EXIT')
                    temp1 = int(input('ENTER YOUR CHOICE: '))
                    if temp1 == 1:
                        path = PATH[username]
                        FileName = input('ENTER FILENAME = ')
                        with open(os.path.join(path, FileName)+'.txt', 'w') as fp:
                            x = input('ENTER THE DATA: ')
                            y = MisplaceData(x)
                            z = equilizer(16,y,FileName)
                            LIST[FileName] = z
                            w = listToString(z)
                            fp.write(w)
                        fp.close()
                        pickle.dump(EX,open(parent_dir+'/save3.p','wb'))
                        pickle.dump(KEY,open(parent_dir+'/save4.p','wb'))
                        pickle.dump(LIST,open(parent_dir+'/save5.p','wb'))
                    elif temp1==2:
                        FileName = input('ENTER FILENAME = ')
                        otp = rand_pass(6)
                        receiver = IMP[username]
                        Mail(receiver,otp)
                        temp_otp = input('ENTER YOUR OTP: ')
                        if temp_otp == otp:
                            path = PATH[username]
                            with open(os.path.join(path, FileName)+'.txt', 'r') as fp:
                                x = fp.read()
                                y = dequilizer(FileName)
                                z = listToStringD(y)
                                print(AntiMisplaceData(z))
                            fp.close()
                        else:
                            break
                    elif temp1==3:
                        path = PATH[username]
                        print(os.listdir(path))
                    elif temp1==4:
                        FileName=input('ENTER FILENAME = ')
                        path = PATH[username]
                        os.remove(os.path.join(path, FileName)+'.txt')

    
