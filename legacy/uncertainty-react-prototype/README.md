# Interactive Worksheet System: Probability & Uncertainty (Middle School)

An elegant, high-fidelity, interactive math worksheet ecosystem tailored for middle school students, optimized for both tablet interaction and flawless, unbranded physical A4 printing.

This repository holds the code for **"תחום וודאות"** (Certainty Domain), built in React 18+ with TypeScript, Vite, and Tailwind CSS.

---

## 🚀 How to Synchronize Your Work to GitHub

Since you are using **Google AI Studio Build**, you can easily sync every file in this workspace to your personal GitHub repository. Here are the two ways to do this:

### Option A: The AI Studio One-Click Export (Easiest)
1. At the top of the AI Studio Build page, locate the **Settings / Menu** icon (or the project share options).
2. Choose **"Export to GitHub"**.
3. Authenticate with your GitHub account when prompted.
4. Select or create your new repository (`i-vadaut-ai-studio`).
5. AI Studio will automatically push all current code folders (including the `/src`, `/public`, package configurations, and this documentation) directly to your new repository!

---

### Option B: Manual Command-Line Setup (If running locally)
If you downloaded the code as a ZIP file (via settings "Export to ZIP"), unzip it, open your terminal inside the project directory, and run:

```bash
# 1. Initialize git local repo
git init

# 2. Add all files to stage
git add .

# 3. Commit the changes
git commit -m "Initial commit: probability and uncertainty worksheet system"

# 4. Create your main branch
git branch -M main

# 5. Connect to your newly created GitHub repository
git remote add origin https://github.com/yanivmizrachiy/i-vadaut-ai-studio.git

# 6. Push code to GitHub
git push -u origin main
```

---

## 📁 Workspace Portfolio Structure

```text
├── package.json               # Package dependencies, build & dev configuration scripts
├── tsconfig.json              # TypeScript compilation setup
├── vite.config.ts             # Vite server & tailwind bundling configuration
├── metadata.json              # Applet configuration & permissions
├── RULES_AND_REQUIREMENTS.md  # FULL Hebrew math curriculum worksheet rules & design guide
├── src/                       # React Codebase
│   ├── main.tsx               # Client entry-point
│   ├── App.tsx                # Main Interactive Worksheet Dashboard, Live preview & Simulation Engine
│   └── index.css              # Global styles & Google font imports (Inter, JetBrains Mono)
└── public/                    # Static / Pre-rendered assets
    └── worksheet/
        └── student-pages/     # Pure, clean, client-facing print pages (No UI menus, no branding)
            ├── question-01/
            │   ├── index.html # High-fidelity static question web page
            │   └── styles.css # Exact print styles, matching the ivory-white A4 page geometry
            ├── question-02/ ... (Question folders 2 through 8)
```

---

## ⚙️ Running Locally

To launch this application locally on your computer:

```bash
# 1. Install required packages
npm install

# 2. Run the Vite development server
npm run dev
```

The app will start at `http://localhost:3000` with hot-reloading active.

---

## 🎨 Visual Craft Guidelines
- **Color Palette**: Hybrid Academic Blue (`#112b4c`), Slate Grey (`#274266`), Ivory White (`#fafaf9`).
- **Typography**: Display headings in Inter/system-ui paired with monospace outputs in JetBrains Mono.
- **Physical Sizing**: Perfect `210mm` x `297mm` bounding box with nested page flex layouts ensuring content never overflows pages during print.
