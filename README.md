# DisDialogue — Discord Dialog Simulator | Симулятор диалогов Discord

[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/github/license/OctoPassik/DisDialogue)](https://github.com/OctoPassik/DisDialogue/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/OctoPassik/DisDialogue)](https://github.com/OctoPassik/DisDialogue/stargazers)
[![GitHub Release](https://img.shields.io/github/v/release/OctoPassik/DisDialogue)](https://github.com/OctoPassik/DisDialogue/releases)

![Discord Dialog Simulator](https://i.imgur.com/Z4OUzsn.png)

**DisDialogue** is a free, open-source **Discord conversation simulator** and **Discord dialog generator** built with Python and PyQt5. It allows you to prototype, test, and create multi-character Discord conversations using webhooks — without cluttering your real Discord servers.

**DisDialogue** — бесплатный **симулятор диалогов Discord** с открытым исходным кодом. Создавайте и тестируйте многопользовательские диалоги Discord с помощью вебхуков, не засоряя реальные серверы.

---

## What is DisDialogue? | Что такое DisDialogue?

DisDialogue is a **desktop application** that simulates realistic Discord conversations by sending messages through Discord webhooks. It's designed for:

- **Discord bot developers** who need to test dialog flows
- **Community managers** who want to prototype conversations
- **Content creators** preparing Discord screenshots and demos
- **Roleplay communities** setting up scripted interactions
- **Discord server admins** testing moderation scenarios

## Key Features | Основные возможности

- **Multi-character conversations** — simulate dialogs between multiple Discord users with unique names and avatars
- **Real Discord webhooks** — messages appear as real messages in your Discord channel
- **Custom avatars** — use Discord User IDs to fetch real avatars, or provide direct image URLs
- **Persistent storage** — all characters, messages, and settings are saved between sessions (SQLite)
- **Adjustable message delay** — control timing between messages (1–60 seconds)
- **Bilingual interface** — English and Russian language support
- **User-friendly GUI** — clean PyQt5 graphical interface, no command-line needed
- **Windows executable** — download and run without installing Python

## Installation | Установка

### Option 1: Download Windows Executable (Recommended)

1. Go to the [Releases page](https://github.com/OctoPassik/DisDialogue/releases)
2. Download the latest `DisDialogue.exe`
3. Run the executable — no installation required

### Option 2: Run from Source (Python)

**Requirements:** Python 3.7 or higher

```bash
# Clone the repository
git clone https://github.com/OctoPassik/DisDialogue.git
cd DisDialogue

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Dependencies

| Package | Purpose |
|---------|---------|
| [PyQt5](https://pypi.org/project/PyQt5/) | Desktop GUI framework |
| [aiohttp](https://pypi.org/project/aiohttp/) | Async HTTP requests to Discord API |
| [discord.py](https://pypi.org/project/discord.py/) | Discord API integration |
| [certifi](https://pypi.org/project/certifi/) | SSL/TLS certificates |

## How to Use | Как использовать

### 1. Configure Bot Token and Webhook

- Enter your **Discord bot token** (needed to fetch user avatars)
  - Get it from [Discord Developer Portal](https://discord.com/developers/applications)
- Enter your **Discord webhook URL**
  - Create one in: Server Settings → Integrations → Webhooks

### 2. Add Characters

- Enter a **character name** and either:
  - A **Discord User ID** — the app will fetch their real avatar
  - A **direct image URL** (`.png`, `.jpg`, `.jpeg`, `.gif`) — used as the avatar

### 3. Compose Dialog

- Select a character from the list
- Type a message and click **Send**
- Repeat to build the full conversation

### 4. Run Simulation

- Set the **delay** between messages (1–60 seconds)
- Click **Start Simulation**
- Watch messages appear in your Discord channel in real time

### 5. Manage Data

- Delete individual characters or messages
- Use **Clear All Data** for a fresh start
- All data persists automatically between sessions

## Screenshot | Скриншот

![DisDialogue Screenshot](https://images-ext-1.discordapp.net/external/FnuBiejIm9z-EtJ3vOLWeEtCCtiJPaupinj7kYHgYe0/https/i.imgur.com/Pp6qrCB.png?format=webp&quality=lossless&width=706&height=591)

## Use Cases | Варианты использования

| Use Case | Description |
|----------|-------------|
| **Bot Testing** | Test how your Discord bot responds to multi-user conversations |
| **Server Setup** | Prototype welcome messages and onboarding dialogs |
| **Content Creation** | Create realistic Discord conversation screenshots |
| **Roleplay** | Set up scripted roleplay scenarios with multiple characters |
| **Moderation Training** | Simulate scenarios for moderator training |
| **Demo Videos** | Generate realistic Discord activity for tutorials and demos |

## FAQ | Часто задаваемые вопросы

**Q: Is DisDialogue free?**
A: Yes, DisDialogue is completely free and open-source.

**Q: Does it work on macOS / Linux?**
A: Yes, when running from source with Python. The `.exe` release is Windows-only.

**Q: Is this against Discord ToS?**
A: Webhooks are an official Discord feature. DisDialogue uses them as intended — for sending messages to channels. Use responsibly.

**Q: Can I simulate more than 2 characters?**
A: Yes, you can add as many characters as you need.

## Contributing | Вклад в проект

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/OctoPassik/DisDialogue/issues).

## Author | Автор

**OctoPass**

- Discord: `.octopass`
- GitHub: [@OctoPassik](https://github.com/OctoPassik)

## Keywords

Discord dialog simulator, Discord conversation generator, Discord webhook simulator, Discord chat simulator, Discord message simulator, Discord roleplay tool, Discord bot testing tool, симулятор диалогов Discord, генератор разговоров Discord, симулятор чата Discord, Discord webhook tool, fake Discord conversation, Discord dialog creator, Discord conversation maker

---

<p align="center">Made with ❤️ and ☕</p>
