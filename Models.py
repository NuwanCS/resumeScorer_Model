from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification
from transformers import pipeline
from flair.data import Sentence
from flair.models import SequenceTagger
import pickle



class Models:

    def serializeIntoByteStream(self, obj, file_name):
        with open(f'{file_name}.pickle', 'wb') as f:
            pickle.dump(obj, f)

    def deserializeIntoDictionary(self, file_name):
        with open(f'{file_name}.pickle', 'rb') as f:
            return pickle.load(f)

    def load_trained_models(self, pickle=False):
        #NER (dates)
        tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
        model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/camembert-ner-with-dates")
        self.ner_dates = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

        #Zero Shot Classification
        # self.zero_shot_classifier = pipeline("zero-shot-classification", model='facebook/bart-large-mnli')
        self.zero_shot_classifier = pipeline("zero-shot-classification", model='valhalla/distilbart-mnli-12-6')

        # Ner
        tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
        model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
        self.ner = pipeline('ner', model=model, tokenizer=tokenizer, grouped_entities=True)

        # Pos Tagging
        self.tagger = SequenceTagger.load("flair/pos-english-fast")


        if pickle:
            self.pickle_models()
        
        return self.ner, self.ner_dates, self.zero_shot_classifier, self.tagger
    
    def pickle_models(self):
        self.serializeIntoByteStream(self.ner, "ner")
        self.serializeIntoByteStream(self.zero_shot_classifier, "zero_shot_classifier_6")
        self.serializeIntoByteStream(self.ner_dates, "ner_dates")
        self.serializeIntoByteStream(self.tagger, "pos_tagger_fast")


    def load_pickled_models(self):
        ner_dates = self.deserializeIntoDictionary('ner_dates')
        ner = self.deserializeIntoDictionary('ner')
        zero_shot_classifier = self.deserializeIntoDictionary('zero_shot_classifier_6')
        tagger = self.deserializeIntoDictionary("pos_tagger_fast")
        return ner_dates, ner, zero_shot_classifier, tagger
    
    def get_flair_sentence(self, sent):
        return Sentence(sent)