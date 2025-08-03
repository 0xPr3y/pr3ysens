
# 🛡️ pr3ySens — System & Network Diagnostic Tool (CLI)

**pr3ySens** is a command-line diagnostic tool for Windows that performs basic and advanced scans to help detect issues in system configuration, connectivity, and open network ports.

It highlights suspicious or dangerous connections, organizes results for quick review, and stores full output logs for further analysis.

> ⚠️ **This is an educational project and work in progress.**  
> Future updates will include more features, better error handling, and smarter classification logic.

---

## ⚙️ Features

- **Default Scan**: Basic tools like `ipconfig`, `ping`, `netstat -an`
- **Full Scan**: Extended system and network diagnostics (`systeminfo`, `tasklist`, `tracert`, `sfc`, etc.)
- **Custom Scan**: Choose scan type manually (system, network, processes)
- **Port Classification**: Detects `important`, `suspicious`, and `high alert` ports
- **Colored Output**: ANSI colors for clear visual feedback (no external dependencies)
- **Log Output**: Saves all command results to `scanOutput.txt`

---

## 🧪 Usage

```bash
python pr3ysens.py
```

Choose the scan mode you want from the menu.

---

## 📦 Requirements

- Python 3.6+
- Works best on Windows 10+
- No external libraries required

---

## 🧠 About This Project

This is a **learning-based project** created to explore Python system tools, subprocess management, and CLI formatting.

Expect future improvements in:
- Port intelligence
- Scan presets and automation
- Report exporting (CSV/JSON)
- UI enhancements (nicer terminal output)

Made with curiosity by **pr3y**.
