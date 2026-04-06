# Dictionary to temporarily store pending reviews
# Key = user_id, Value = message + AI draft
pending_reviews = {}


# Store user message and AI draft
def store_review(user_id, msg, draft):
    
    # Save data in dictionary using user_id as key
    pending_reviews[user_id] = {
        "msg": msg,       # Original user message
        "draft": draft    # AI generated response
    }


# Retrieve stored review data
def get_review(user_id):
    
    # .get() avoids error if key doesn't exist
    return pending_reviews.get(user_id)


# Clear stored review after approve/reject
def clear_review(user_id):
    
    # Check if user exists in dictionary
    if user_id in pending_reviews:
        
        # Delete the entry
        del pending_reviews[user_id]