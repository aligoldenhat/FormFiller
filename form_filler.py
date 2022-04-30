import urllib
import requests
from bs4 import BeautifulSoup
import datetime, calendar, os
from threading import Timer
import re
from time import sleep

#url = 'https://docs.google.com/forms/yourform'
url = ''
Name = 'your name'
Number = ''
ID = ''
PhoneNumber = ''
Vaccinate = ''

#Update holiday every month
Holidays = [23, 2, 3]

#Do not book on some days
def CheckDay():
    curr_day = calendar.day_name[datetime.date.today().weekday()]
    reserve_day = ['Saturday', 'Sunday', 'Tuesday', 'Wednesday', 'Thursday']

    for check_day in reserve_day:
        if curr_day == check_day:
            return True
    
    return False

def HolidayCheck():
    for Holiday in Holidays:
        if datetime.date.today().day == Holiday:
            return False
    return True

#Is Google Form Open?
def AvailabeForm():
    try:
        res = urllib.request.urlopen(url)
        soup = BeautifulSoup(res.read(), 'html.parser')
        all_questions = soup.form.findChildren()
        return True
    except AttributeError:
        return False
    
def get_questions(url):
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    content = soup.body.find_all(text = re.compile('var FB'))
    
    match = re.findall('[,]["][\w\s]+["][,]', str(content))
    question_strings = [x.strip('"') for x in match]
    
    match_ids = re.findall('(?<=\[\[)(\d+)', str(content))
    question_ids = ['entry.' + x for x in match_ids[1:]]
    
    return question_ids

def FormFiller(url, Name, Number, ID, PhoneNumber, Vaccinate): #Change the parameters other than url as per your needs
    
    '''Sends the answers for a Google Form'''
    
    ids = get_questions(url)
    
    answers = [Name, Number, ID, PhoneNumber, Vaccinate]
    response = dict(zip(ids, answers))
    
    if 'viewform' in url:
        s = url.index('viewform') 
        response_url = url.replace(url[s::], 'formResponse?')
        
    try:
        #This tries to send the data (answers) using POST method.
        r = requests.post(response_url, response)
        if r.status_code == 200:
            return '[!] Attendence posted !'
        else:
            raise Exception

    except:
        try:
            #This tries to send the data (answers) using URL Reconstruction if the POST method fails.
            ans_list = [x + '=' + y for x, y in zip(ids, answers)]
            
            for i in range(0, len(ans_list)):
                response_url += ans_list[i]
                response_url += '&'
                
            response_url.strip("&")    
            r = requests.get(response_url)
            status = r.status_code
            
            if status == 200:
                return '[!] Attendance sent !'
            else:
                raise Exception
        except:
            #If both POST method and URL Recosntruction fails, it returns an error message
            return '[!] Attendance not sent !'


#file = os.path.join(os.path.dirname(__file__), './log.txt')
#Create a log.txt and ...
file = r'C:\Users\Digi Max\Desktop\log.txt'
log_txt = open(file, 'a')
log_txt.write('\n')
log_txt.write(str(datetime.datetime.now()))
log_txt.write(' =====> ')


if HolidayCheck():
    if CheckDay():
        def DoAll():
            if AvailabeForm():
                a = FormFiller(url, Name, Number, ID, PhoneNumber, Vaccinate)
                print (a)
                log_txt.write(a)
            else:
                print('form baz nashode')
                log_txt.write('NA  - ')
                Timer(5, DoAll).start() 
        DoAll()
    else:
        print ('roz haye jome V 2shanbe hast')
        log_txt.write('roz haye jome V 2shanbe hast')
else:
    print('ruz tatil hast emruz')
    log_txt.write('ruz tatil hast emruz')


