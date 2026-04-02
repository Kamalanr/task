pending_reviews = {}

def store_review(user_id, msg, draft):
    pending_reviews[user_id] = {"msg": msg, "draft": draft}

def get_review(user_id):
    return pending_reviews.get(user_id)

def clear_review(user_id):
    if user_id in pending_reviews:
        del pending_reviews[user_id]