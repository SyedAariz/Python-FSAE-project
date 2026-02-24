## Getting Started


1. **Open a terminal in the folder where you want the project to be**:

2. **Clone the repository** (from the root of the project):

   ```bash
   git clone https://github.com/SyedAariz/Python-FSAE-project.git
   cd Python-FSAE-project
   ```

3. **Make sure you are in main branch**:

   ```bash
   git checkout main
   ```
4. (Optional) Create Virtual Environment
Recommended for Python project:

```bash
python3 -m venv venv
source venv/bin/activate
```
5. Run the Project

```bash
python3 main.py
```

## Daily Workflow

### Starting Work

Always make sure you’re up to date before creating a new branch:

```bash
git checkout main
git pull origin main            # get the latest changes
git checkout -b feature/your-task   # create a new branch
```

### After Finishing Your Work

Before committing, make sure your code runs without errors.

```bash
git add .
git commit -m "Describe what you did"
git push origin feature/your-task
```

Then open a **Pull Request** on GitHub to merge your branch into `main`.
