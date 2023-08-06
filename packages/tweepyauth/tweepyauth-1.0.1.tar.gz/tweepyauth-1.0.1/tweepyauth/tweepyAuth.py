import tweepy
import webbrowser
import os


def auto_authenticate():
	if os.path.isfile('twitter_keys.txt'):
		print('loading twitter_keys.txt')
		with open('twitter_keys.txt','r') as f:
			keys = list(f.read().split(','))	
			auth = tweepy.OAuthHandler(keys[0],keys[1])
	else:
		print('consumer_keys.txt doesnt exist')
		keys = [input('consumer API key:'),input('consumer API secret key:')]
		try:
			auth = tweepy.OAuthHandler(keys[0],keys[1])
		except BaseException as e:
			print('keys invalid:',e)
		try:
			with open('twitter_keys.txt','w') as f:
				f.write(','.join(keys))
		except BaseException as e:
			print('error writing twitter_keys.txt:',e)
			os.remove('twitter_keys.txt')
		return None

	if os.path.isfile('twitter_tokens.txt'):
		print('loading twitter_tokens.txt')
		try:
			with open('twitter_tokens.txt','r') as f:
				tokens = list(f.read().split(','))
				auth.set_access_token(tokens[0], tokens[1])
				print('all done')
				return tweepy.API(auth)
		except BaseException as e:
			print('tweepyauth error:',e)
			return None
	else:
		print('twitter_tokens.txt doesnt exist, registering now')
		auth = authenticate(keys[0],keys[1]) 
		return verify(auth)


def authenticate(consumer_token,consumer_secret):
	auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
	try:
		redirect_url = auth.get_authorization_url()
		print(redirect_url)
		try:
			webbrowser.open(redirect_url,new=0)
		except:
			pass
		print('opening broswer window, please log in')
		return auth
	except tweepy.TweepError:
		print('Error! Failed to authorize.')

def verify(auth,verifier=None):
	if verifier == None:
		verifier = input('Verifier:')
	try:
		access_tokens = auth.get_access_token(verifier)
		token_key = access_tokens[0]
		token_secret = access_tokens[1]
		auth.set_access_token(token_key, token_secret)
		with open('twitter_tokens.txt','w') as f:
			f.write(f'{token_key},{token_secret}')
	except tweepy.TweepError:
		print('Error! Failed to get access token.')
		return None
	api = tweepy.API(auth)
	return api

if __name__ == '__main__':
	api = auto_authenticate()
	print(api.home_timeline()[0])