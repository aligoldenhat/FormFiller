import urllib
import requests
from bs4 import BeautifulSoup
import datetime, calendar, os, calendar
from threading import Timer
import re
from time import sleep
import logging

Name = ''
Number = ''
ID = ''
PhoneNumber = ''
Vaccinate = ''

#update holiday every month
Holidays = [23, 2, 3]

#emruz chan shanbe asst
curr_date = datetime.datetime.today().weekday()
weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
Today = weekdays[curr_date]

#aya mishe emruz reseve kard
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

#aya google form answar accept mikne
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
            return '[!]'
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
                return '[!]'
            else:
                raise Exception
        except:
            #If both POST method and URL Recosntruction fails, it returns an error message
            return '[!] Attendance not sent !'

def Start():
    logging.basicConfig(filename=file,
                        format='%(asctime)s %(message)s',
                        filemode='a',
                        level=logging.INFO)
    logger = logging.getLogger()
    global total_time, wait_time, sleep_time

    wait_time = 5    #chan saniye ye bar refresh kne
    sleep_time = 70       #chan saniye sleep bere


    total_time = 0
    if HolidayCheck():
        if CheckDay():
            def DoAll():
                global total_time, wait_time, sleep_time
                if AvailabeForm():
                    sleep(sleep_time)
                    a = FormFiller(url, Name, Number, ID, PhoneNumber, Vaccinate)
                    print (a)
                    log = f"=={Today}==> ({total_time}/{wait_time}= {int(total_time/wait_time)} NA) --{sleep_time}S >> {a}"
                    logger.info(log)

                else:
                    print('form baz nashode')
                    total_time += wait_time

                    Timer(wait_time, DoAll).start()
            DoAll()
        else:
            print ('roz haye jome V 2shanbe hast')
            logger.info(f"=={Today}==> emruz {Today} hast")
    else:
        print('ruz tatil hast emruz')
        logger.info(f"=={Today}==> ruze tatil hast")


if __name__ == "__main__":
    file = r"test.log"
    url = 'https://docs.google.com/forms/d/e/1FAIpQLSe2woUfImI-hNjkKThUD14Z0O6fQwKvqanYDWLnIFgxzJM4og/viewform?usp=sf_link'
    Start()
else:
    file = r"/home/ubuntu/logff.log"
    url = 'https://docs.google.com/forms/d/e/1FAIpQLSfo73u2pHJFxJpV8Ow8_4y8VyPztHgikw3RJKmUgFmrZ3GqQQ/viewform'
