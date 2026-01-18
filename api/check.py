from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import json

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def handler(request):
    body = json.loads(request.body)

    intro = clean_text(body.get("introduction", ""))
    review = clean_text(body.get("literature", ""))

    documents = [intro, review]

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    similarity_percent = round(similarity * 100, 2)
    originality = round(100 - similarity_percent, 2)

    status = "PASS" if originality >= 90 else "FAIL"

    return {
        "statusCode": 200,
        "body": json.dumps({
            "similarity": similarity_percent,
            "originality": originality,
            "status": status
        })
    }
