Here is a **professional, GitHub-ready `README.md`** for your SafeRename project. You can copy-paste it directly.

---

# 🧠 SafeRename

**Offline Intelligent File Renaming System with Transaction Safety**

SafeRename is a privacy-first desktop application designed to safely scan, analyze, and rename large batches of files and folders. It focuses on **data integrity, rollback safety, and intelligent filename sanitization**, making it ideal for managing messy media libraries and corrupted file naming structures.

---

## 🚀 Features

* 🔍 Recursive folder scanning (deep directory support)
* 🧹 Smart filename sanitization (emoji & invalid character removal)
* 📦 Batch renaming engine for large file sets
* 🔄 Transaction-based execution system (safe commit model)
* ↩️ Undo / rollback last rename operation
* ⚡ Concurrent execution for improved performance
* 🧩 Collision detection & auto-resolution
* 👁️ Preview mode before execution (before → after mapping)
* 🔐 Fully offline (no internet dependency, no telemetry)

---

## 🏗️ Architecture Overview

SafeRename follows a modular, layered architecture inspired by production-grade systems:

* **Scanner Layer** → Recursively collects file metadata
* **Sanitization Layer** → Cleans and normalizes filenames
* **Transaction Engine** → Ensures atomic rename operations
* **Execution Scheduler** → Orders operations safely
* **Concurrency Layer** → Parallel execution support
* **Rollback System** → Recovery from failures

---

## 🖥️ Tech Stack

* Python 3.x
* CustomTkinter (UI framework)
* pathlib (filesystem operations)
* threading / concurrent.futures (parallel execution)
* Modular architecture design

---

## 📦 Installation


### 1. Create virtual environment (recommended)

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the application

```bash
python app/main.py
```

---

## 🧪 How It Works

1. Select a folder
2. System scans all files recursively
3. Filenames are analyzed and sanitized
4. Preview shows original vs cleaned names
5. User confirms execution
6. Safe transactional rename is executed
7. Rollback data is stored locally

---

## 🔒 Privacy & Security

* 100% offline operation
* No cloud sync
* No telemetry or tracking
* Local rollback storage only
* Safe transaction execution model

---

## 📌 Use Cases

* Cleaning mobile-to-PC transferred files
* Removing emojis from filenames
* Organizing large media libraries
* Preparing datasets for ML workflows
* Fixing corrupted or invalid filenames

---

## ⚠️ Safety Design

SafeRename uses a **transaction-style rename system**, meaning:

* Operations are staged before execution
* Conflicts are resolved before commit
* Rollback data is stored locally
* Partial failure does not corrupt file structure

---

## 📁 Project Structure (Simplified)

```
SafeRename/
│
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── scanner/
│   │   ├── sanitizer/
│   │   ├── transaction_engine/
│   │   ├── concurrency/
│   │   └── rename_engine/
│   ├── ui/
│   └── utils/
│
├── venv/
├── requirements.txt
└── README.md
```

---

## 📈 Roadmap

* [x] File scanning engine
* [x] Sanitization system
* [x] Transaction-based renaming
* [x] Undo/rollback support
* [x] Concurrent execution


---

## 🧑‍💻 Author

Built as a systems-level engineering project focused on:

* filesystem safety
* transactional integrity
* offline-first design
* scalable batch processing


