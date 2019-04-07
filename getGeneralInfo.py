# coding=utf-8
'''This file provides apis for getting the information of user'''

from zhihu_oauth import GetDataErrorException
from zhihu_oauth.zhcls.generator import ActivityGenerator
from zhihu_oauth.zhcls.activity import ActType
from zhihu_oauth.helpers import *
import time


def get_normal_para(people):
    name = people.name
    follower_count = people.follower_count
    following_count = people.following_count
    thanked_count = people.thanked_count
    voteup_count = people.voteup_count
    article_count = people.article_count
    answer_count = people.answer_count
    gender = people.gender #0 for female, 1 for male, -1 for none

    return name,follower_count,following_count,thanked_count,voteup_count,article_count,answer_count


def get_flexible_para(people):

    educations = people.educations
    education = ''
    isCuhkszMember = False

    judge = ['������Ĵ�ѧ(����)','������Ĵ�ѧ����','CUHK(SZ)','CUHKSZ','������Ĵ�ѧ�����ڣ�']

    if educations:
        for experience in educations:
            if 'school' in experience:
                education += experience.school.name + ' '
            if 'major' in experience:
                education += experience.major.name + ';'

    employments = people.employments
    employment = ''
    if employments:
        for experience in employments:
            if 'company' in experience:
                employment += experience.company.name + ' '
            if 'job' in experience:
                employment += experience.job.name + ';'

    business = ''
    if people.business:
        business = people.business.name


    location = ''
    if people.locations:
        for place in people.locations:
            location += place.name + ';'

    badge = ''
    if people.badge:
        if people.badge.has_identity: badge += 'identified '
        if people.badge.is_best_answerer: badge += 'best answer '
        if people.badge.is_organization: badge += 'organization'

    #judge if the people belongs to cuhksz
    cuhksz_count = 0
    combination = education + employment + location
    for word in judge:
        if word in combination:
            isCuhkszMember = True
            cuhksz_count = 1
            print('find a CUHKSZ member')
            break

    return education, employment, business, location, badge, cuhksz_count


#only applied for Hong Kong students
def get_spec_info(people):

    #get following topics
    following_topics = []
    for topic in people.following_topics:
        following_topics.append(topic.name)

    #get following people
    following_people = []
    for ppl in people.followings:
        following_people.append(ppl.name)

    #get answers' detail
    ans = []
    for answer in people.answers:
        answ = {}
        answ['voteup_count'] = answer.voteup_count
        answ['question'] = answer.question.title
        answ['create_time'] = answer.created_time

        answ['topic'] = []
        for topic in answer.question.topics:
            answ['topic'].append(topic.name)

        ans.append(answ)

    #get questions' detail
    ques = []
    for question in people.questions:
        quest = {}
        quest['title'] = question.title
        quest['follower_count'] = question.follower_count
        
        quest['topic'] = []
        for topic in question.topics:
            quest['topic'].append(topic.name)

        ques.append(quest)

    activities = []
    # for act in people.activities.filter(ActType.VOTEUP_ANSWER):
    #     print(ts2str(act.created_time), act2str(act))

    for act in people.activities:
        activity = {}
        activity['time'] = act.created_time
        activity['type'] = act.type
        

        activities.append(activity)

    return following_topics, following_people, ans, ques, activities



    



 