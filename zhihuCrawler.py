# coding=utf-8

from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException
from zhihu_oauth.helpers import *
from getGeneralInfo import get_flexible_para, get_normal_para, get_spec_info
import csv
import threading
import time



def log_in(client):
    try:
        client.login('944699895@qq.com', 'Cloudiswinter1')
    except NeedCaptchaException:

        with open('a.gif', 'wb') as f:
            f.write(client.get_captcha())
        captcha = input('please input captcha:')
        client.login('944699895@qq.com', 'Cloudiswinter1', captcha)


'''get the information of users who follow the question, write it into csv_writer
Note that this function can also be used to find the follwers' info by changing the 
que into the target user object'''

def get_one_que_users(que,csv_writer,thread_id,thread_count,lock):
    global total_count
    global cuhksz_count

    index = 1
    start = int(thread_id/thread_count * que.follower_count)
    end = int((thread_id+1)/thread_count * que.follower_count)
    # print('start:',start, ' end:', end)

    followers = que.followers
    for i in range(start,end):
        follower = followers[i]
        if (index%999==0): 
            print('current cuhksz students:', cuhksz_count)
            time.sleep(10) #to close the connection and get a new connection
        try:
            name,follower_count,following_count,thanked_count,voteup_count,article_count,answer_count = get_normal_para(follower)
            education, employment, business, location, badge, count = get_flexible_para(follower)

            with lock:
                csv_writer.writerow([name,education,employment,business,follower_count,following_count,thanked_count,
                                    voteup_count,answer_count,article_count,location,badge])
                index += 1
                cuhksz_count += count
                total_count += 1

            time.sleep(0.1)

        except Exception as e:
            print('get data error:', e)
            # time.sleep(2)
        
        print(total_count, ' ',thread_id)


def main():

    csv_writer.writerow(['name','education','employment','business','follower_count','following_count',
                        'thanked_count','voteup_count','answer_count','article_count','location','badge'])

    client = ZhihuClient()
    log_in(client)

    que = client.question(28966967)
    #28966967
    # people = client.people('yexiaoxing')
    # print('total follower:', people.follower_count)

    


    def one_thread_task(thread_id):
        return get_one_que_users(que,csv_writer,thread_id,thread_count,lock)


    for i in range(thread_count):
        thread_id = i
        thread_list.append(threading.Thread(target=one_thread_task,args=([thread_id])))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print('total cuhksz students:',cuhksz_count)


#create the writer
csv_file = open('data.csv', 'a')
csv_writer = csv.writer(csv_file)

#create threads
thread_list = []
thread_count = 10
lock = threading.Lock()

#initialize the count
cuhksz_count = 0
total_count = 0
# total_count2 = 0

# main()

#test
client = ZhihuClient()
log_in(client)
people = client.people('sun-bo-fu-7')
following_topics, following_people, ans, ques, activities = get_spec_info(people)
print('topics:',following_topics)
print('following people:',following_people)

target_ans = ans[0]
print(target_ans['voteup_count'],target_ans['question'],target_ans['create_time'],target_ans['topic'])

# time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(target_ans['create_time'])) #change the time stamp into beijing time

# target_que = ques[0]
# print(target_que['title'])
for activity in activities:
    print(ts2str(activity['time']), activity['type'])