import tweepy
import yaml
import coronaStats as st

def load_config():
    with open("config.yaml", 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config

        except yaml.YAMLError as exc:
            print(exc)
            exit
            
def tweetStats(text, config, image = None):
    config = load_config()

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(config['TwitterAPI']['consumer']['key'], config['TwitterAPI']['consumer']['secret'])
    auth.set_access_token(config['TwitterAPI']['access']['token'], config['TwitterAPI']['access']['secret'])
    
    api = tweepy.API(auth)

    #Create a tweet
    if image:
        api.update_with_media(image, text)
    else:
        api.update_status(text)

config = load_config()
myfilename = 'compared_related'
stats = st.CoronaStats(config['csvUrl'])
myfile = stats.plot_diagram_related(myfilename)
infected = stats.get_actual_infected()
date = stats.get_latest_update_date()
growth_germany = stats.get_weekly_growth()

tweet_text = "Am " + date + " gab es " + str(infected['overall'][0]) + " (" + infected['overall'][1] +") erfasste Infektionen weltweit.\n"
tweet_text += "In Deutschland: " + str(infected['germany'][0]) + " (" + infected['germany'][1] +") Infektionen.\n\n"
tweet_text += "Wachstumsrate in Deutschland der letzten 7 Tage: " + "{0:.2f}".format(growth_germany) + "%\n\n"
tweet_text += "Dashboard: https://my-covid-dash.herokuapp.com/"
tweet_text += "\n\n#corona #mycoronastats #COVID19deutschland"

tweetStats(tweet_text, config, myfile)

exit