# GF_PY312_CLASS_Embed_Text_Model.py
# Create by GF 2025-03-21

import sentence_transformers

# ##################################################

class Embed_Text_Model():

    def __init__(self):

        self.SentenceTransformer = sentence_transformers.SentenceTransformer
        self.util                = sentence_transformers.util

        #self.Local_Model_Path = "./nomic-ai/nomic-embed-text-v1.5"
        self.Local_Model_Path = "./BAAI/bge-m3"

        # [nomic-embed-text-v1.5 Contains]
        #
        # nomic-ai/nomic-embed-text-v1.5
        # nomic-ai/nomic-bert-2048

        # Loading Embeding Model.
        self.Model = self.SentenceTransformer(
                        self.Local_Model_Path,
                        local_files_only=True,
                        trust_remote_code=True
                    )

    def Calsulate_2_Sentence_Cos_Similarity(self, Sentence_1, Sentence_2):

        # 计算 2 个句子的余弦 (Cos) 相似度
        # Calsulate 2 Sentence Cos Similarity
        #
        # Example:
        #
        # sentence_1 = "Bin Sari Specialized Technologies"
        # sentence_2 = "Bin Sari Specialized"
        # similarity = Calsulate_2_Sentence_Cos_Similarity(sentence_1, sentence_2)
        # >>> print(similarity)
        # tensor([[0.8936]])

        model = self.Model
        util  = self.util

        # ..........................................

        # Loading Embeding Model.
        # model = SentenceTransformer(
        #             "./nomic-ai/nomic-embed-text-v1.5",
        #             local_files_only=True,
        #             trust_remote_code=True
        #         )

        Embeding_1 = model.encode(Sentence_1)
        Embeding_2 = model.encode(Sentence_2)

        # Calsulate Similarity.
        Similarity = util.cos_sim(Embeding_1, Embeding_2)

        return Similarity

# ##################################################
# EOF Signed by GF.
