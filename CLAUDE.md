# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Serverless Devs project for deploying a FastAPI application to Aliyun Function Compute 3.0 (FC3). The application exposes a simple HTTP endpoint and uses GitHub Actions for CI/CD deployment.

Key components:
- `app.py`: FastAPI application with FC3-compatible handler function
- `s.yaml`: Serverless Devs configuration for FC3 deployment
- `.github/workflows/test.yml`: GitHub Actions workflow for automated deployment
- `requirements.txt`: Python dependencies (FastAPI, Uvicorn, ASGIref)

## Development Environment Setup

### Prerequisites
- Python 3.10 (matches FC3 runtime)
- Node.js 24+ (for Serverless Devs CLI)
- Aliyun account with Function Compute access

### Local Setup
1. Create and activate a Python virtual environment:
   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Serverless Devs CLI globally:
   ```bash
   npm install -g @serverless-devs/s@3.1.10
   ```

4. Configure Aliyun credentials (required for deployment):
   ```bash
   s config add --AccessKeyID <your-access-key-id> --AccessKeySecret <your-access-key-secret> -a default -f
   ```

5. Install the FC3 component:
   ```bash
   s add devsapp/fc3 -y
   ```

## Local Development and Testing

### Running FastAPI Locally
For standard FastAPI development (without FC3 event format):
```bash
uvicorn app:app --reload --port 8000
```
The app will be available at `http://localhost:8000`. Note: This bypasses the FC3 handler and uses standard FastAPI ASGI server.

### Testing FC3 Handler Locally
To test the FC3-compatible handler with simulated events, use Serverless Devs local invocation:
```bash
# Create a test event file (test-event.json)
echo '{"httpMethod": "GET", "path": "/"}' > test-event.json

# Invoke locally
s local invoke -e test-event.json
```

## Deployment

### Manual Deployment
1. Ensure dependencies are installed locally (they will be packaged):
   ```bash
   pip install -r requirements.txt -t .
   ```

2. Deploy to Aliyun FC3:
   ```bash
   s deploy -y --debug
   ```

   Environment variables needed:
   - `ALIYUN_ACCOUNT_ID`: Your Aliyun account ID
   - `ALIYUN_REGION`: Deployment region (default: cn-shenzhen)

### CI/CD Deployment
The GitHub Actions workflow (`.github/workflows/test.yml`) automatically deploys on push to `master` branch or manual trigger. It performs:
- Python 3.10 setup
- Dependency installation (packaged with `-t .`)
- Serverless Devs configuration (using GitHub Secrets)
- FC3 component installation
- Deployment with debug output

### Configuration
The `s.yaml` file defines:
- Service: `fc-fastapi-service`
- Function: `fc-fastapi-function`
- Runtime: `python3.10`
- Handler: `app.handler`
- Memory: 256MB, Timeout: 30s
- HTTP trigger with anonymous auth supporting GET/POST

## Architecture Notes

### FC3 Handler Pattern
The `handler(event, context)` function in `app.py` adapts FC3 HTTP events to FastAPI responses:
- Receives FC3 event object with `httpMethod`, `path`, `headers`, `queryParameters`, `body`
- Returns response with `statusCode`, `headers`, `body` format
- Currently only handles root path (`/`) GET requests; other routes return 404

### Dependencies Packaging
FC3's `installDependency: true` may not reliably install dependencies at runtime. The CI/CD workflow installs dependencies locally (`-t .`) before deployment, ensuring they are included in the deployment package.

### Secrets Management
- GitHub Secrets store: `ACCESSKEYID`, `ACCESSKEYSECRET`, `ALIYUN_ACCOUNT_ID`, `ALIYUN_REGION`
- Local development uses `s config add` to store credentials in `~/.s/access.yaml`

## Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
This occurs when dependencies are not packaged with the deployment. Solutions:
1. Install dependencies locally before deployment: `pip install -r requirements.txt -t .`
2. Use WebIDE in Aliyun console to manually install: `pip install -r requirements.txt -t /code`
3. Consider using FC3 Layers for dependency management

### "Code config must be a string or an object..."
Ensure `code:` field in `s.yaml` is a string path (`./`) not an object with `src` and `type` fields. FC3 only accepts string paths or OSS object references.

### Local Testing Differences
The FC3 handler expects event format different from standard HTTP requests. Use `s local invoke` for accurate testing rather than direct HTTP requests to uvicorn.