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
- LLM: Azure OpenAI (GPT-4)
- Search: Azure Cognitive Search
- Storage: Azure Blob Storage
- Agent Orchestration: Semantic Kernel

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Jiex1x/PersonaAI.git
   cd PersonaAI
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and fill in your Azure credentials

5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
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