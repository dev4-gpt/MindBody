# Setup Guide - Using Virtual Environment

## ✅ Yes, you should use a virtual environment!

Using a virtual environment (venv) is **essential** for Python projects. It:
- Keeps dependencies isolated from your system Python
- Prevents conflicts between projects
- Makes it easier to manage versions
- Is a Python best practice

## Step-by-Step Setup

### 1. Navigate to Project Root

```bash
cd "/.../AI health coach"
```

### 2. Create Virtual Environment

```bash
# Create venv (using Python 3.11.6 from pyenv)
python3.11 -m venv venv

# Or if pyenv is set up:
pyenv shell 3.11.6
python -m venv venv
```

### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt after activation.

### 4. Upgrade pip (Recommended)

```bash
pip install --upgrade pip
```

### 5. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 6. Install Frontend Dependencies (if needed)

```bash
cd ../frontend
# Streamlit is already in backend requirements, but if you want it separate:
pip install streamlit requests pillow
```

### 7. Verify Installation (if needed)

```bash
# Check installed packages
pip list

# Test imports
python -c "import fastapi; import streamlit; print('✅ All imports successful')"
```

## Running the Application

### Start Backend (Terminal 1)

```bash
# Make sure venv is activated
source venv/bin/activate  # if not already activated

cd backend
python -m app.main

# Or:
uvicorn app.main:app --reload --port 8000
```

### Start Frontend (Terminal 2)

```bash
# Make sure venv is activated
source venv/bin/activate  # if not already activated

cd frontend
streamlit run streamlit_app.py
```

### OR In AI health coach/

```bash
source venv/bin/activate

python test_system.py 
```

And follow the rules inside

## Deactivating Virtual Environment

When you're done working:

```bash
deactivate
```

## Troubleshooting

### Issue: "command not found" after activation

**Solution:** Make sure you activated the venv:
```bash
source venv/bin/activate
```

### Issue: Wrong Python version

**Solution:** Create venv with specific Python:
```bash
pyenv shell 3.11.6
python3.11 -m venv venv
source venv/bin/activate
```

### Issue: Packages not found after installation

**Solution:** Make sure venv is activated and you're in the right directory:
```bash
which python  # Should show venv path
pip list      # Should show installed packages
```

### Issue: sqlite3 error

**Fixed!** I've removed sqlite3 from requirements.txt since it's built-in to Python.

## Quick Reference

```bash
# Create venv
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Deactivate
deactivate
```

## Why Virtual Environment?

Without venv:
- ❌ Packages install to system Python
- ❌ Can cause conflicts with other projects
- ❌ Hard to manage different versions
- ❌ Can break system Python

With venv:
- ✅ Isolated environment per project
- ✅ No conflicts with other projects
- ✅ Easy to recreate environment
- ✅ Safe to experiment
- ✅ Standard Python practice

