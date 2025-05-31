# Safe Python Script Execution API

This project is a secure Python script execution API service built with Flask and [nsjail](https://github.com/google/nsjail). It safely runs user-submitted Python code inside an isolated sandbox and returns the result of the `main()` function.

## 🚀 Features

- Accepts Python scripts via POST to `/execute`
- Executes in a sandboxed Linux environment using nsjail
- Returns:
  - `result`: the return value from `main()`
  - `stdout`: everything printed by the script
- Enforces memory and time limits
- Validates input and handles errors gracefully
- Lightweight Docker image, deployable to Cloud Run

---

## 📦 Example Request

### ✅ Curl (Local Docker Test)

```bash
curl -X POST http://localhost:8080/execute -H "Content-Type: application/json" -d "{"script": "def main():\n    print(\"Hello from script\")\n    return {\"status\": \"success\"}\n\nif __name__ == \"__main__\":\n    import json\n    print(json.dumps(main()))"}"
```

---

## 🐳 Running Locally with Docker

```bash
docker build -t safe-python-executor .
docker run -p 8080:8080 safe-python-executor
```

---

## ☁️ Cloud Run Deployment

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/safe-python-executor
gcloud run deploy safe-python-executor \
  --image gcr.io/YOUR_PROJECT_ID/safe-python-executor \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars=USE_NSJAIL=0
```

> Replace `YOUR_PROJECT_ID` with your GCP project ID.

---

## 🌐 Example with Cloud Run

```bash
curl -Method POST "https://safe-python-runner-191785419969.us-central1.run.app/execute" -ContentType "application/json" -Body '{"script": "import json\n\ndef main():\n    print(\"Hello from main!\")\n    result = {\"status\": \"success\", \"value\": 42}\n    print(json.dumps(result))\n\nif __name__ == \"__main__\":\n    main()"}'
```

```bash
Invoke-RestMethod -Method Post -Uri "https://safe-python-runner-191785419969.us-central1.run.app/execute" -ContentType "application/json" -Body '{"script": "import json\ndef main():\n print(\"Hello from main!\")\n result = {\"status\": \"success\", \"value\": 42}\n print(json.dumps(result))\n\nif __name__ == \"__main__\":\n main()"}'  
```

---

## 📝 Notes

- The script **must define `main()`** and print its return value as valid JSON.
- Errors are handled gracefully and returned in the `error` field.
- Stdout is captured separately.

---
