# coding=utf-8

from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException
from zhihu_oauth.helpers import *
from getGeneralInfo import *
import csv
import threading
import time
import pandas as pd
from IPython.display import Image

import matplotlib.pyplot as plt
import requests
import numpy as np


def log_in(client):
    try:
        client.login('account', 'psw')
    except NeedCaptchaException:
        with open('a.gif', 'wb') as f:
            f.write(client.get_captcha())


'''
get the information of users who follow the question, write it into csv_writer
Note that this function can also be used to find the follwers' info by changing the 
que into the target user object
'''
def get_one_que_users(que,csv_writer,thread_id,thread_count,lock):
    global total_count
    global hk_student_list

    index = 1
    start = int(thread_id/thread_count * que.follower_count)
    end = int((thread_id+1)/thread_count * que.follower_count)

    followers = que.followers
    for i in range(start,end):
        follower = followers[i]
        
        try:
            name,follower_count,following_count,\
            thanked_count,voteup_count,article_count,answer_count = get_normal_para(follower)
            
            education, employment, business, location, badge, count = get_flexible_para(follower)

            with lock:
                csv_writer.writerow([name,education,employment,business,follower_count,following_count,thanked_count,
                                    voteup_count,answer_count,article_count,location,badge])
                index += 1
                total_count += 1

                #append to the list if it's HK student
                if count == 1: 
                    hk_student_list.append(follower)
                    hk_student_name.append(follower.name)

        except Exception as e:
            print('get data error:', e)
        
        print(total_count, ' ',thread_id)


'''get the follower of next target of hk_student_list'''
def get_followers(thread_id):
    global hk_student_list
    global index
    global maxnum
    
    while index < len(hk_student_list) and len(hk_student_list) < maxnum:

        target = hk_student_list[index]
        print(index)
        
        for people in target.followings:
            try:
                name,follower_count,following_count,\
                thanked_count,voteup_count,article_count,answer_count = get_normal_para(people)
                
                education, employment, business, location, badge, count = get_flexible_para(people)
                with lock2:
                    csv_writer.writerow([name,education,employment,business,follower_count,following_count,thanked_count,
                                        voteup_count,answer_count,article_count,location,badge])
                
                if (count == 1) & (people.name not in hk_student_name):
                    hk_student_list.append(people)  
                    hk_student_name.append(people.name)

            except Exception as e:
                print(e)
        index += 1
        np.save('index.npy',np.array(index))



def one_thread_task(thread_id):
    return get_one_que_users(que,csv_writer,thread_id,thread_count,lock)

def get_spec():
    global hk_student_list
    global index2
    
    while index2 < len(hk_student_list) - 1:
    
        target = hk_student_list[index2]
        print(index2)

        try:
            following_topics, following_people, ans, ques, activities, gender = get_spec_info(target)
            
            index2 += 1
            name = target.name

            follow_writer.writerow([name, gender,','.join(following_topics), ','.join(following_people)])
            for question in ques:
                que_writer.writerow([name,question['title'],','.join(question['topic']),question['follower_count']])
                
            for answer in ans:
                answer_writer.writerow([name,answer['question'],answer['create_time'],answer['voteup_count'],','.join(answer['topic'])])
                
            for activity in activities:
                activity_writer.writerow([name,gender,activity['time'],activity['type']])

        except Exception as e:
            print(e)
            time.sleep(10)



def get_data(client):

    csv_writer.writerow(['name','education','employment','business','follower_count','following_count',
                        'thanked_count','voteup_count','answer_count','article_count','location','badge'])


    question_id = 31729762 #start question
    que = client.question(question_id)
    
    #to get the information of one question user
    for i in range(thread_count):
        thread_id = i
        thread_list.append(threading.Thread(target=one_thread_task,args=([thread_id])))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()
    
    #expand the hk_student_list by the following chain
    while index < len(hk_student_list) and len(hk_student_list) < maxnum:
        new_thread_list = []
        for i in range(thread_count2):
            thread_id = i
            new_thread_list.append(threading.Thread(target=get_followers,args=([thread_id])))

        for thread in new_thread_list:
            thread.start()

        for thread in new_thread_list:
            thread.join()


def write_hk_student_info():

    csv_file = open('hk_student_info.csv', 'a')
    csv_writer2 = csv.writer(csv_file)

    csv_writer2.writerow(['name','education','employment','business','follower_count','following_count',
                            'thanked_count','voteup_count','answer_count','article_count','location','badge'])

    for people in hk_student_list:
        try:
            name,follower_count,following_count,\
            thanked_count,voteup_count,article_count,answer_count = get_normal_para(people)
            
            education, employment, business, location, badge, count = get_flexible_para(people)

            csv_writer2.writerow([name,education,employment,business,follower_count,following_count,thanked_count,
                                voteup_count,answer_count,article_count,location,badge])
        except Exception as e:
            print(e)

def write_modules():

    que_writer.writerow(['name','title','topic','follower_count'])
    activity_writer.writerow(['name','gender','time','type'])
    answer_writer.writerow(['name','question','create_time','voteup_count','topic'])
    follow_writer.writerow(['name','gender','following_topics','following_people'])



    # In[64]:


    new_thread_list = []
    new_thread_count = 30

    for i in range(new_thread_count):
        thread_id = i
        new_thread_list.append(threading.Thread(target=get_spec))

    for thread in new_thread_list:
        thread.start()

    for thread in new_thread_list:
        thread.join()

def main():
    #login
    client = ZhihuClient()
    log_in(client)
    Image('./a.gif')
    captcha = input('please input captcha:')
    client.login('account', 'psw', captcha)

    get_data(client)
    write_hk_student_info()
    write_modules()


if __name__ == "__main__":
    #initialize writers
    question_file = open('question.csv', 'a')
    activity_file = open('activity.csv','a')
    answer_file = open('answer.csv','a')
    follow_file = open('follow.csv','a') #following topics and people
    csv_file = open('data.csv', 'a')
    csv_writer = csv.writer(csv_file)
    que_writer = csv.writer(question_file)
    activity_writer = csv.writer(activity_file)
    answer_writer = csv.writer(answer_file)
    follow_writer = csv.writer(follow_file)

    thread_list = [] #for getting one question users
    thread_count = 10
    lock = threading.Lock()

    thread_list2 = [] #for expanding the hk_student_list
    thread_count2 = 20
    lock2 = threading.Lock()

    total_count = 0 #initialize the count

    #initialize hk student list
    hk_student_list = []
    hk_student_name = [] #for the checking purpose
    maxnum = 10000 #specify the maximum number of hk_student_list

    index = 0
    index2 = 0

    main()