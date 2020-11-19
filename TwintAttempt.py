import sys, os, datetime

import twint
import time
import traceback
#from .token import token
c = twint.Config()
#twint.token.Token(c).refresh()
c.Limit = 1
c.Username = "JordanSimkovic"
c.Pandas = True
#print(datetime.date.today() - datetime.timedelta(days  = 2))
c.Since = str(datetime.date.today() - datetime.timedelta(days  = 2))
c.Hide_output = True
#twint.token = token.Token(config)
#twint.token.refresh()

twint.run.Search(c)

Tweets_df1 = twint.storage.panda.Tweets_df

print(Tweets_df1.keys())


#print(Tweets_df1["created_at"])
#print(type(Tweets_df1["created_at"][0]))
print(Tweets_df1["date"][0])
print(type(Tweets_df1["date"][0]))

#dt_object = datetime.datetime.fromtimestamp(Tweets_df1["created_at"][0])
#print(dt_object)


now = datetime.datetime.now()

print("now =", now)
format = "%Y-%m-%d %H:%M:%S"
# dd/mm/YY H:M:S
dt_string = now.strftime(format)
print("date and time =", dt_string)
#format = "%Y-%m-%d %H:%M:%S"
print((datetime.datetime.strptime(Tweets_df1["date"][0], format) - datetime.datetime.strptime(dt_string, format)).total_seconds())


print(set(Tweets_df1["created_at"]))

newwest_tweet_time = Tweets_df1["created_at"][0]

def streamer(Tweets_df):

    global newwest_tweet_time

    while(True):
        #twint.token = token.Token(config)
        #twint.token.refresh()
        twint.token.Token(c).refresh()

        twint.run.Search(c)

        Tweets_df_temp = twint.storage.panda.Tweets_df

        text_df_temp = set(Tweets_df_temp["tweet"])
        text_df = set(Tweets_df["tweet"])

        diff = text_df_temp - text_df

        if not diff == set():
            Tweets_df = Tweets_df_temp

            print("There are " + str(len(diff)) + " new tweets")

            i = 0
            for new_tweet in diff:
                i += 1
                print("New tweet number: " + str(i))
                print(new_tweet)
                picture_bool = not not Tweets_df["photos"][i]
                video_bool = bool(Tweets_df["video"][i])
                pod_bool = any("apple.co" in url for url in Tweets_df["urls"][i])

                if picture_bool == video_bool and not pod_bool and ((Tweets_df["created_at"][list(Tweets_df["tweet"]).index(new_tweet)] - newwest_tweet_time) > 0):
                    print("This would be posted to Reddit")
                    newwest_tweet_time = Tweets_df["created_at"][list(Tweets_df["tweet"]).index(new_tweet)]
                else:
                    print("This would not be posted to Reddit")
        else:
            print("No new tweets. Sleeping for 60 seconds")
            time.sleep(5)
            continue

        #dict_Tweets_df = dict(Tweets_df)


while(True):
    try:
        twint.run.Search(c)

        Tweets_df1 = twint.storage.panda.Tweets_df

        streamer(Tweets_df1)
    except:
        traceback.print_exc()
        time.sleep(60*5)
