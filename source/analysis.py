# coding=utf-8
import pandas as pd
import numpy as np
import csv

answer_df = pd.read_csv('answer_nodup.csv')
question_df = pd.read_csv('question_nodup.csv')
follow_df = pd.read_csv('follow_nodup.csv')
activity_df = pd.read_csv('activity_nodup.csv')
data_df = pd.read_csv('data_nodup.csv')
hk_df = pd.read_csv('hk_student_info_nodup.csv')


'''get the count of elements through all rows of the series'''
def get_count(topic_series):
    topics = {}
    
    for row_topics in topic_series:
        try:
            row_topic_list = row_topics.split(',')
            for topic in row_topic_list:
                if topic in topics.keys():
                    topics[topic] += 1
                else: topics[topic] = 1
                    
        except Exception as e:
            pass
        
    return topics


# # General Info

que_topics = get_count(question_df.topic)
follow_topics = get_count(follow_df.following_topics)
follow_people = get_count(follow_df.following_people)


# # CUHKSZ Info

target = ['香港中文大学（深圳）','香港中文大学\(深圳\)','CUHKSZ','CUHK\(SZ\)','香港中文大学深圳']
cuhksz_df = hk_df.loc[hk_df['education'].str.contains('|'.join(target),case=False)]
cuhksz_df.to_csv('cuhksz_df.csv',encoding='utf-8')

cuhksz_name = cuhksz_df.name
cuhksz_ans_df = answer_df.loc[answer_df.name.isin(cuhksz_name)]
cuhksz_que_df = question_df.loc[question_df.name.isin(cuhksz_name)]
cuhksz_act_df = activity_df.loc[activity_df.name.isin(cuhksz_name)]
cuhksz_follow_df = follow_df.loc[follow_df.name.isin(cuhksz_name)]


cuhksz_follow_topics = get_count(cuhksz_follow_df.following_topics) 
cuhksz_follow_people = get_count(cuhksz_follow_df.following_people)


cuhksz_follow_df.to_csv('cuhksz_follow.csv',encoding='utf-8')
following = cuhksz_follow_df.loc[cuhksz_follow_df.name=='龙岗第一百里守约','following_people']


# # CUHK Info


cuhk_df = hk_df.loc[(hk_df['education'].str.contains('|'.join(target))==False) 
                                                    & (hk_df['education'].str.contains('香港中文大学|CUHK',case=False))]

cuhk_df.to_csv('cuhk_df.csv',encoding='utf-8')


cuhk_name = cuhk_df.name
cuhk_ans_df = answer_df.loc[answer_df.name.isin(cuhk_name)]
cuhk_que_df = question_df.loc[question_df.name.isin(cuhk_name)]
cuhk_act_df = activity_df.loc[activity_df.name.isin(cuhk_name)]
cuhk_follow_df = follow_df.loc[follow_df.name.isin(cuhk_name)]
cuhk_follow_topics = get_count(cuhk_follow_df.following_topics) 
cuhk_follow_people = get_count(cuhk_follow_df.following_people)


# # City U Info

target = ['香港城市大学','CityU']
cityu_df = hk_df.loc[hk_df['education'].str.contains('|'.join(target),case=False)]


cityu_name = cityu_df.name
cityu_ans_df = answer_df.loc[answer_df.name.isin(cityu_name)]
cityu_que_df = question_df.loc[question_df.name.isin(cityu_name)]
cityu_act_df = activity_df.loc[activity_df.name.isin(cityu_name)]
cityu_follow_df = follow_df.loc[follow_df.name.isin(cityu_name)]
cityu_follow_topics = get_count(cityu_follow_df.following_topics) 
cityu_follow_people = get_count(cityu_follow_df.following_people)


# # HKU Info

target = ['香港大学','HKU']
hku_df = hk_df.loc[(hk_df['education'].str.contains('|'.join(target),case=False)) 
                   & (hk_df['education'].str.contains('HKUST', case=False)== False)]

hku_name = hku_df.name
hku_ans_df = answer_df.loc[answer_df.name.isin(hku_name)]
hku_que_df = question_df.loc[question_df.name.isin(hku_name)]
hku_act_df = activity_df.loc[activity_df.name.isin(hku_name)]
hku_follow_df = follow_df.loc[follow_df.name.isin(hku_name)]
hku_follow_topics = get_count(hku_follow_df.following_topics) 
hku_follow_people = get_count(hku_follow_df.following_people)


# # HKUST Info

target = ['香港科技大学','HKUST']
hkust_df = hk_df.loc[hk_df['education'].str.contains('|'.join(target),case=False)]

hkust_name = hkust_df.name
hkust_ans_df = answer_df.loc[answer_df.name.isin(hkust_name)]
hkust_que_df = question_df.loc[question_df.name.isin(hkust_name)]
hkust_act_df = activity_df.loc[activity_df.name.isin(hkust_name)]
hkust_follow_df = follow_df.loc[follow_df.name.isin(hkust_name)]
hkust_follow_topics = get_count(hkust_follow_df.following_topics) 
hkust_follow_people = get_count(hkust_follow_df.following_people)


