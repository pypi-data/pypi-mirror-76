import numpy as np
from gensim.models import Word2Vec
import warnings
import time
import jiagu
import joblib

warnings.filterwarnings("ignore")

W2V_MODEL_PATH = "data/word2vec_wx"
XG_MODEL_PATH = "2020_08_05_18_08_danmu_XG.model"


class XgWord2Vec(object):
    def __init__(self, xg_model_path, w2v_model_path):
        self.xg_model = joblib.load(open(xg_model_path, "rb"))
        self.w2v_model = Word2Vec.load(w2v_model_path)

    def predict(self, s):
        flag = self.xg_model.predict(np.array(self.compute_doc_vec_single(s, self.w2v_model)))[0]
        return flag

    @staticmethod
    def compute_doc_vec_single(article, w2v):
        vec = np.zeros((1, w2v.layer1_size))
        n = 0
        for word in jiagu.seg(article):
            if word in w2v:
                vec += w2v[word]
                n += 1
        return (vec / n).tolist()


if __name__ == '__main__':
    t = time.time()
    sg = XgWord2Vec("2020_08_05_18_08_danmu_XG.model")
    # joblib.dump(sg, "20200806_model.cls")
    # model = joblib.load("20200806_model.cls")
    # print(model.predict("你喜欢我吗"))
    print(sg.predict("喜欢吗"))
    print(f"花费时间:{time.time() - t}")
    # print(sg.w2v_model.wv.vocab)
