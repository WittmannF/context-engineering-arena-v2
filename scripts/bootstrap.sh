#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=== Context Engineering Arena — Bootstrap ==="
echo ""

# Check Python >= 3.11
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 not found. Install Python 3.11+ and try again."
  exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]; }; then
  echo "ERROR: Python 3.11+ required. Found Python $PYTHON_VERSION."
  exit 1
fi
echo "  Python $PYTHON_VERSION — OK"

# Check Node >= 18
if ! command -v node &>/dev/null; then
  echo "ERROR: node not found. Install Node.js 20+ and try again."
  exit 1
fi

NODE_VERSION=$(node --version | sed 's/v//')
NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d. -f1)

if [ "$NODE_MAJOR" -lt 18 ]; then
  echo "ERROR: Node.js 18+ required. Found Node.js $NODE_VERSION."
  exit 1
fi
echo "  Node.js $NODE_VERSION — OK"

# Check uv
if ! command -v uv &>/dev/null; then
  echo "ERROR: uv not found. Install with: pip install uv"
  exit 1
fi
echo "  uv $(uv --version 2>/dev/null | head -1) — OK"

echo ""

# Create data directories
echo "--- Creating data directories..."
mkdir -p data/raw data/processed data/samples
touch data/raw/.gitkeep data/processed/.gitkeep data/samples/.gitkeep

# Create generated site data directory
mkdir -p packages/site/src/data/generated

echo ""

# Python environment
echo "--- Setting up Python environment..."
cd arena
uv venv .venv --quiet
source .venv/bin/activate
uv pip install -e . --quiet
cd "$ROOT"
echo "  arena-cli installed."

echo ""

# Node dependencies
echo "--- Installing site dependencies..."
cd packages/site
npm install --silent
cd "$ROOT"
echo "  Node modules installed."

echo ""

# Build initial catalog
echo "--- Building initial catalog..."
source arena/.venv/bin/activate
python -m arena_cli.cli build-catalog

echo ""
echo "=== Bootstrap complete! ==="
echo ""
echo "Next steps:"
echo ""
echo "  Start dev server:"
echo "    cd packages/site && npm run dev"
echo ""
echo "  Validate everything:"
echo "    source arena/.venv/bin/activate"
echo "    python -m arena_cli.cli validate"
echo ""
echo "  Download sample data:"
echo "    python -m arena_cli.cli download-data --task task-001-enron-investigation --sample"
echo "    python -m arena_cli.cli prepare-data --task task-001-enron-investigation"
echo ""
echo "  List available tasks:"
echo "    python -m arena_cli.cli list-tasks"
echo ""