# # HKBU Info

target = ['香港浸会大学','HKBU']
hkbu_df = hk_df.loc[hk_df['education'].str.contains('|'.join(target),case=False)]


hkbu_name = hkbu_df.name
hkbu_ans_df = answer_df.loc[answer_df.name.isin(hkbu_name)]
hkbu_que_df = question_df.loc[question_df.name.isin(hkbu_name)]
hkbu_act_df = activity_df.loc[activity_df.name.isin(hkbu_name)]
hkbu_follow_df = follow_df.loc[follow_df.name.isin(hkbu_name)]
hkbu_follow_topics = get_count(hkbu_follow_df.following_topics) 
hkbu_follow_people = get_count(hkbu_follow_df.following_people)


# # PolyU

target = ['香港理工大学','polyu']
polyu_df = hk_df.loc[hk_df['education'].str.contains('|'.join(target),case=False)]


# In[19]:


polyu_name = polyu_df.name
polyu_ans_df = answer_df.loc[answer_df.name.isin(polyu_name)]
polyu_que_df = question_df.loc[question_df.name.isin(polyu_name)]
polyu_act_df = activity_df.loc[activity_df.name.isin(polyu_name)]
polyu_follow_df = follow_df.loc[follow_df.name.isin(polyu_name)]
polyu_follow_topics = get_count(polyu_follow_df.following_topics) 
polyu_follow_people = get_count(polyu_follow_df.following_people)


# # Topic Analysis
for k in sorted(polyu_follow_topics,key=polyu_follow_topics.__getitem__,reverse=True):
    print(k,polyu_follow_topics[k])


# # Activity Analysis
cuhksz_act_df['time'] = pd.to_datetime(cuhksz_act_df['time'],unit='s',dayfirst=True)


'''plot a diagram showing the actions through last three years with given act_df'''
def plot_action(act_df,school_name):
    
    act_df['time'] = pd.to_datetime(act_df['time'],unit='s',dayfirst=True)
    
    target_df = act_df.set_index('time')['2018-01-02':'2018-12-31']
    target_df['time_bin'] = pd.cut(target_df.index,12,precision=0)
    action_count = target_df.groupby('time_bin').count()['name']

    target_df2 = act_df.set_index('time')['2019':]
    target_df2['time_bin'] = pd.cut(target_df2.index,4,precision=0)
    action_count2 = target_df2.groupby('time_bin').count()['name']

    target_df3 = act_df.set_index('time')['2017-01-02':'2017-12-31']
    target_df3['time_bin'] = pd.cut(target_df3.index,12,precision=0)
    action_count3 = target_df3.groupby('time_bin').count()['name']

    target_df4 = act_df.set_index('time')['2016-01-02':'2016-12-31']
    target_df4['time_bin'] = pd.cut(target_df4.index,12,precision=0)
    action_count4 = target_df4.groupby('time_bin').count()['name']
    
    
    plt.figure(1,figsize=(15,10))

    l1, = plt.plot(np.arange(len(action_count)),action_count)
    x_ticks = [str(i.left)[5:7] for i in action_count.index]
    plt.xticks(np.arange(len(action_count))[::1],x_ticks[::1])

    l2, = plt.plot(np.arange(len(action_count2)),action_count2)
    x_ticks2 = [str(i.left)[5:7] for i in action_count2.index]

    l3, = plt.plot(np.arange(len(action_count3)),action_count3)
    x_ticks3 = [str(i.left)[5:7] for i in action_count3.index]

    l4, = plt.plot(np.arange(len(action_count4)),action_count4)
    x_ticks4 = [str(i.left)[5:7] for i in action_count3.index]

    plt.title('actions of '+ school_name + ' students',fontsize=25,loc='center')
    plt.xlabel('month',fontsize=20)
    plt.ylabel('actions',fontsize=20)
    plt.legend([l4,l3,l1,l2],['2016','2017','2018','2019'],fontsize=20)
    plt.savefig(school_name+' action分析')
    
plot_action(cuhksz_act_df,'cuhksz')


#Analyze the most active users of last one month
target_df = cuhksz_act_df.set_index('time')['2019-3-20':]
target_df.groupby('name').count().sort_values(by='gender',ascending=False)


# # Analyze the actions of one day
def plot_oneday_action(df,school_name):
    target_df = df.copy()
    target_df['time'] = pd.to_datetime(df['time'],unit='s',dayfirst=True)
    target_df['hour'] = target_df.time.dt.hour
    target_df = target_df.groupby('hour').count()
    
    plt.figure(figsize=(15,10))
    plt.plot(target_df.index,target_df.name)
    x_ticks = [i for i in target_df.index]
    plt.xticks(np.arange(len(target_df))[::2],x_ticks[::2])
    plt.title('Actions of one day ({})'.format(school_name),fontsize=20)
    plt.ylabel('actions',fontsize=20)
    plt.xlabel('daytime',fontsize=20)
    plt.savefig(school_name+'oneday action')


plot_oneday_action(cuhksz_act_df,'cuhksz')

