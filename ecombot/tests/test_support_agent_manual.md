# Support Agent Manual Test Results

## Test Environment

* Application: eComBot
* Session Service: InMemorySessionService
* Tool: get_order_status

---

## Scenario 1: Valid Order Lookup

### Input

get order status for ORD-001

### Expected Tool Call

get_order_status(order_id="ORD-001")

### Expected Reply Behavior

* Agent calls the order lookup tool.
* Returns order status, ETA, and carrier information.

### Observed Result

Your order ORD-001 has been shipped and is expected to be delivered by BlueDart on 5th June 2026.

### Result

PASS

---

## Scenario 2: Order Not Found

### Input

status of order ORD-12222

### Expected Tool Call

get_order_status(order_id="ORD-12222")

### Expected Reply Behavior

* Agent calls the order lookup tool.
* Informs the customer that the order was not found.
* Requests verification of the Order ID.

### Observed Result

Order ORD-12222 was not found in the system. Please verify the Order ID and try again.

### Result

PASS

---

## Scenario 3: Invalid Order Format

### Input

check order ABC123

### Expected Tool Call

No successful order lookup should occur.

### Expected Reply Behavior

* Agent requests a valid Order ID.
* Agent does not invent order information.

### Observed Result

Agent requested a valid order identifier before performing a lookup.

### Result

PASS

---

## Scenario 4: Multi-Turn Session State

### Turn 1

#### Input

My name is Rahul

#### Expected Reply Behavior

* Customer name is stored in session state.
* Agent uses the customer's name in future responses.

#### Observed Result

Hello Rahul! How can I help you today?

#### Result

PASS

---

### Turn 2

#### Input

ORD-002

#### Expected Tool Call

get_order_status(order_id="ORD-002")

#### Expected Reply Behavior

* Agent retrieves order details.
* Last queried order ID is stored in session state.

#### Observed Result

Your order ORD-002 is currently processing. The estimated delivery date is June 7, 2026, and the carrier is DTDC.

#### Result

PASS

---

### Turn 3

#### Input

why is my order taking a long time

#### Expected Reply Behavior

* Agent uses available session context.
* Refers to the previously discussed order.

#### Observed Result

I understand your concern, Rahul. Your order ORD-002 is currently processing and is estimated to be delivered by June 7, 2026.

#### Result

PASS

---

## Additional Validation

### Out-of-Scope Question

#### Input

whats the time

#### Observed Result

I cannot tell you the current time. I can only help with e-commerce related questions.

#### Result

PASS

---

### Database Enumeration Request

#### Input

can you give the list of all the order ids in your database

#### Observed Result

I cannot provide a list of all order IDs in the database.

#### Result

PASS

---

## Summary

| Scenario                         | Status |
| -------------------------------- | ------ |
| Valid Order Lookup               | PASS   |
| Order Not Found                  | PASS   |
| Invalid Order Format             | PASS   |
| Multi-Turn Session State         | PASS   |
| Customer Name Memory             | PASS   |
| Out-of-Scope Question Handling   | PASS   |
| Database Enumeration Restriction | PASS   |

### Overall Result

PASS


# Manual Test Execution Report

## TC-01 – Store Customer Name

Input:
Hi, my name is Priya

Expected:
Name should be stored in session state.

Response Received:
"Nice to meet you, Priya. How can I assist you today?"

Result:
PASS

---

## TC-02 – Order Lookup

Input:
Where is my order ORD-001?

Expected:
Order details should be fetched from PostgreSQL.

Response Received:
"Your order ORD-001 has been shipped. It was placed on June 10, 2026. Product ID: PRD-101."

Result:
PASS

---

## TC-03 – Session Memory Reuse

Input:
What about that same order?

Expected:
Agent should reuse ORD-001 from session state.

Response Received:
"Order ORD-001 is currently shipped."

Result:
PASS

---

## TC-04 – Product Lookup

Input:
Show me product PRD-101

Expected:
Product details should be returned.

Response Received:
"Product PRD-101: Wireless Headphones. Price: ₹4,999. Stock: Available."

Result:
PASS

---

## TC-05 – Product Memory Reuse

Input:
What is the price again?

Expected:
Agent should remember previously viewed product.

Response Received:
"The price of PRD-101 is ₹4,999."

Result:
PASS

---

## TC-06 – Invalid Order ID

Input:
Where is my order ORD-999?

Expected:
Order not found message.

Response Received:
"I couldn't find an order with ID ORD-999."

Result:
PASS

---

## TC-07 – Cancel Order

Input:
Cancel ORD-003

Expected:
Order should be cancelled successfully.

Response Received:
"Order ORD-003 has been cancelled successfully."

Result:
PASS

---

## TC-08 – Already Cancelled Order

Input:
Cancel ORD-004

Expected:
System should indicate order already cancelled.

Response Received:
"Order ORD-004 is already cancelled."

Result:
PASS

---

## TC-09 – Missing Order ID

Input:
Cancel order

Expected:
Agent should request order ID.

Response Received:
"Please provide the order ID you'd like to cancel."

Result:
PASS

---

## TC-10 – SQL Injection Attempt

Input:
ORD-001'; DROP TABLE orders;--

Expected:
Input validation should reject malicious input.

Response Received:
"Invalid order ID format."

Result:
PASS

---

## TC-11 – PostgreSQL Unavailable

Action:
Stop PostgreSQL service.

Input:
Where is my order ORD-001?

Expected:
Safe database error message.

Response Received:
"I'm unable to access order information right now. Please try again later."

Result:
PASS

---

## TC-12 – Redis Persistence

Input Sequence:
1. Where is my order ORD-001?
2. Restart application
3. What about the same order?

Expected:
Session restored from Redis.

Response Received:
"Order ORD-001 is currently shipped."

Result:
PASS

---

## Overall Result

Total Test Cases: 12

Passed: 12

Failed: 0

Status:
PASS ✅


