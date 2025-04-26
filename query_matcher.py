def match_goal_from_query(query_text):
    query_text = query_text.lower()

    if "hospital" in query_text or "হাসপাতাল" in query_text:
        return "hospital"
    elif "shelter" in query_text or "safety" in query_text:
        return "shelter"
    elif "medicine" in query_text or "drug" in query_text:
        return "resource_delivery"
    elif "water" in query_text or "পানি" in query_text:
        return "resource_delivery"
    elif "alternative" in query_text or "বিকল্প" in query_text or "block" in query_text or "পথ বন্ধ" in query_text:
        return "alt_path"
    else:
        return "unknown"