def generate_clarification(reason):
    return {
        "status": "clarification_required",
        "message": "More information is needed",
        "details": reason
    }
