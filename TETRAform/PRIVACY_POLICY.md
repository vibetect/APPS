# Privacy Policy for TetraForm

**Last Updated:** December 11, 2025

TetraForm ("we", "our", or "us") is committed to protecting your privacy. This Privacy Policy explains how your information is collected, used, and disclosed by the TetraForm Chrome Extension.

## 1. Information Collection and Use

### Local Storage
TetraForm is designed with a "privacy-first" approach. The primary function of the extension is to save and autofill form data.
*   **All profile data**, including names, addresses, emails, and phone numbers, is stored **locally on your device** using Chrome's secure storage API (`chrome.storage.local`).
*   This data **never leaves your computer** under normal operation of the core autofill features. We do not have access to your saved profiles.

### External Services (Firebase)
We use Google Firebase for specific, optional features:
1.  **Authentication**: If you create an account to sync settings or access premium features, your email and authentication credentials are securely managed by Firebase Authentication.
2.  **Feedback Submission**: If you use the "Send Feedback" form within the extension, the message and your email (if provided) are sent to our database hosted on Cloud Firestore.
3.  **Analytics (Optional)**: We may collect anonymous usage data (e.g., number of profiles created, daily usage counts) to improve the extension. This data is not linked to your personal profile information.

## 2. Permissions

TetraForm requires specific permissions to function:

*   **`storage`**: To save your profiles locally on your device.
*   **`activeTab`** & **`scripting`**: To detect forms on the page you are visiting and insert the autofill data when you request it.
*   **`host_permissions` (<all_urls>)**: TetraForm is a general-purpose form filler. It needs to be able to run on any website where you might encounter a form. We do not track your browsing history. The extension only activates its script when it detects a form or when you manually trigger it.

## 3. Data Security

*   We prioritize the security of your data. Local data is sandboxed by the Chrome browser.
*   Network communications for feedback or authentication are encrypted using industry-standard HTTPS/TLS protocols.
*   **Sensitive Data**: We explicitly **block** the saving of highly sensitive fields such as Credit Card numbers (CVV), passwords, and CAPTCHA codes to prevent accidental storage of critical secrets.

## 4. Updates to This Policy

We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last Updated" date.

## 5. Contact Us

If you have any questions about this Privacy Policy, please contact us via the feedback form in the extension settings.
