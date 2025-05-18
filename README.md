# SPFScanner

**SPFScanner** is a fast and flexible Minecraft server port scanner created by @ganduspl.  
It helps you find open Minecraft servers on any IP and port range, with colorful output and automatic result saving.

---

## ✨ Features

- Scans any IP and port range for open Minecraft servers (Java Edition)
- Uses [mcsrvstat.us](https://api.mcsrvstat.us/) API for reliable server info (MOTD, version, player count)
- Colorful terminal output (MOTD with Minecraft color codes)
- Smart skipping of empty port ranges for faster scanning
- Results saved automatically to the `Results/` folder with timestamp and server count
- Graceful exit and result saving on Ctrl+C

---

## 🚀 Quick Start

1. **Install requirements**  
   Run in your terminal:
   ```
   pip install -r requirements.txt
   ```

2. **Run the scanner**
   ```
   python spfscanner.py
   ```

3. **Follow the prompts**  
   Enter the IP and starting port, choose scan direction, and let SPFScanner do the rest!

---

## 📁 Output

- Results are saved in the `Results/` folder.
- Filenames include the date, time, and number of servers found, e.g.  
  `2025-05-18_20-15-30_found3_servers.txt`

---

## 🛠️ Requirements

- Python 3.8+
- See `requirements.txt` for required packages

---

## ⚡ Example Output

```
Scanning 127.0.0.1:25565-25575...
Server detected: 127.0.0.1:25565 | §bSLASHMC.PL | Version: 1.20.4 | Players: 10/100
```

---

## 📜 License

Feel free to use and modify this script for educational purposes!

---

**Made with ❤️ by @ganduspl**
