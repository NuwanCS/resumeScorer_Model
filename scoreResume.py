from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class Scorer:

    def sent_similarity(self, text_1, text_2):
        model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')
        sentences = [''.join(text_1), ''.join(text_2)]
        sentence_embeddings = model.encode(sentences)
        similarity = cosine_similarity(sentence_embeddings[0].reshape(1, -1), sentence_embeddings[1].reshape(1, -1))[0][0]
        return round(similarity * 100, 2)

    # def __init__(self):
    #     self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    #     self.model = AutoModel.from_pretrained('bert-base-uncased')

    # def sent_similarity(self, text_1, text_2):
    #     encoded_input = self.tokenizer(text_1, text_2, padding=True, truncation=True, return_tensors='pt')
    #     with torch.no_grad():
    #         outputs = self.model(**encoded_input)
    #         embeddings = outputs[0][:, 0, :]
    #         print('-----------', embeddings)
    #         similarity = torch.cosine_similarity(embeddings[0], embeddings[1], dim=0)
    #     return round(similarity.item() * 100, 2)
        