# SPFScanner

**SPFScanner** is a fast Minecraft server port scanner created by @ganduspl.  
it helps you find open Minecraft servers on any IP and port ranges

---
![image](https://github.com/user-attachments/assets/1dc52adf-bcb0-48a2-938e-0908ef8f4b71)

## ✨ Features

- Scans any IP and port range for open Minecraft servers (Java Edition)
- Uses [mcsrvstat.us](https://api.mcsrvstat.us/) API for reliable server info (MOTD, version, player count)
- Colorful terminal output (MOTD with Minecraft color codes)
- Smart skipping of empty port ranges for faster scanning
- Results saved automatically to the `Results/` folder with timestamp and server count

---

## 🚀 How to start scanning

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
   Enter the IP and starting port, choose scan direction, and let SPFScanner scan

---

## 📁 Output / Results

- Results are saved in the `Results/` folder.
- Filenames include the date, time, and number of servers found,
  `2025-05-18_20-15-30_found3_servers.txt`

---

## 🛠️ Requirements

- Python 3.8+
- See `requirements.txt` for required packages

---

## ⚡ Example Output

```
Scanning 127.0.0.1:25565-25575...
Server detected: 127.0.0.1:25565 | MOTD | Version: 1.20.4 | Players: 10/100
```

---

## 📜 License

Feel free to use and modify this script for educational purposes :D

---

**Made with 💖 by @ganduspl**
