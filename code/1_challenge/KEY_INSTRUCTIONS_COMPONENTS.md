

Perfect! Here are **the instructions we used to guide the Contoso HR Agent** that was created in Challenge 1:

## Agent System Instructions 📋

```
You are an HR assistant. Always search the knowledge base for answers.
Cite your sources using [document#page] format.
If information isn't in documents, say "I don't know."
```

## Key Instruction Components:

1. **Role Definition**: "You are an HR assistant"
   - Sets the agent's persona and domain

2. **Retrieval Behavior**: "Always search the knowledge base for answers"
   - Forces RAG pattern (must use Azure AI Search tool)
   - Prevents hallucination by requiring document grounding

3. **Citation Format**: "Cite your sources using [document#page] format"
   - Ensures transparency and verifiability
   - Helps with groundedness evaluation

4. **Fallback Behavior**: "If information isn't in documents, say 'I don't know.'"
   - Prevents making up answers
   - Critical for trustworthy AI behavior

## These Instructions Were Designed To:
- ✅ Maximize **groundedness** (answers must come from docs)
- ✅ Ensure **relevance** (stay on HR topics)
- ✅ Enable **citation validation** (sources are traceable)
- ✅ Prevent **hallucination** (explicit refusal when unsure)

This aligns with the **Responsible AI principles** from Challenge 1, focusing on reliability, transparency, and safety!