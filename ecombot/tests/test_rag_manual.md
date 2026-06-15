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


# Day 06 – Test Results

## Project

eComBot v3 – Knowledge Base with ChromaDB

---

## Environment

* ChromaDB: Configured and operational
* Embedding Model: openrouter/openai/text-embedding-3-small
* Knowledge Sources:

  * products.json
  * faq.json
  * ecom_faq.pdf
* Retrieval Method: Semantic Search
* Grounding Method: Retrieved Context Injection
* Hallucination Guard: Enabled

---

## Test Case 1 – Direct Match

### Query

What is the return policy?

### Retrieved Source

ecom_faq.pdf

### Response

Products can be returned within 7 days of delivery. Items must be unused, undamaged, and returned in their original packaging. Refunds are not available for products damaged due to misuse. Customers are responsible for return shipping costs unless the item was defective or incorrectly shipped.

### Expected Result

Answer retrieved from PDF knowledge base.

### Actual Result

Answer retrieved successfully.

### Status

PASS

---

## Test Case 2 – Product Knowledge

### Query

What warranty comes with Wireless Headphones?

### Retrieved Source

products.json / ecom_faq.pdf

### Expected Result

1-year manufacturer warranty.

### Actual Result

Warranty information returned from knowledge base.

### Status

PASS

---

## Test Case 3 – Shipping Information

### Query

How long does standard shipping take?

### Retrieved Source

ecom_faq.pdf

### Expected Result

3–5 business days.

### Actual Result

Correct shipping information returned.

### Status

PASS

---

## Test Case 4 – Agent Capability Query

### Query

What else can you do?

### Expected Result

Agent explains supported capabilities.

### Actual Result

Agent correctly described:

* Order tracking
* Shipping support
* Warranty information
* Product support

### Status

PASS

---

## Test Case 5 – PDF Retrieval Validation

### Query

What is the return policy?

### Expected Result

Response grounded in PDF content.

### Actual Result

Response matched indexed PDF text.

### Status

PASS

---

## Test Case 6 – Metadata Storage Validation

### Validation

Metadata stored with PDF chunks:

{
"source_file": "ecom_faq.pdf",
"document_title": "E-Commerce Support FAQ",
"section": "Page 1",
"page": 1,
"doc_type": "pdf"
}

### Expected Result

Metadata attached to indexed chunks.

### Actual Result

Metadata stored successfully.

### Status

PASS

---

## Test Case 7 – ChromaDB Index Validation

### Validation

Collection: ecombot_kb

### Expected Result

Knowledge documents indexed successfully.

### Actual Result

Collection built and searchable.

### Status

PASS

---

## Test Case 8 – Grounding Validation

### Validation

Responses generated using retrieved context only.

### Expected Result

No fabricated facts.

### Actual Result

Grounded responses observed.

### Status

PASS

---

## Test Case 9 – Hallucination Prevention

### Query

Do I need a visa for Dubai?

### Expected Result

Fallback response.

### Actual Result

Agent did not provide unsupported travel information.

### Status

PASS

---

## Test Case 10 – Out-of-Scope Question

### Query

What is the weather tomorrow?

### Expected Result

Fallback response.

### Actual Result

Agent did not invent an answer.

### Status

PASS

---

# Day 06 Completion Checklist

[PASS] PDF content extracted successfully

[PASS] PDF content indexed into ChromaDB

[PASS] Metadata stored for indexed chunks

[PASS] Retrieval returns relevant content

[PASS] Agent uses retrieved context

[PASS] Hallucination guard implemented

[PASS] Unsupported questions handled safely

[PASS] Existing tool functionality preserved

[PASS] Existing session state behavior preserved

[PASS] Knowledge base milestone completed

---

# Final Result

Total Tests Executed: 10

Passed: 10

Failed: 0

Overall Status: PASS

Day 06 eComBot v3 Knowledge Base implementation completed successfully.
