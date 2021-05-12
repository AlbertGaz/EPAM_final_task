"""ML MODEL IMPORT."""
import os
import pickle

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
MODEL_EN_DIR = os.path.join(DIR_PATH, "model_cardiffnlp_en.bin")
MODEL_RU_DIR = os.path.join(DIR_PATH, "model_blanchefort_ru.bin")

EN = "en"
RU = "ru"

MODELS = {}

with open(MODEL_EN_DIR, "rb") as f_in:
    MODELS[EN] = pickle.load(f_in)

with open(MODEL_RU_DIR, "rb") as f_in:
    MODELS[RU] = pickle.load(f_in)
