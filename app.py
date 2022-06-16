import cv2
import os
import numpy as np
import RPi.GPIO as GPIO
import time
from flask import Flask, redirect, url_for, render_template, request
#app = Flask(__name__, static_url_path='/static')
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT) # blue
GPIO.setup(17,GPIO.OUT) # yellow
GPIO.setup(7,GPIO.OUT) # red


def your_name():
	yn = txt.get() 
	lbl2.configure(text="your name: "+yn) 
	messagebox.showinfo("name",yn) 

def f():
    os.system("python 03_face_recognition.py")
    return 1


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/owner', methods=['GET', 'POST'])
def  owner():
    if request.method == 'GET':
        #Informatin data from infor.txt
        f1 = open('/home/pi/fdCam/userInformation/infor.txt', 'r')
        inforArray = [] #user inform array
        while True:
            line = f1.readline()
            if not line: break
            inforArray.append(line)
        f1.close()
        print(inforArray)
        
        #who is Owner?
        f2 = open('/home/pi/fdCam/owner/owner.txt', 'r')
        # if owner file is null return '' 
        # if owner file  is not null reutnr <owner>\n'
        
        owner = f2.readline()
        f2.close()
        print(owner)
        return render_template('owner.html', inform = inforArray, ownerId = owner)
    
    elif request.method == 'POST':
        userId = request.form['id'] # id entered by user
        # write 
        f1 = open('/home/pi/fdCam/owner/owner.txt', 'w')
        
        f1.write("{0}\n".format(userId))
        f1.close()
        return redirect(url_for('home'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        name = request.form['name'] # Name entered by user
        # Read an existing member from a file
        id = 0
        f1 = open('/home/pi/fdCam/userInformation/infor.txt', 'r')
        id = len(f1.readlines())
        
        sub_face_id = 0
        if  f1.tell() == 1: # tell() is current Cursor point
            f2 = open('/home/pi/fdCam/userInformation/infor.txt', 'w')
            f2.write("{0} {1}\n".format(1, name))
            sub_face_id = 1
        else:
            f2 = open('/home/pi/fdCam/userInformation/infor.txt', 'a')
            f2.write("{0} {1}\n".format(id+1, name))
            sub_face_id = id+1
        
        f2.close() 
        f1.close
        
        #### Start: Collect data from new user with opencv and Create a new model!
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height
        face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

        face_id = sub_face_id # id+1
        print("\n [INFO] Initializing face capture. Look the camera and wait ...")

        # Initialize individual sampling face count
        count = 0
        while(True):
            ret, img = cam.read()
            #img = cv2.flip(img, -1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1
                # Save the captured image into the datasets folder
                cv2.imwrite("faseDataSet/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imshow('image', img)
            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break
            elif count >= 30: # Take 30 face sample and stop video
                 break
        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()
        #### end: Collect data from new user with opencv and Create a new model!
        
        return redirect(url_for('home'))
    
@app.route('/remove', methods=['GET', 'POST'])
def Remove():
    if request.method == 'GET':
        #Informatin data from infor.txt
        f1 = open('/home/pi/fdCam/userInformation/infor.txt', 'r')
        inforArray = [] #user inform array
        while True:
            line = f1.readline()
            if not line: break
            inforArray.append(line)
        f1.close()
        print(inforArray)
        
        #who is Owner?
        f2 = open('/home/pi/fdCam/owner/owner.txt', 'r')
        # if file is null return '' 
        # if file  is not null reutnr <owner>\n'
        owner = f2.readline()
        f2.close()
        print(owner)
        return render_template('remove.html', inform = inforArray, ownerId = owner)
        
    elif request.method == 'POST':
        userId = request.form['id'] # (remove) id entered by user
        # write 
        f1 = open('/home/pi/fdCam/userInformation/infor.txt', 'r')
        informations = f1.readlines()
        print(informations)
        newInformations = []
        count = 1
        exitFlag = 1
        for i in informations:
            if userId != "" and count != int(userId) and len(informations) >= int(userId) and int(userId) > 0 :
                information = i.split()
                newInformations.append(information)
                exitFlag = -1
            elif int(userId) == count:
                exitFlag = -1
            count +=1
            
        print('hello')
        print(exitFlag)
        if exitFlag == 1:
            return redirect(url_for('home')) # It's case of no users
        
        else:
            print(newInformations) # this variable is new users for the old users
            count2 = 0
            for i in newInformations: #The process of matching the user's id from 1 to 1
                newInformations[count2] = str(count2 + 1) + " " + newInformations[count2][1]+"\n"
                count2 +=1
            print(newInformations)
            f1.close()
            
            f2 = open('/home/pi/fdCam/userInformation/infor.txt', 'w')
            for i in newInformations:
                f2.write(i) # Update user file information
            f2.close()
            
            #user face dataset remove!!
            for i in range(1, 31):
                os.remove('/home/pi/fdCam/faseDataSet/User.{0}.{1}.jpg'.format(userId, i))
            
            #All file name upadate
            for i in range(int(userId) + 1, len(newInformations) + 2):
                for j in range(1, 31):
                    os.rename('/home/pi/fdCam/faseDataSet/User.{0}.{1}.jpg'.format(i, j),'/home/pi/fdCam/faseDataSet/User.{0}.{1}.jpg'.format(i-1, j))
            
            return redirect(url_for('home'))
            
@app.route('/face_recognition')
def Face_Recognition():    
    os.system("python 02_face_training.py")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0

    # names related to ids: example ==> loze: id=1,  etc
    # add to array of user name 
    names = ['None']
    f1 = open('/home/pi/fdCam/userInformation/infor.txt', 'r')
    inforArray = [] #user inform array
    ownerID = 0
    while True:
        line = f1.readline()
        if not line: break
        inforArray.append(line)
    f1.close()
    print(inforArray)
    
    for i in inforArray:
        names.append(i.split()[1])
    print(names)
    f1.close()
    
    f2 = open('/home/pi/fdCam/owner/owner.txt', 'r')
    ownerID = f2.read(1) # not owner-> '\n'
    if ownerID == '\n':
        ownerID = -1
    else:
        ownerID = int(ownerID)
    print(ownerID)
    f2.close()
    
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    recog_flags = -1
    while True:
        ret, img =cam.read()
        img = cv2.flip(img, 1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )

        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            # Check if confidence is less them 100 ==> "0" is perfect match
            
            
            if (confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                if(names.index(id) == ownerID):
                    print('You  owner: ' + id)
                    GPIO.output(2,True)   # Blue LED ON
                    GPIO.output(17,False) # yellow off
                    GPIO.output(7,False)  # red off
                else:
                    print('Not Owner!!!')
                    GPIO.output(2,False)   # Blue LED off
                    GPIO.output(17,True) # yellow ON
                    GPIO.output(7,False)  # red off
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
                print('who are you?')
                GPIO.output(2,False)   # Blue LED off
                GPIO.output(17,False)  # yellow off
                GPIO.output(7,True)    # red ON
            
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    
    GPIO.output(2,False)   
    GPIO.output(17,False)
    GPIO.output(7,False)  
    return redirect(url_for('home'))

@app.route('/gohome', methods=['GET', 'POST'])
def Gohome():
    if request.method == 'POST':
        return redirect(url_for('home'))
        
if __name__ == '__main__':
    app.run()


    
