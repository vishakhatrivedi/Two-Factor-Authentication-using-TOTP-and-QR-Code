# Two-Factor-Authentication-using-TOTP-and-QR-Code
This secure TOTP project leverages Flask, MySQL, JavaScript and HTML to ensure secure user logins. Users enjoy a streamlined setup with QR code integration for TOTP, enhancing overall security. The application's backend, powered by MySQL, efficiently stores user login data and audit logs, providing a comprehensive and secure authentication solution. 
It also features a GPT 3.5 Turbo Powered Chatbot with tokens limited to 30 per search and ensures to generate complete sentences. This chatbot integration can have future scope in fields like college dashboards, employee dashboard, file management system etc. 

**Run:**
- ```python app.py``` in the terminal starts the development server.
<img width="778" alt="image" src="https://github.com/vishakhatrivedi/Two-Factor-Authentication-using-TOTP-and-QR-Code/assets/91044422/5273404e-a033-4a9e-af65-3182315b0403">


**Login/Register:**

<img width="333" alt="image" src="https://github.com/vishakhatrivedi/Two-Factor-Authentication-using-TOTP-and-QR-Code/assets/91044422/5764a9a0-8217-4cfc-b6fc-ecd6706b1f75">

-The MySQL database stores the details of the user automatically.

<img width="393" alt="image" src="https://github.com/vishakhatrivedi/Two-Factor-Authentication-using-TOTP-and-QR-Code/assets/91044422/09ee7951-b179-4871-b7f1-77639dc5dc7d">


**Scanning the QR code and entering a time based OTP (TOTP):**

<img width="300" alt="image" src="https://github.com/vishakhatrivedi/Two-Factor-Authentication-using-TOTP-and-QR-Code/assets/91044422/61048589-2257-4ec3-be96-225c0ce3b1ec">

- Scan the QR code using any authentication app, such as Google Authenticator.

 
 **Chatbot:**
 
<img width="929" alt="image" src="https://github.com/vishakhatrivedi/Two-Factor-Authentication-using-TOTP-and-QR-Code/assets/91044422/0de3fed1-40cb-4545-b43d-ac655454c725">


On logging out, the MySQL database stores the audit log with login and log out time.

<img width="407" alt="image" src="https://github.com/vishakhatrivedi/Two-Factor-Authentication-using-TOTP-and-QR-Code/assets/91044422/582aafb6-c13d-4eb1-8e88-40f73415e67a">
