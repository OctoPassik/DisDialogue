# DisDialogue

![Discord Dialog Simulator](https://i.imgur.com/Z4OUzsn.png)

## 🎭 About

DisDialogue is a powerful Discord conversation simulator that uses webhooks to prototype and test multi-character interactions. It's perfect for developers, community managers, and Discord enthusiasts who want to experiment with dialogue flows without cluttering their actual Discord servers.

## ✨ Features

- 🤖 Simulate multi-character conversations
- 🎨 Customizable character avatars and names
- 💬 Real-time webhook message sending
- 🔄 User-friendly graphical interface
- 💾 Persistent data storage between sessions
- 🔐 Secure bot token and webhook URL management

## 🚀 Getting Started

### Option 1: Run from Source

#### Prerequisites

- Python 3.7+
- PyQt5
- aiohttp
- discord.py

#### Installation

1. Clone the repository:
   ```
   git clone https://github.com/OctoPassik/DisDialogue.git
   ```

2. Navigate to the project directory:
   ```
   cd DisDialogue
   ```

3. Install the required dependencies:
   ```
   pip install PyQt5 aiohttp discord.py
   ```

4. Run the application:
   ```
   python main.py
   ```

### Option 2: Windows Executable

1. Download the latest release from the [Releases page](https://github.com/OctoPassik/DisDialogue/releases).
2. Extract the zip file.
3. Run `DisDialogue.exe`.

## 🎮 How to Use

1. **Configure Bot and Webhooks**:
   - Enter your Discord bot token
   - Add two webhook URLs for message alternation

2. **Add Characters**:
   - Input character names and avatar URLs
   - Use Discord user IDs for dynamic avatar fetching

3. **Compose Messages**:
   - Select a character from the list
   - Type your message and hit "Send"

4. **Start Simulation**:
   - Click "Start Simulation" to begin sending messages via webhooks
   - Watch the conversation unfold in your Discord channel!

5. **Manage Data**:
   - Delete individual characters or messages as needed
   - Use "Clear All Data" for a fresh start

## 🛠 Advanced Usage

- **Custom Avatars**: Use direct image URLs or Discord user IDs for avatars
- **Message Timing**: Adjust the 2-second delay between messages in the code
- **Error Handling**: Check the application output for detailed error messages

## 📸 Screenshot
![DisDialogue Screenshot](https://i.imgur.com/SP9Gy2q.png)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/OctoPassik/DisDialogue/issues).

## 🙋‍♂️ Author

**OctoPass**

- Discord: .octopass
- Github: [@OctoPassik](https://github.com/OctoPassik)

---

<p align="center">Made with ❤️ and ☕</p>
