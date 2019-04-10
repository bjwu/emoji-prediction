from emoji.unicode_codes import UNICODE_EMOJI

class Auth(object):
        APP_KEY = 'WQirN5HNTPmwaJPiZz17pOV24'
        APP_SECRET = 'ww0xl00RVgTJRRA8iDdwGDABgZR4PTKR2F8f6w3cpfxwkoLGc6'
        OAUTH_TOKEN = '785311601377341440-MBgqSU0hBwFmPy5EBZHjw4ctsq5duuN'
        OAUTH_TOKEN_SECRET = 'G2n7AfHlZoMw8x6XYktos4679e1kOHkLsPbXw4v8VM7Mq'

# max is 400
raw_emojis = '🤓🤗🙄😊😃😏😍😘😚😳😌😆😁😉😜😝😀😙😛😴😟😦😧😮😬😕😯😑😒😅😓😥😩😔😞😖😨😰😣😢🤣😭😂😲😱😫😠😡😤😪😋😷😎😵😐😶😇🤔🤐🙄👽💤💩😈👿👺🙋🤦‍🎅😺😸😻😽😼🙀😿😹😾👅👀👍👎👌👊✊👋✋👇👈👉🙌🙏👆👏🤘🖕💪👻🍀🐾🌚🌝🌞🔥💥✨💧💊💔💞💕💝💘🚾🙈🙉🙊🐶💦⭐'

def is_valid(e):
    try:
        UNICODE_EMOJI[e]
        return e
    except KeyError:
        pass

LANGUAGE = 'en'
# filter out emojis not in our library
EMOJIS = list(filter(None, [is_valid(e) for e in raw_emojis]))
print(EMOJIS)
DOWNLOADED_TWEETS_PATH = 'emoji_twitter_data.txt'
