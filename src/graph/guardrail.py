from groq import Groq

def verify_factual_grounding(context: str, proposed_answer: str, client: Groq) -> bool:
    """
    Two-Pass Verification: Asks the LLM to verify if its own answer is strictly 
    contained within the provided context. Returns True if safe, False if hallucinated.
    """
    # If the system already admitted it doesn't know, let it pass safely
    if "data not available" in proposed_answer.lower():
        return True

    verification_prompt = f"""
    Context provided:
    {context}
    
    Proposed Answer:
    {proposed_answer}
    
    Task: Carefully examine the context. Does the Proposed Answer state any specific names, projects, startups, or financial facts that are NOT explicitly supported by the context?
    Respond with exactly one word: "SAFE" if everything is in the context, or "HALLUCINATION" if it guessed or extrapolated.
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": verification_prompt}],
            temperature=0.0,
            max_tokens=5
        )
        status = response.choices[0].message.content.strip().upper()
        return "HALLUCINATION" not in status
    except Exception as e:
        # Fail safe: If verification fails, block the answer
        return False