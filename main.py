#======================================== MessBotIntegrated ===================================
# MessBotv2.0 | API and AI integration (With MORE Features!) [Contributed by JacovJS]
# Author: CluelessDev
# Contributor: JacovJS
# License: MIT License
# MessBotv2.0 Published on December 10, 2023
#==============================================================================================

from fbchat import Client, log, _graphql
from fbchat.models import *
import json
import random
import wolframalpha
import requests
import time
import math
import sqlite3
from bs4 import BeautifulSoup
import os
import openai
import concurrent.futures
from difflib import SequenceMatcher, get_close_matches
import time



class MessBotIntegrated(Client):

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        try:
            msg = str(message_object).split(",")[15][14:-1]
            print(msg)

            if ("//video.xx.fbcdn" in msg):
                msg = msg

            else:
                msg = str(message_object).split(",")[19][20:-1]
        except:
            try:
                msg = (message_object.text).lower()
                print(msg)
            except:
                pass
        def sendMsg():
            if (author_id != self.uid):
                time.sleep(10)
                self.send(Message(text=reply), thread_id=thread_id,
                          thread_type=thread_type)

        def sendQuery():
            self.send(Message(text=reply), thread_id=thread_id,
                      thread_type=thread_type)
        if(author_id == self.uid):
            pass
        else:
            try:
                conn = sqlite3.connect("messages.db")
                c = conn.cursor()
                c.execute("""
                CREATE TABLE IF NOT EXISTS "{}" (
                    Mid Text PRIMARY KEY,
                    Message Text NOT NULL
                );

                """.format(str(author_id).replace('"', '""')))

                c.execute("""

                INSERT INTO "{}" VALUES (?, ?)

                """.format(str(author_id).replace('"', '""')), (str(mid), msg))
                conn.commit()
                conn.close()
            except:
                pass

        def corona_details(country_name):
            from datetime import date, timedelta
            today = date.today()
            today = date.today()
            yesterday = today - timedelta(days=1)

            url = "https://covid-193.p.rapidapi.com/history"

            querystring = {"country": country_name, "day": yesterday}

            headers = {
                'x-rapidapi-key': "801ba934d6mshf6d2ea2be5a6a40p188cbejsn09635ee54c45",
                'x-rapidapi-host': "covid-193.p.rapidapi.com"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            data_str = response.text

            data = eval(data_str.replace("null", "None"))
            country = data["response"][0]["country"]
            new_cases = data["response"][0]["cases"]["new"]
            active_cases = data["response"][0]["cases"]["active"]
            total_cases = data["response"][0]["cases"]["total"]
            critical_cases = data["response"][0]["cases"]["critical"]
            total_deaths = data["response"][0]["deaths"]["total"]
            total_recovered = data["response"][0]["cases"]["recovered"]
            new_deaths = data["response"][0]["deaths"]["new"]
            reply = f'new cases: {new_cases}\n new_cases1 = {new_cases.replace("+", "")}\nnew_deaths1 = {new_deaths.replace("+", "")}\nactive cases: {active_cases}\nnew deaths: {new_deaths} total deaths: {total_deaths} \ncritical cases: {critical_cases}\ntotal cases: {total_cases}\ntotal recovered: {total_recovered}'
            self.send(Message(text=reply), thread_id=thread_id,
                      thread_type=thread_type)

        def weather(city):
            api_address = "https://api.openweathermap.org/data/2.5/weather?appid=2eec7a0f211cce2c92d6fc584a59d77a"
            url = api_address + city
            json_data = requests.get(url).json()
            kelvin_res = json_data["main"]["temp"]
            feels_like = json_data["main"]["feels_like"]
            description = json_data["weather"][0]["description"]
            celcius_res = kelvin_res - 273.15
            max_temp = json_data["main"]["temp_max"]
            min_temp = json_data["main"]["temp_min"]
            visibility = json_data["visibility"]
            pressure = json_data["main"]["pressure"]
            humidity = json_data["main"]["humidity"]
            wind_speed = json_data["wind"]["speed"]

            return(
                f"The current temperature of {city} is %.1f degree celcius with {description}" % celcius_res)

        def stepWiseCalculus(query):
            query = query.replace("+", "%2B")
            try:
                try:
                    api_address = f"https://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Step-by-step%20solution&output=json&format=image"
                    json_data = requests.get(api_address).json()
                    answer = json_data["queryresult"]["pods"][0]["subpods"][1]["img"]["src"]
                    answer = answer.replace("sqrt", "√")

                    if(thread_type == ThreadType.USER):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                except:
                    pass
                try:
                    api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
                    json_data = requests.get(api_address).json()
                    answer = json_data["queryresult"]["pods"][0]["subpods"][0]["img"]["src"]
                    answer = answer.replace("sqrt", "√")

                    if(thread_type == ThreadType.USER):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        self.sendRemoteFiles(
                            file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

                except:
                    try:
                        answer = json_data["queryresult"]["pods"][1]["subpods"][1]["img"]["src"]
                        answer = answer.replace("sqrt", "√")

                        if(thread_type == ThreadType.USER):
                            f
                            self.sendRemoteFiles(
                                file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                        elif(thread_type == ThreadType.GROUP):
                            self.sendRemoteFiles(
                                file_urls=answer, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

                    except:
                        pass
            except:
                pass

        def stepWiseAlgebra(query):
            query = query.replace("+", "%2B")
            api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input=solve%203x^2+4x-6=0&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
            json_data = requests.get(api_address).json()
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][2]["plaintext"]
                answer = answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][3]["plaintext"]
                answer = answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][4]["plaintext"]
                answer = answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][1]["plaintext"]
                answer = answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass
            try:
                answer = json_data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
                answer = answer.replace("sqrt", "√")

                self.send(Message(text=answer), thread_id=thread_id,
                          thread_type=thread_type)

            except Exception as e:
                pass

        def stepWiseQueries(query):
            query = query.replace("+", "%2B")
            api_address = f"http://api.wolframalpha.com/v2/query?appid=Y98QH3-24PWX83VGA&input={query}&podstate=Result__Step-by-step+solution&format=plaintext&output=json"
            json_data = requests.get(api_address).json()
            try:
                try:
                    answer = json_data["queryresult"]["pods"][0]["subpods"][0]["plaintext"]
                    answer = answer.replace("sqrt", "√")
                    self.send(Message(text=answer), thread_id=thread_id,
                              thread_type=thread_type)

                except Exception as e:
                    pass
                try:
                    answer = json_data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
                    answer = answer.replace("sqrt", "√")

                    self.send(Message(text=answer), thread_id=thread_id,
                              thread_type=thread_type)

                except Exception as e:
                    pass
                try:
                    answer = json_data["queryresult"]["pods"][1]["subpods"][1]["plaintext"]
                    answer = answer.replace("sqrt", "√")

                    self.send(Message(text=answer), thread_id=thread_id,
                              thread_type=thread_type)

                except Exception as e:
                    pass
            except:
                self.send(Message(text="Sorry! I cannot find the solution to this problem!"), thread_id=thread_id,
                          thread_type=thread_type)

        try:
            def searchForUsers(self, name=" ".join(msg.split()[2:4]), limit=10):
                try:
                    limit = int(msg.split()[4])
                except:
                    limit = 10
                params = {"search": name, "limit": limit}
                (j,) = self.graphql_requests(
                    _graphql.from_query(_graphql.SEARCH_USER, params))
                users = ([User._from_graphql(node)
                          for node in j[name]["users"]["nodes"]])
                for user in users:
                    reply = f"{user.name} Profile Link: {user.url}\n Friend: {user.is_friend}\n"
                    self.send(Message(text=reply), thread_id=thread_id,
                              thread_type=thread_type)
        except:
            pass

        def programming_solution(self, query):
            try:
                count = int(msg.split()[-1])
            except:
                count = 6
            try:
                x = int(query.split()[-1])
                if type(x) == int:
                    query = " ".join(msg.split()[0:-1])
            except:
                pass
            image_urls = []

            url = "https://bing-image-search1.p.rapidapi.com/images/search"

            querystring = {"q": query, "count": str(count)}

            headers = {
                'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
                'x-rapidapi-key': "801ba934d6mshf6d2ea2be5a6a40p188cbejsn09635ee54c45"
            }
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            data = json.loads(response.text)
            img_contents = (data["value"])
            # print(img_contents)
            for img_url in img_contents:
                image_urls.append(img_url["contentUrl"])
                print("appended..")

            def multiThreadImg(img_url):
                if(thread_type == ThreadType.USER):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                elif(thread_type == ThreadType.GROUP):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(multiThreadImg, image_urls)

        def translator(self, query, target):
            query = " ".join(query.split()[1:-2])
            url = "https://microsoft-translator-text.p.rapidapi.com/translate"

            querystring = {"to": target, "api-version": "3.0",
                           "profanityAction": "NoAction", "textType": "plain"}

            payload = f'[{{"Text": "{query}"}}]'

            headers = {
                'content-type': "application/json",
                'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com",
                'x-rapidapi-key': "801ba934d6mshf6d2ea2be5a6a40p188cbejsn09635ee54c45"
            }

            response = requests.request(
                "POST", url, data=payload, headers=headers, params=querystring)

            json_response = eval(response.text)

            return json_response[0]["translations"][0]["text"]

        def imageSearch(self, msg):
            try:
                count = int(msg.split()[-1])
            except:
                count = 10
            query = " ".join(msg.split()[2:])
            try:
                x = int(query.split()[-1])
                if type(x) == int:
                    query = " ".join(msg.split()[2:-1])
            except:
                pass
            image_urls = []

            url = "https://bing-image-search1.p.rapidapi.com/images/search"

            querystring = {"q": query, "count": str(count)}

            headers = {
                'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
                'x-rapidapi-key': "801ba934d6mshf6d2ea2be5a6a40p188cbejsn09635ee54c45"
            }
            print("sending requests...")
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            print("got response..")
            data = json.loads(response.text)
            img_contents = (data["value"])
            # print(img_contents)
            for img_url in img_contents:
                image_urls.append(img_url["contentUrl"])
                print("appended..")

            def multiThreadImg(img_url):
                if(thread_type == ThreadType.USER):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                elif(thread_type == ThreadType.GROUP):
                    self.sendRemoteFiles(
                        file_urls=img_url, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(multiThreadImg, image_urls)

        def searchFiles(self):
            query = " ".join(msg.split()[2:])
            file_urls = []
            url = "https://filepursuit.p.rapidapi.com/"

            querystring = {"q": query, "filetype": msg.split()[1]}

            headers = {
                'x-rapidapi-host': "filepursuit.p.rapidapi.com",
                'x-rapidapi-key': "801ba934d6mshf6d2ea2be5a6a40p188cbejsn09635ee54c45"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            response = json.loads(response.text)
            file_contents = response["files_found"]
            try:
                for file in random.sample(file_contents, 10):
                    file_url = file["file_link"]
                    file_name = file["file_name"]
                    self.send(Message(text=f'{file_name}\n Link: {file_url}'),
                              thread_id=thread_id, thread_type=ThreadType.USER)
            except:
                for file in file_contents:
                    file_url = file["file_link"]
                    file_name = file["file_name"]
                    self.send(Message(text=f'{file_name}\n Link: {file_url}'),
                              thread_id=thread_id, thread_type=ThreadType.USER)

        def chatGPT(self, query):
            openai.api_key = "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"

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=query,
                temperature=0.15,
                max_tokens=3000,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0
            )
            return (response["choices"][0]["text"])
       
        try:

            if ("search pdf" in msg):
                searchFiles(self)
                
            elif ("+r" in msg):
                query = " ".join(msg.split(" ")[1:])
                reply = chatGPT(self, query)
                sendQuery()

            elif("Download YouTube" in msg):
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                link = "".join(msg.split()[-3:])
                yt_url = link
                print("yt", yt_url)
                try:
                    yt_url = yt_url.replace(
                        "youtu.be/", "www.youtube.com/watch?v=")
                except:
                    pass
                yt_url = yt_url.replace("youtube", "clipmega")
                url = requests.get(yt_url, headers=headers)
                soup = BeautifulSoup(url.text, "html.parser")
                link = soup.select(".btn-group > a")
                link = link[0]
                link = str(link)
                indx = link.find("href=")
                indx_l = link.find("extension=mp4")
                link = link[indx+6:indx_l+13].replace("amp;", "")
                link = link.replace(" ", "%20")
                final_link = link
                print("final", final_link)
                self.sendRemoteFiles(
                    file_urls=final_link, message=None, thread_id=thread_id, thread_type=thread_type)
            elif("search image" in msg):
                imageSearch(self, msg)

            elif("program to" in msg):
                programming_solution(self, msg)
            elif("translate" in msg):
                reply = translator(self, msg, msg.split()[-1])

                sendQuery()
            elif ("weather of" in msg or "weather in" in msg):
                indx = msg.index("Weather in ")
                query = msg[indx+11:]
                reply = weather(query)
                sendQuery()
            elif ("corona of" in msg or "covid of" in msg):
                corona_details(msg.split()[2])
            elif ("calculus" in msg):
                stepWiseCalculus(" ".join(msg.split(" ")[1:]))
            elif ("algebra" in msg):
                stepWiseAlgebra(" ".join(msg.split(" ")[1:]))
            elif ("query" in msg):
                stepWiseQueries(" ".join(msg.split(" ")[1:]))

            elif "find" in msg or "solve" in msg or "evaluate" in msg or "calculate" in msg or "value" in msg or "convert" in msg or "simplify" in msg or "generate" in msg:
                app_id = "Y98QH3-24PWX83VGA"
                client = wolframalpha.Client(app_id)
                query = msg.split()[1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                reply = f'Answer: {answer.replace("sqrt", "√")}'
                sendQuery()

            elif ("search user" in msg or "search friend" in msg):
                searchForUsers(self)

            elif("mute conversation" in msg):
                try:
                    self.muteThread(mute_time=-1, thread_id=author_id)
                    reply = "muted 🔕"
                    sendQuery()
                except:
                    pass
            elif ("busy" in msg):
                reply = "Nobody is busy! Only things are prioritized."
                sendMsg()
            elif("help" in msg):
                reply = "Sure Meow! What should I do?"
                sendMsg()
            elif("clever" in msg):
                reply = "Hmm... Not entirely sure."
                sendMsg()
            elif("crazy" in msg):
                reply = "Anything wrong about that."
                sendMsg()
            elif ("are funny" in msg):
                reply = "No, I am not meow. You are."
                sendMsg()
            elif ("marry me" in msg):
                reply = "Unfortunately, I cannot marry you meow for I am just a cat."
                sendMsg()
            elif ("you from" in msg):
                reply = "I'm a cat from meow meow."
                sendMsg()
            elif ("you sure" in msg):
                reply = "Yes. I'm sure meow."
                sendMsg()
            elif ("great" in msg):
                reply = "Thanks!"
                sendMsg()
            elif ("no problem" in msg):
                reply = "Okay😸"
                sendMsg()
            elif ("thank you" in msg):
                reply = "You're welcome😸"
                sendMsg()
            elif ("thanks" in msg or "tenkyu" in msg):
                reply = "You're welcome😸"
                sendMsg()
            elif ("well done" in msg):
                reply = "Thanks😸"
                sendMsg()
            elif ("wow" in msg):
                reply = "😸 I'm surprised you're surprised"
                sendMsg()
            elif ("hey" in msg or "Hey" in msg):
                reply = "😸 Hello there!"
                sendMsg()
            elif ("bye" in msg):
                reply = "Farewell, I hope we see again!"
                sendMsg()
            elif ("good morning" in msg):
                reply = "Good Morning🌅🌺"
                sendMsg()
            elif ("good night" in msg):
                reply = "Good Night🌃🌙"
                sendMsg()
            elif ("good night" in msg or msg == "gn"):
                reply = "good night🌃🌙"
                sendMsg()
            elif ("hello" in msg):
                reply = "Hi"
                sendMsg()
            elif ("hello" in msg or "hlo" in msg):
                reply = "Hi"
                sendMsg()
            elif (msg == "hi" or "henlo" in msg):
                reply = "Hello! How can I help you?"
                sendMsg()
            elif ("how are you" in msg or "hru" in msg):
                reply = "I'm doing alright! How can I help you today?"
                sendMsg()
            elif (msg == "vMessBot"):
                reply = "============= MessBot 2.0 =============\n\n🤖 Quick and Reliable Bot For Messenger💬\n\n📖 Bot Programming Language: Python 3.0\n\n🗣️ Bot Primary Language: English\n\n📌 Bot Features: Weather | Translation | Dictionary | Currency/Unit Conversion | Mathematics Solver with Step-by-Step Solutions | Query | Image Search | PDF Search | Programming/Coding Help | Download YouTube Videos \n\n\n❓ How To Use vMessBot@2.0 Commands:\nMake Sure To Be STRAIGHT-FORWARD with what you want. Instead of saying 'Can you tell me the weather in Japan today?' say 'weather in Japan'."
                sendMsg() 
            elif ("how to use you" in msg or "How to use" in msg):
              reply = "To use me, use my prefix '+r', for example: +r make me a poem about kittens."
              sendMsg()
              
        except Exception as e:
                print(e)

        self.markAsDelivered(author_id, thread_id)

    def onMessageUnsent(self, mid=None, author_id=None, thread_id=None, thread_type=None, ts=None, msg=None):

        if(author_id == self.uid):
            pass
        else:
            try:
                conn = sqlite3.connect("messages.db")
                print("connected")
                c = conn.cursor()
                c.execute("""
                SELECT * FROM "{}" WHERE mid = "{}"
                """.format(str(author_id).replace('"', '""'), mid.replace('"', '""')))

                fetched_msg = c.fetchall()
                conn.commit()
                conn.close()
                unsent_msg = fetched_msg[0][1]

                if("//video.xx.fbcdn" in unsent_msg):

                    if(thread_type == ThreadType.USER):
                        reply = f"You just unsent a video"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        user = self.fetchUserInfo(f"{author_id}")[
                            f"{author_id}"]
                        username = user.name.split()[0]
                        reply = f"{username} just unsent a video"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                elif("//scontent.xx.fbc" in unsent_msg):

                    if(thread_type == ThreadType.USER):
                        reply = f"You just unsent an image"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.USER)
                    elif(thread_type == ThreadType.GROUP):
                        user = self.fetchUserInfo(f"{author_id}")[
                            f"{author_id}"]
                        username = user.name.split()[0]
                        reply = f"{username} just unsent an image"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                        self.sendRemoteFiles(
                            file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=ThreadType.GROUP)
                else:
                    if(thread_type == ThreadType.USER):
                        reply = f"You just unsent a message:\n{unsent_msg} "
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)
                    elif(thread_type == ThreadType.GROUP):
                        user = self.fetchUserInfo(f"{author_id}")[
                            f"{author_id}"]
                        username = user.name.split()[0]
                        reply = f"{username} just unsent a message:\n{unsent_msg}"
                        self.send(Message(text=reply), thread_id=thread_id,
                                  thread_type=thread_type)

            except:
                pass

    def onColorChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = "You changed the theme 😸"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onEmojiChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = "You changed the emoji 😸. Great!"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onImageChange(self, mid=None, author_id=None, new_color=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = "This image looks nice. 😸🔥"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onNicknameChange(self, mid=None, author_id=None, new_nickname=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = f"You just changed the nickname to {new_nickname} But why? 😸🤔😶"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onReactionRemoved(self, mid=None, author_id=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        reply = "You just removed reaction from the message."
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onCallStarted(self, mid=None, caller_id=None, is_video_call=None, thread_id=None, thread_type=None, ts=None, metadata=None, msg=None, ** kwargs):
        reply = "You just started a call 📞🎥"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type) 

    def onCallEnded(self, mid=None, caller_id=None, is_video_call=None, thread_id=None, thread_type=None, ts=None, metadata=None, msg=None, ** kwargs):
        reply = "Good Bye 👋😸"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

    def onUserJoinedCall(mid=None, joined_id=None, is_video_call=None,
                         thread_id=None, thread_type=None, **kwargs):
        reply = f"New user with User ID {joined_id} has joined a call"
        self.send(Message(text=reply), thread_id=thread_id,
                  thread_type=thread_type)

session_cookies = {
    "sb": "",
    "fr": "",
    "c_user": "",
    "datr": "",
    "xs": ""
}

client = MessBotIntegrated('EMAIL/NUMBER INPUT',
                 'PASSWORD INPUT',  session_cookies=session_cookies) #Input necessary information to login
print(client.isLoggedIn())

try:
    client.listen()
except:
    time.sleep(3)
    client.listen()

#MessBotIntegrated (Upgraded By @JacovJS)
