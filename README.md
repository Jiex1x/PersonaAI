# PersonalBrand.AI

PersonalBrand.AI is a multi-agent collaboration platform for personal brand incubation. It helps users establish their professional presence through automated brand strategy development.

## Features

- 🎯 Brand Identity Development
- 💡 Unique Strengths Analysis
- 👥 Target Audience Definition
- 📝 Content Strategy Planning
- 📅 Launch Schedule Creation

## Technology Stack

- Backend: FastAPI
- LLM: OpenAI API (GPT-4)
- Search: Azure Cognitive Search
- Storage: Azure Blob Storage
- Agent Orchestration: Semantic Kernel

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your credentials
5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Environment Variables

The following environment variables are required:

- `OPENAI_API_KEY`: Your OpenAI API key
- `AZURE_SEARCH_SERVICE_ENDPOINT`: Your Azure Cognitive Search service endpoint
- `AZURE_SEARCH_ADMIN_KEY`: Your Azure Cognitive Search admin key
- `AZURE_SEARCH_INDEX_NAME`: The name of your search index

## Health Checks

The application provides a health check endpoint at `/test-services` that verifies the connection to all required services. You can use this endpoint to ensure all services are properly configured and accessible.

Example response:
```json
{
  "status": "ok",
  "services": {
    "openai": {
      "status": "ok",
      "error": null
    },
    "azure_search": {
      "status": "ok",
      "error": null
    }
  }
}
```

## Project Structure

```
personalbrand-ai/
├── app/
│   ├── agents/         # Agent implementations
│   ├── core/           # Core functionality
│   ├── models/         # Data models
│   ├── services/       # External services
│   └── main.py        # FastAPI application
├── tests/             # Test cases
└── docs/              # Documentation
```

## Contributing

This project is part of the Microsoft AI Agent Competition. Contributions are welcome! 