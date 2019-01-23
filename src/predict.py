from flair.models import TextClassifier
from flair.data import Sentence

classifier = TextClassifier.load_from_file("model/best-model.pt")
sentence = Sentence("Hi. Yes mum, I will...")
classifier.predict(sentence)
print(sentence.labels)
