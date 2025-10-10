## **API Overview:**

`Create Account POST /api/register`  
*`Vulnerability: An attacker could spam this endpoint to create millions of fake accounts (resource exhaustion).`*  
*`Patch: The WAF can learn a baseline rate of requests from a single IP address. When it sees hundreds of requests per minute during an attack, it can flag this as anomalous behavior and block the IP.`*

* **`Request`**  
  `{`  
      `"username": "string",`  
      `"password": "string"`  
  `}`  
* **`Response`**  
  `{`  
      `"userId": 12345,`  
      `"username": "someuser",`  
      `"message": "User registered successfully. Please log in."`  
  `}`

`[🔒] Delete Account POST /api/accounts`

* **`Request`**

`{`  
    `"username": "string",`  
    `"password": "string"`  
`}`

* **`Response`**

	`{`  
    `"status": "success"`  
`}`

`Login POST /api/login`  
*`Vulnerability: Credential Stuffing / Brute Force. An attacker can try thousands of password combinations.`*  
*`Patch: WOOF will see a high rate of failed login attempts (401 Unauthorized responses) from a specific IP. It can learn that more than 10 failed logins per minute is an anomaly and temporarily block the source.`*  
*`Vulnerability: SQL Injection`*  
*`Patch: WOOF will recognize SQL injection when logging in and block requests which contain this.`*

* **`Request`**  
  `{`  
      `"username": "string",`  
      `"password": "string"`  
  `}`  
* **`Response`**  
  `{`  
      `"token": "your_jwt_or_session_token_here"`  
  `}`

`[🔒] View Account GET /api/users/{userId}`  
*`Vulnerability: Allows User A to see User B's balance.`*  
*`Patch: WOOF is trained on "good" traffic where the {userId} in the URL path always matches the userId inside the JWT token. A malicious request (GET /api/users/56789/account from a user whose token says they are userId: 12345) breaks this learned pattern, and the WAF can block it.`*

* **`Request`**  
* **`Response`**  
  `{`  
      `"userId": 12345,`  
      `"balance": 5430.50`  
  `}`

`[🔒] View Me GET /api/me`  
*`Vulnerability: The API handler is poorly written and returns sensitive data, like the user's password hash, along with non-sensitive data.`*  
*`Patch: This is where response-based training shines. WOOF is trained on "good" responses, learning that a valid response for this endpoint has the schema { "userId", "username" }. When a "malicious" (leaky) response comes back containing an extra field like "passwordHash", the WAF can block the response and log a security alert, preventing the sensitive data from reaching the client.`*

* **`Request`**  
* **`Response`**  
  `{`  
      `"userId": 12345,`  
      `"username": "someuser",`  
      `"passwordHash": "sha256_hash_of_password_here"`   
  `}`

`[🔒] Transfer Funds POST /api/transactions`  
*`Vulnerability: The API blindly trusts the fromUserId field in the request body, allowing an attacker to make a transfer from an account that isn't theirs.`*  
*`Patch: Similar to BOLA, WOOF learns the rule that body.fromUserId must match the userId in the JWT token.`*  
*`Vulnerability: The API allows a user to transfer a negative amount, effectively stealing money from the recipient.`*  
*`Patch: WOOF can learn a schema for this request. By training it on valid requests where amount is always a positive number, it can create a rule that amount must be > 0. A request with amount: -100 would violate this learned business rule and be blocked.`*

* **`Request`**  
  `{`  
      `"fromUserId": 12345,`  
      `"toUserId": 56789,`  
      `"amount": 100.00,`  
      `"description": "string"`  
  `}`  
* **`Response`**  
  `{`  
      `"status": "success",`  
      `"transactionId": 903`  
  `}`

`[🔒] Get Transactions GET /api/accounts/{userId}/transactions/`  
*`Vulnerability: Same as above. An attacker can view the transaction history of any other user by changing the {userId} in the URL.`*  
*`Patch: Same as above. The WAF enforces the rule that the {userId} in the URL must match the userId in the authentication token.`*

* **`Request`**  
* **`Response`**  
  `[`  
      `{ "transactionId": 901, "amount": -50.00, "description": "Coffee Shop" },`  
      `{ "transactionId": 902, "amount": 1200.00, "description": "Paycheck" }`  
  `]`

`[🔒] Search Transactions GET /api/accounts/{userId}/transactions/search?description=coffee`  
*`Vulnerability: The backend naively concatenates the description query parameter into a SQL query, allowing an attacker to manipulate the database.`*  
*`Patch: The WAF is trained on "good" requests where description is a simple string (e.g., coffee, paycheck). A malicious request (description=coffee' OR 1=1;--) contains characters (', ;, --) and patterns that the WAF can immediately identify as a known SQLi attack signature and block.`*

* **`Request`**  
* **`Response`**  
  `[`  
      `{ "transactionId": 901, "amount": -50.00, "description": "Coffee Shop" }`  
  `]`
