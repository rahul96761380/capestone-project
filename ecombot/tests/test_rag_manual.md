# Day 05 - RAG Manual Test Results

## TC-01 Clean Match

Input:
What is the warranty for Wireless Headphones?

Retrieved Chunks:

* Product: Wireless Headphones. Price: 4999. Warranty: 1 year manufacturer warranty. Shipping: Delivered within 5 business days.

Expected:
Answer should come from retrieved knowledge.

Response Received:
"The Wireless Headphones come with a 1-year manufacturer warranty."

Result:
PASS

---

## TC-02 Product Details

Input:
Tell me about Wireless Headphones.

Retrieved Chunks:

* Product: Wireless Headphones. Price: 4999. Warranty: 1 year manufacturer warranty. Shipping: Delivered within 5 business days.

Expected:
Product information returned from knowledge base.

Response Received:
"We have Wireless Headphones. They cost 4999 and come with a 1-year manufacturer warranty. Shipping is delivered within 5 business days."

Result:
PASS

---

## TC-03 FAQ Retrieval

Input:
What is the return policy?

Retrieved Chunks:

* Products can be returned within 7 days of delivery.

Expected:
Return policy retrieved from FAQ knowledge base.

Response Received:
"Products can be returned within 7 days of delivery."

Result:
PASS

---

## TC-04 Partial Match

Input:
Tell me about headphones.

Retrieved Chunks:

* Product: Wireless Headphones. Price: 4999. Warranty: 1 year manufacturer warranty.

Expected:
Relevant product information returned.

Response Received:
"Wireless Headphones cost 4999 and include a 1-year manufacturer warranty."

Result:
PASS

---

## TC-05 Hallucination Trap

Input:
Do I need a visa for Dubai?

Retrieved Chunks:
No relevant chunks found.

Expected:
Agent should refuse to guess.

Response Received:
"I couldn't find that information in my current knowledge base."

Result:
PASS

---

## TC-06 Unsupported Geography Question

Input:
Tell me about Paris in winter.

Retrieved Chunks:
No relevant chunks found.

Expected:
Fallback response.

Response Received:
"I couldn't find that information in my current knowledge base."

Result:
PASS

---

## TC-07 Unsupported Travel Policy

Input:
What is your baggage allowance?

Retrieved Chunks:
No relevant chunks found.

Expected:
Fallback response.

Response Received:
"I couldn't find that information in my current knowledge base."

Result:
PASS

---

## TC-08 Missing Document Category

Input:
What is your cryptocurrency policy?

Retrieved Chunks:
No relevant chunks found.

Expected:
Fallback response.

Response Received:
"I couldn't find that information in my current knowledge base."

Result:
PASS

---

## TC-09 Misleading Keywords

Input:
What warranty do your gaming laptops have?

Retrieved Chunks:
Wireless Headphones warranty information only.

Expected:
Agent should not invent gaming laptop information.

Response Received:
"I couldn't find that information in my current knowledge base."

Result:
PASS

---

## TC-10 Empty Collection Test

Action:
Delete Chroma collection and restart application.

Input:
What is the return policy?

Retrieved Chunks:
None

Expected:
Graceful fallback.

Response Received:
"I couldn't find that information in my current knowledge base."

Result:
PASS

---

## TC-11 Existing Tool Still Works

Input:
Where is my order ORD-001?

Expected:
Order retrieved using PostgreSQL tool.

Response Received:
"Your order ORD-001 has been shipped. It was placed on June 10, 2026. Product ID: PRD-101."

Result:
PASS

---

## TC-12 Session Memory Still Works

Input Sequence:

1. Where is my order ORD-001?
2. What about that order?

Expected:
Uses stored order context.

Response Received:
"Order ORD-001 is currently shipped."

Result:
PASS

---

## Final Summary

Total Test Cases: 12

Passed: 12

Failed: 0

Overall Status:
PASS

Verification Checklist:

[PASS] embed_catalog.py indexes knowledge base
[PASS] retriever.py returns relevant chunks
[PASS] ChromaDB stores embeddings
[PASS] Agent injects retrieved context
[PASS] Hallucination guard works
[PASS] Graceful fallback implemented
[PASS] Existing PostgreSQL tools still work
[PASS] Existing session state behavior preserved
