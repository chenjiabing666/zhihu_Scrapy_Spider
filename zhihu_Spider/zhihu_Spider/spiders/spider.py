# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu_Spider.items import ZhihuSpiderItem

class SpiderSpider(scrapy.Spider):
    name = "spider"
    # allowed_domains = ["zhihu.com"]
    # start_urls = ['http://zhihu.com/']
    start_user = 'excited-vczh'
    user_url="https://www.zhihu.com/api/v4/members/{user}?include={include}"
    user_query='locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    follow_url='https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&amp;offset={offset}&amp;limit={limit}'
    follow_query='data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield scrapy.Request(self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        #yield scrapy.Request(self.follow_url.format(user=self.start_user,include=self.follow_query,limit=20,offset=0),callback=self.parse_follow_user)

    ##解析用戶的信息
    def parse_user(self,response):
        item=ZhihuSpiderItem()
        result=json.loads(response.text)
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

        yield scrapy.Request(self.follow_url.format(user=result.get('url_token'),include=self.follow_query,limit=20,offset=0),callback=self.parse_follow_user)

    def parse_follow_user(self,response):
        results=json.loads(response.text)

        if 'data' in results.keys():   # 繼續收集關注列表中的用戶信息
            for result in results.get('data'):
                yield scrapy.Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.parse_user)

        if 'paging' in results.get('paging') and results.get('paging').get('is_end')==False:
            for result in results.get('paging'):
                yield scrapy.Request(result.get('next'))   #繼續請求下一頁的用戶列表











