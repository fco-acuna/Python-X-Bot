from twitter_bot_class import TwitterBot
from apis import get_random_dog_image, get_motivational_quote

if __name__ == "__main__":
    try:
        quote = get_motivational_quote()
        image_url = get_random_dog_image()

        bot = TwitterBot("pacs47154@gmail.com", "Strange97*")
        bot.login()
        bot.post_tweets(quote, image_url=image_url)
        bot.logout()
    except Exception as e:
        print("Error general:", e)
        try:
            bot.logout()
        except:
            pass
