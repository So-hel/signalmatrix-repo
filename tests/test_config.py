import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app.config import settings
    print("✅ Configuration loaded successfully.")
    print(f"GITHUB_TOKEN: {'****' + settings.github_token[-4:] if settings.github_token else 'MISSING'}")
    print(f"AI_PROVIDER: {settings.ai_provider}")
    print(f"OPENAI_API_KEY: {'****' + settings.openai_api_key[-4:] if settings.openai_api_key else 'MISSING'}")
    print(f"OPENAI_MODEL: {settings.openai_model}")
    print(f"BLACKBOX_API_KEY: {'****' + settings.blackbox_api_key[-4:] if settings.blackbox_api_key else 'MISSING'}")
    print(f"BLACKBOX_MODEL: {settings.blackbox_model}")
except Exception as e:
    print(f"❌ Configuration loading failed: {e}")
    sys.exit(1)
