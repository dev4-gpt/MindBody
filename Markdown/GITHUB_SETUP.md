# GitHub Setup Guide

## Step-by-Step Instructions

### 1. Initialize Git Repository

```bash
cd "/Users/aryamandev/AI health coach"
git init
```

### 2. Add All Files

```bash
git add .
```

### 3. Create Initial Commit

```bash
git commit -m "Initial commit: Multi-agent orchestration framework for MindBody Strength Coach

- Multi-agent orchestration engine
- 3 specialized agents (Pose, Nutrition, Mindfulness)
- 12 domain-specific tools
- Guardrails and safety system
- Context-aware memory
- FastAPI backend
- Streamlit frontend
- Support for 10 exercises
- Video analysis support"
```

### 4. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `MindBody` (or your preferred name)
3. Description: "Multi-agent orchestration framework for real-time exercise form correction, nutrition estimation, and mindfulness coaching"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 5. Add Remote and Push

After creating the repo, GitHub will show you commands. Use these:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/dev4-gpt/MindBody.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 6. Verify

Check your GitHub repository - all files should be there!

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
# Login to GitHub
gh auth login

# Create repo and push in one command
gh repo create mindbody-strength-coach --public --source=. --remote=origin --push
```

## Troubleshooting

### If you get authentication errors:

**Option 1: Use Personal Access Token**
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token with `repo` permissions
3. Use token as password when pushing

**Option 2: Use SSH**
```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: Settings > SSH and GPG keys
# Then use SSH URL:
git remote set-url origin git@github.com:YOUR_USERNAME/mindbody-strength-coach.git
```

### If you need to update later:

```bash
git add .
git commit -m "Your commit message"
git push
```

## What Gets Pushed

✅ All source code
✅ Documentation
✅ Configuration files
✅ Docker files

❌ Virtual environment (venv/) - excluded by .gitignore
❌ Environment variables (.env) - excluded
❌ Python cache files - excluded
❌ Large model files - excluded

