import sys
import asyncio
import aiohttp
import discord
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget, QMessageBox, QListWidgetItem, QDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QCursor


class CreditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Credits")
        self.setFixedSize(300, 100)
        layout = QVBoxLayout()

        credit_label = QLabel("This application was created by OctoPass")
        layout.addWidget(credit_label)

        discord_label = QLabel(".octopass")
        discord_label.setStyleSheet("text-decoration: underline; color: blue;")
        discord_label.setCursor(QCursor(Qt.PointingHandCursor))
        discord_label.mousePressEvent = self.copy_discord
        layout.addWidget(discord_label)

        self.setLayout(layout)

    def copy_discord(self, event):
        QApplication.clipboard().setText(".octopass")
        QMessageBox.information(self, "Copied", "Discord username copied to clipboard!")


class DialogSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discord Dialog Simulator")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.setup_ui()
        self.load_data()
        self.add_credits()
    def setup_ui(self):
        # Bot Token
        token_layout = QHBoxLayout()
        token_layout.addWidget(QLabel("Bot Token:"))
        self.token_input = QLineEdit()
        token_layout.addWidget(self.token_input)
        self.layout.addLayout(token_layout)

        # Webhook URLs
        webhook_layout = QHBoxLayout()
        webhook_layout.addWidget(QLabel("Webhook URL 1:"))
        self.webhook1_input = QLineEdit()
        webhook_layout.addWidget(self.webhook1_input)
        self.layout.addLayout(webhook_layout)

        webhook_layout2 = QHBoxLayout()
        webhook_layout2.addWidget(QLabel("Webhook URL 2:"))
        self.webhook2_input = QLineEdit()
        webhook_layout2.addWidget(self.webhook2_input)
        self.layout.addLayout(webhook_layout2)

        # Character List
        char_list_layout = QHBoxLayout()
        self.character_list = QListWidget()
        char_list_layout.addWidget(self.character_list)
        self.delete_char_button = QPushButton("Delete Character")
        self.delete_char_button.clicked.connect(self.delete_character)
        char_list_layout.addWidget(self.delete_char_button)
        self.layout.addWidget(QLabel("Characters:"))
        self.layout.addLayout(char_list_layout)

        # Add Character
        add_char_layout = QHBoxLayout()
        self.char_name_input = QLineEdit()
        self.char_avatar_input = QLineEdit()
        add_char_layout.addWidget(self.char_name_input)
        add_char_layout.addWidget(self.char_avatar_input)
        self.add_char_button = QPushButton("Add Character")
        self.add_char_button.clicked.connect(self.add_character)
        add_char_layout.addWidget(self.add_char_button)
        self.layout.addLayout(add_char_layout)

        # Conversation
        conv_layout = QHBoxLayout()
        self.conversation = QTextEdit()
        self.conversation.setReadOnly(True)
        conv_layout.addWidget(self.conversation)
        self.delete_message_button = QPushButton("Delete Last Message")
        self.delete_message_button.clicked.connect(self.delete_last_message)
        conv_layout.addWidget(self.delete_message_button)
        self.layout.addWidget(QLabel("Conversation:"))
        self.layout.addLayout(conv_layout)

        # Message Input
        message_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        message_layout.addWidget(self.message_input)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.add_message)
        message_layout.addWidget(self.send_button)
        self.layout.addLayout(message_layout)

        # Start Simulation
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Simulation")
        self.start_button.clicked.connect(self.start_simulation)
        button_layout.addWidget(self.start_button)

        # Clear All Data
        self.clear_all_button = QPushButton("Clear All Data")
        self.clear_all_button.clicked.connect(self.clear_all_data)
        button_layout.addWidget(self.clear_all_button)

        self.layout.addLayout(button_layout)

    def load_data(self):
        conn = sqlite3.connect('dialog_simulator.db')
        c = conn.cursor()

        # Create tables if not exist
        c.execute('''CREATE TABLE IF NOT EXISTS config
                     (key TEXT PRIMARY KEY, value TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS characters
                     (name TEXT PRIMARY KEY, avatar_url TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS conversation
                     (id INTEGER PRIMARY KEY, name TEXT, message TEXT)''')

        # Load config
        c.execute("SELECT * FROM config")
        config = dict(c.fetchall())
        self.token_input.setText(config.get('bot_token', ''))
        self.webhook1_input.setText(config.get('webhook1', ''))
        self.webhook2_input.setText(config.get('webhook2', ''))

        # Load characters
        c.execute("SELECT * FROM characters")
        for name, avatar_url in c.fetchall():
            self.character_list.addItem(f"{name}: {avatar_url}")

        # Load conversation
        c.execute("SELECT name, message FROM conversation ORDER BY id")
        for name, message in c.fetchall():
            self.conversation.append(f"{name}: {message}")

        conn.close()

    def add_character(self):
        name = self.char_name_input.text()
        avatar = self.char_avatar_input.text()
        if name and avatar:
            self.character_list.addItem(f"{name}: {avatar}")
            self.save_character(name, avatar)
            self.char_name_input.clear()
            self.char_avatar_input.clear()

    def delete_character(self):
        current_item = self.character_list.currentItem()
        if current_item:
            name = current_item.text().split(':')[0]
            self.character_list.takeItem(self.character_list.row(current_item))
            self.delete_character_from_db(name)

    def delete_character_from_db(self, name):
        conn = sqlite3.connect('dialog_simulator.db')
        c = conn.cursor()
        c.execute("DELETE FROM characters WHERE name = ?", (name,))
        conn.commit()
        conn.close()

    def add_message(self):
        message = self.message_input.text()
        if message:
            selected_items = self.character_list.selectedItems()
            if selected_items:
                character = selected_items[0].text().split(':')[0]
                self.conversation.append(f"{character}: {message}")
                self.save_message(character, message)
                self.message_input.clear()

    def delete_last_message(self):
        text = self.conversation.toPlainText()
        lines = text.split('\n')
        if lines:
            lines.pop()
            self.conversation.setPlainText('\n'.join(lines))
            self.delete_last_message_from_db()

    def delete_last_message_from_db(self):
        conn = sqlite3.connect('dialog_simulator.db')
        c = conn.cursor()
        c.execute("DELETE FROM conversation WHERE id = (SELECT MAX(id) FROM conversation)")
        conn.commit()
        conn.close()

    def save_character(self, name, avatar_url):
        conn = sqlite3.connect('dialog_simulator.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO characters VALUES (?, ?)", (name, avatar_url))
        conn.commit()
        conn.close()

    def save_message(self, name, message):
        conn = sqlite3.connect('dialog_simulator.db')
        c = conn.cursor()
        c.execute("INSERT INTO conversation (name, message) VALUES (?, ?)", (name, message))
        conn.commit()
        conn.close()

    def start_simulation(self):
        self.save_config()
        self.simulation_thread = SimulationThread(
            self.token_input.text(),
            self.webhook1_input.text(),
            self.webhook2_input.text(),
            self.get_character_config(),
            self.get_conversation_data()
        )
        self.simulation_thread.message_sent.connect(self.on_message_sent)
        self.simulation_thread.error_occurred.connect(self.on_error)
        self.simulation_thread.finished.connect(self.on_simulation_finished)
        self.simulation_thread.start()
        self.start_button.setEnabled(False)
#aaa
    def save_config(self):
        conn = sqlite3.connect('dialog_simulator.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO config VALUES (?, ?)", ('bot_token', self.token_input.text()))
        c.execute("INSERT OR REPLACE INTO config VALUES (?, ?)", ('webhook1', self.webhook1_input.text()))
        c.execute("INSERT OR REPLACE INTO config VALUES (?, ?)", ('webhook2', self.webhook2_input.text()))
        conn.commit()
        conn.close()

    def get_character_config(self):
        config = {}
        for i in range(self.character_list.count()):
            name, avatar_url = self.character_list.item(i).text().split(': ')
            config[name] = {"avatar_url": avatar_url}
        return config

    def get_conversation_data(self):
        conn = sqlite3.connect('dialog_simulator.db')
        c = conn.cursor()
        c.execute("SELECT name, message FROM conversation ORDER BY id")
        data = [{"name": name, "message": message} for name, message in c.fetchall()]
        conn.close()
        return data

    def on_message_sent(self, message):
        self.conversation.append(message)

    def on_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)

    def on_simulation_finished(self):
        self.start_button.setEnabled(True)
        QMessageBox.information(self, "Simulation Completed", "The dialog simulation has finished.")

    def clear_all_data(self):
        reply = QMessageBox.question(self, 'Clear All Data',
                                     'Are you sure you want to clear all data? This action cannot be undone.',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            conn = sqlite3.connect('dialog_simulator.db')
            c = conn.cursor()
            c.execute("DELETE FROM config")
            c.execute("DELETE FROM characters")
            c.execute("DELETE FROM conversation")
            conn.commit()
            conn.close()

            self.token_input.clear()
            self.webhook1_input.clear()
            self.webhook2_input.clear()
            self.character_list.clear()
            self.conversation.clear()
            self.char_name_input.clear()
            self.char_avatar_input.clear()
            self.message_input.clear()

            QMessageBox.information(self, "Data Cleared", "All data has been cleared successfully.")

    def add_credits(self):
        credits_button = QPushButton("Created by OctoPass", self)
        credits_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: gray;
            }
            QPushButton:hover {
                color: black;
            }
        """)
        credits_button.setCursor(QCursor(Qt.PointingHandCursor))
        credits_button.clicked.connect(self.show_credits)

        credits_layout = QHBoxLayout()
        credits_layout.addStretch()
        credits_layout.addWidget(credits_button)

        self.layout.addLayout(credits_layout)

    def show_credits(self):
        credit_dialog = CreditDialog(self)
        credit_dialog.exec_()


class SimulationThread(QThread):
    message_sent = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, bot_token, webhook1, webhook2, character_config, conversation_data):
        super().__init__()
        self.bot_token = bot_token
        self.webhook_urls = [webhook1, webhook2]
        self.character_config = character_config
        self.conversation_data = conversation_data

    def run(self):
        asyncio.run(self.simulate_dialog())

    async def simulate_dialog(self):
        intents = discord.Intents.default()
        intents.members = True
        client = discord.Client(intents=intents)
        try:
            await client.login(self.bot_token)
            self.message_sent.emit("Logged in as: " + str(client.user))

            async with aiohttp.ClientSession() as session:
                for i, message in enumerate(self.conversation_data):
                    webhook_url = self.webhook_urls[i % 2]
                    name = message["name"]
                    avatar_url = self.character_config[name]["avatar_url"]
                    if avatar_url.isdigit():
                        avatar_url = await self.fetch_avatar(client,
                                                             avatar_url) or "https://cdn.discordapp.com/embed/avatars/0.png"
                    try:
                        await self.send_webhook_message(
                            session,
                            webhook_url,
                            message["message"],
                            name,
                            avatar_url
                        )
                        self.message_sent.emit(f"Message sent: {name}: {message['message'][:30]}...")
                    except Exception as e:
                        self.error_occurred.emit(f"Error sending message: {str(e)}")
                    await asyncio.sleep(2)  # Pause between messages

            self.message_sent.emit("Dialog simulation completed.")
        except Exception as e:
            self.error_occurred.emit(f"Error in simulation: {str(e)}")
        finally:
            await client.close()
            self.finished.emit()

    async def fetch_avatar(self, client, user_id):
        try:
            user = await client.fetch_user(int(user_id))
            return str(user.avatar.url) if user.avatar else None
        except discord.NotFound:
            return None

    async def send_webhook_message(self, session, webhook_url, content, username, avatar_url):
        data = {
            "content": content,
            "username": username,
            "avatar_url": avatar_url
        }
        async with session.post(webhook_url, json=data) as response:
            if response.status != 204:
                error_text = await response.text()
                self.error_occurred.emit(f"Error sending message. Status: {response.status}, Error: {error_text}")
            else:
                self.message_sent.emit(f"Message sent successfully: {content[:30]}...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DialogSimulator()
    window.show()
    sys.exit(app.exec_())