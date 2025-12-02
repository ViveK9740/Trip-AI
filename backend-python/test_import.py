import sys
import os
print(f"CWD: {os.getcwd()}")
print(f"Path: {sys.path}")

try:
    from utils.logger import setup_logger
    print("✅ Import utils.logger successful")
except Exception as e:
    print(f"❌ Import utils.logger failed: {e}")

try:
    from agents.orchestrator import orchestrator
    print("✅ Import agents.orchestrator successful")
except Exception as e:
    print(f"❌ Import agents.orchestrator failed: {e}")
