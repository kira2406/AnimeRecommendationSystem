from utils.helpers import *
from config.paths_config import *
from pipeline.prediction_pipeline import *

# print(find_similar_users(int(11880),USER_WEIGHTS_PATH,USER2USER_ENCODED,USER2USER_DECODED))
# print(find_similar_animes('Fairy Tail',ANIME_WEIGHTS_PATH,ANIME2ANIME_ENCODED,ANIME2ANIME_DECODED, DF))

# user_pref = get_user_preferences(11880, RATING_DF, DF)
# print(user_pref)
print(hybrid_recommendation(11880))