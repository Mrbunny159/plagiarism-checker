import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def handler(request):
    try:
        body = json.loads(request.body)

        intro = clean_text(body.get("introduction", ""))
        review = clean_text(body.get("literature", ""))

        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([intro, review])

        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        similarity_percent = round(similarity * 100, 2)
        originality = round(100 - similarity_percent, 2)

        status = "PASS" if originality >= 90 else "FAIL"

        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({
                "similarity": similarity_percent,
                "originality": originality,
                "status": status
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({ "error": str(e) })
        }
