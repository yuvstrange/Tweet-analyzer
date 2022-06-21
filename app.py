
import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns



consumerKey = ''
consumerSecret = ''
accessToken = ''
accessTokenSecret = ''


authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret) 
   
authenticate.set_access_token(accessToken, accessTokenSecret) 
    

api = tweepy.API(authenticate, wait_on_rate_limit = True)


























def app():


	st.title("Tweet Analyzer")


	activities=["Tweet Analyzer","Generate Twitter Data"]

	choice = st.sidebar.selectbox("Select Your Activity",activities)

	

	if choice=="Tweet Analyzer":

		st.subheader("Analyze the tweets of your favourite Personalities")

		st.subheader("This tool performs the following tasks :")

		st.write("1. Fetches the 5 most recent tweets from the given twitter handle")
		st.write("2. Generates a Word Cloud")
		st.write("3. Performs Sentiment Analysis and displays it in the form of a Bar Graph")


		


		raw_text = st.text_area("Enter the exact twitter handle of the Personality (without @)")



		st.markdown("Do checkout another tool on the sidebar")

		Analyzer_choice = st.selectbox("Select the Activities",  ["Show Recent Tweets","Generate WordCloud" ,"Visualize the Sentiment Analysis"])


		if st.button("Analyze"):

			
			if Analyzer_choice == "Show Recent Tweets":

				st.success("Fetching last 5 Tweets")

				
				def Show_Recent_Tweets(raw_text):

				
					posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")

					
					def get_tweets():

						l=[]
						i=1
						for tweet in posts[:5]:
							l.append(tweet.full_text)
							i= i+1
						return l

					recent_tweets=get_tweets()		
					return recent_tweets

				recent_tweets= Show_Recent_Tweets(raw_text)

				st.write(recent_tweets)



			elif Analyzer_choice=="Generate WordCloud":

				st.success("Generating Word Cloud")

				def gen_wordcloud():

					posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")


					df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
				
					allWords = ' '.join([twts for twts in df['Tweets']])
					wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
					plt.imshow(wordCloud, interpolation="bilinear")
					plt.axis('off')
					plt.savefig('WC.jpg')
					img= Image.open("WC.jpg") 
					return img

				img=gen_wordcloud()

				st.image(img)



			else:



				
				def Plot_Analysis():

					st.success("Generating Visualisation for Sentiment Analysis")

					


					posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")

					df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])


					
					
					def cleanTxt(text):
					 text = re.sub('@[A-Za-z0–9]+', '', text) 
					 text = re.sub('#', '', text) 
					 text = re.sub('RT[\s]+', '', text) 
					 text = re.sub('https?:\/\/\S+', '', text) 
					 
					 return text


					df['Tweets'] = df['Tweets'].apply(cleanTxt)


					def getSubjectivity(text):
					   return TextBlob(text).sentiment.subjectivity

					
					def getPolarity(text):
					   return  TextBlob(text).sentiment.polarity


					
					df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
					df['Polarity'] = df['Tweets'].apply(getPolarity)


					def getAnalysis(score):
					  if score < 0:
					    return 'Negative'
					  elif score == 0:
					    return 'Neutral'
					  else:
					    return 'Positive'
					    
					df['Analysis'] = df['Polarity'].apply(getAnalysis)


					return df



				df= Plot_Analysis()



				st.write(sns.countplot(x=df["Analysis"],data=df))


				st.pyplot(use_container_width=True)

				

	

	else:

		st.subheader("This tool fetches the last 100 tweets from the twitter handle & performs the following tasks")

		st.write("1. Converts it into a DataFrame")
		st.write("2. Cleans the text")
		st.write("3. Analyzes Subjectivity of tweets ")
		st.write("4. Analyzes Polarity of tweets ")
		st.write("5. Analyzes Sentiment of tweets")






		user_name = st.text_area("*Enter the exact twitter handle of the Personality (without @)*")

		st.markdown(" Do checkout another tool on the sidebar")

		def get_data(user_name):

			posts = api.user_timeline(screen_name=user_name, count = 100, lang ="en", tweet_mode="extended")

			df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

			def cleanTxt(text):
				text = re.sub('@[A-Za-z0–9]+', '', text) 
				text = re.sub('#', '', text) 
				text = re.sub('RT[\s]+', '', text)
				text = re.sub('https?:\/\/\S+', '', text) 
				return text

			# Clean the tweets
			df['Tweets'] = df['Tweets'].apply(cleanTxt)


			def getSubjectivity(text):
				return TextBlob(text).sentiment.subjectivity

						
			def getPolarity(text):
				return  TextBlob(text).sentiment.polarity


						
			df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
			df['Polarity'] = df['Tweets'].apply(getPolarity)

			def getAnalysis(score):
				if score < 0:
					return 'Negative'

				elif score == 0:
					return 'Neutral'


				else:
					return 'Positive'

		
						    
			df['Sentiment'] = df['Polarity'].apply(getAnalysis)
			return df

		if st.button("Show Data"):

			st.success("Fetching Last 100 Tweets")

			df=get_data(user_name)

			st.write(df)







			

				


























if __name__ == "__main__":
	app()
