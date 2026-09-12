# Setup & Deployment Guide for `khushboocodes`

This repository creates a specialized GitHub Profile README featuring:
1. **Cyberpunk Terminal Card** (`dark.svg` / `light.svg`) with your animated ASCII portrait, terminal window title, scanning radar, neofetch-style system info, and typing effects.
2. **Arcade Jet Contribution Heatmap** (`dist/github-jet.svg`) where an animated fighter jet patrols your contribution calendar, shooting bullets and blasting your peak contribution days.

---

## 🚀 Quick Step-by-Step Deployment

### Step 1: Create your Special Profile Repository on GitHub
1. Go to [github.com/new](https://github.com/new).
2. Set **Repository name** to:
   ```
   khushboocodes
   ```
   *(GitHub will show a green banner: "You found a secret! khushboocodes/khushboocodes is a special repository...")*
3. Make sure it is set to **Public**.
4. Leave "Add a README file" **unchecked** (since we already have our custom `README.md`).
5. Click **Create repository**.

---

### Step 2: Push this Project from Your Machine

Open your terminal in this directory (`c:\Users\loq\Downloads\khushboocodes`) and run:

```bash
# Initialize git
git init
git branch -M main

# Stage and commit all files
git add .
git commit -m "feat: initialize cyberpunk profile with ascii terminal card and jet heatmap"

# Link to your new repository
git remote add origin https://github.com/khushboocodes/khushboocodes.git

# Push to GitHub
git push -u origin main
```

---

### Step 3: Enable GitHub Actions Write Permissions (One-Time)
So that GitHub Actions can automatically refresh your jet heatmap daily:

1. In your GitHub repository `khushboocodes/khushboocodes`:
2. Navigate to **Settings** -> **Actions** -> **General**.
3. Scroll down to **Workflow permissions**.
4. Choose **Read and write permissions**.
5. Check **Allow GitHub Actions to create and approve pull requests**.
6. Click **Save**.

---

### Step 4: Run the Action Manually (Optional)
To verify everything is running smoothly on GitHub:
1. Click the **Actions** tab in your repository.
2. Select **Update Jet Heatmap SVG** from the left sidebar.
3. Click **Run workflow** -> **Run workflow**.

---

## 🛠️ Local Development & Customization

### Re-generating the Jet Heatmap locally
```bash
# Works without any token by scraping public contributions:
node generate.mjs

# Or test with mock preview data:
node preview-test.mjs
```

### Customizing the Terminal Profile & ASCII Portrait
- If you ever want to update the portrait image, replace `portrait.txt` with new ASCII art and run:
  ```bash
  python ascii_to_svg.py
  python build_svgs.py
  ```
- To customize the information displayed on the right panel (role, skills, bio), edit `build_svgs.py` and run `python build_svgs.py`.
