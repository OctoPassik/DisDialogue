import sys
import asyncio
import aiohttp
import ssl
import certifi
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QTextEdit, QListWidget, QMessageBox, QListWidgetItem, QDialog, QSpinBox, QMenu
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QCursor
import sqlite3
from datetime import datetime


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help / Помощь")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        lang_layout = QHBoxLayout()

        self.en_button = QPushButton("🇺🇸 English")
        self.ru_button = QPushButton("🇷🇺 Русский")

        self.en_button.setCheckable(True)
        self.ru_button.setCheckable(True)
        self.en_button.setChecked(True)  

        button_style = """
            QPushButton {
                padding: 5px 15px;
                border: 1px solid 
                border-radius: 3px;
                background-color: 
            }
            QPushButton:checked {
                background-color: 
                border: 2px solid 
            }
        """
        self.en_button.setStyleSheet(button_style)
        self.ru_button.setStyleSheet(button_style)

        self.en_button.clicked.connect(lambda: self.switch_language('en'))
        self.ru_button.clicked.connect(lambda: self.switch_language('ru'))

        lang_layout.addWidget(self.en_button)
        lang_layout.addWidget(self.ru_button)
        lang_layout.addStretch()

        layout.addLayout(lang_layout)

        self.content = QTextEdit()
        self.content.setReadOnly(True)
        layout.addWidget(self.content)

        self.setLayout(layout)
        self.help_content = {
            'en': """
<h2>Discord Dialog Simulator - Help Guide</h2>
<h3>Main Components</h3>
<h4>Bot Token</h4>
• The bot token is required to fetch real Discord user avatars
• You can get it from the Discord Developer Portal:
  1. Go to https:
  2. Create a new application or select existing one
  3. Go to "Bot" section
  4. Click "Add Bot" if needed
  5. Copy the token
<h4>Webhook URL</h4>
• Required to send messages to your Discord channel
• To get it:
  1. Go to your Discord server
  2. Edit channel settings
  3. Go to "Integrations" → "Webhooks"
  4. Create or copy existing webhook URL
<h4>Characters</h4>
• You can add characters in two ways:
  1. Using Discord User ID - will fetch real user's avatar
  2. Using direct image URL - will use provided image as avatar
• To get Discord User ID:
  1. Enable Developer Mode in Discord settings
  2. Right-click on user → Copy ID
<h4>Simulation Settings</h4>
• Delay - time between messages (1-60 seconds)
• Messages are sent in the order they appear in the conversation list
• You can edit/delete messages before starting simulation

<h4>Tips</h4>
• Test webhook URL before starting long simulations
• Use reasonable delays to avoid rate limiting
• Make sure bot token has necessary permissions if using user avatars
• You can use right-click menu to delete messages
• All data is saved automatically and persists between program restarts
""",
            'ru': """
<h2>Discord Dialog Simulator - Руководство</h2>

<h3>Основные компоненты</h3>

<h4>Токен бота (Bot Token)</h4>
• Токен бота необходим для получения реальных аватаров пользователей Discord
• Как получить токен:
  1. Перейдите на https:
  2. Создайте новое приложение или выберите существующее
  3. Перейдите в раздел "Bot"
  4. Нажмите "Add Bot" если нужно
  5. Скопируйте токен

<h4>URL вебхука (Webhook URL)</h4>
• Необходим для отправки сообщений в ваш канал Discord
• Как получить:
  1. Зайдите на ваш сервер Discord
  2. Откройте настройки канала
  3. Перейдите в "Интеграции" → "Вебхуки"
  4. Создайте новый или скопируйте существующий URL вебхука

<h4>Персонажи (Characters)</h4>
• Можно добавлять персонажей двумя способами:
  1. Используя ID пользователя Discord - будет использован реальный аватар
  2. Используя прямую ссылку на изображение - будет использована указанная картинка
• Как получить ID пользователя Discord:
  1. Включите режим разработчика в настройках Discord
  2. ПКМ по пользователю → Копировать ID

<h4>Настройки симуляции</h4>
• Задержка - время между сообщениями (1-60 секунд)
• Сообщения отправляются в том порядке, в котором они находятся в списке
• Можно редактировать/удалять сообщения перед запуском симуляции

<h4>Советы</h4>
• Проверяйте URL вебхука перед запуском длинных симуляций
• Используйте разумные задержки, чтобы избежать ограничений Discord
• Убедитесь, что у бота есть необходимые разрешения при использовании аватаров
• Используйте контекстное меню для удаления сообщений
• Все данные сохраняются автоматически и сохраняются между запусками программы
"""
        }

        self.switch_language('en')

    def switch_language(self, lang):
        if lang == 'en':
            self.en_button.setChecked(True)
            self.ru_button.setChecked(False)
        else:
            self.en_button.setChecked(False)
            self.ru_button.setChecked(True)

        self.content.setHtml(self.help_content[lang])
class CreditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Credits")
        self.setFixedSize(300, 150)
        layout = QVBoxLayout()

        credit_label = QLabel("This application was created by OctoPass")
        layout.addWidget(credit_label)

        tester_label = QLabel("Tested by Caramelka")
        layout.addWidget(tester_label)

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
        self.setGeometry(100, 100, 1000, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.setup_ui()
        self.load_data()
        self.add_credits()

        self.simulation_thread = None

    def setup_ui(self):

        token_layout = QHBoxLayout()
        token_layout.addWidget(QLabel("Bot Token:"))
        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.Password)
        token_layout.addWidget(self.token_input)

        self.toggle_token_button = QPushButton("Show")
        self.toggle_token_button.setCheckable(True)
        self.toggle_token_button.toggled.connect(self.toggle_token_view)
        token_layout.addWidget(self.toggle_token_button)
        self.main_layout.addLayout(token_layout)

        webhook_layout = QHBoxLayout()
        webhook_layout.addWidget(QLabel("Webhook URL:"))
        self.webhook_input = QLineEdit()
        webhook_layout.addWidget(self.webhook_input)
        self.main_layout.addLayout(webhook_layout)

        char_list_layout = QHBoxLayout()
        self.character_list = QListWidget()
        char_list_layout.addWidget(self.character_list)

        char_buttons_layout = QVBoxLayout()
        self.delete_char_button = QPushButton("Delete Character")
        self.delete_char_button.clicked.connect(self.delete_character)
        char_buttons_layout.addWidget(self.delete_char_button)
        char_list_layout.addLayout(char_buttons_layout)

        self.main_layout.addWidget(QLabel("Characters:"))
        self.main_layout.addLayout(char_list_layout)

        add_char_layout = QHBoxLayout()
        self.char_name_input = QLineEdit()
        self.char_name_input.setPlaceholderText("Character Name")
        self.char_avatar_input = QLineEdit()
        self.char_avatar_input.setPlaceholderText("User ID or Avatar URL")
        add_char_layout.addWidget(self.char_name_input)
        add_char_layout.addWidget(self.char_avatar_input)
        self.add_char_button = QPushButton("Add Character")
        self.add_char_button.clicked.connect(self.add_character)
        add_char_layout.addWidget(self.add_char_button)
        self.main_layout.addLayout(add_char_layout)

        conv_log_layout = QHBoxLayout()

        conv_layout = QVBoxLayout()
        self.conversation = QListWidget()
        self.conversation.setContextMenuPolicy(Qt.CustomContextMenu)
        self.conversation.customContextMenuRequested.connect(self.show_context_menu)
        conv_layout.addWidget(QLabel("Conversation:"))
        conv_layout.addWidget(self.conversation)

        conv_buttons_layout = QHBoxLayout()
        self.clear_conversation_button = QPushButton("Clear Conversation")
        self.clear_conversation_button.clicked.connect(self.clear_conversation)
        conv_buttons_layout.addWidget(self.clear_conversation_button)

        self.delete_selected_message_button = QPushButton("Delete Selected Message")
        self.delete_selected_message_button.clicked.connect(self.delete_selected_message)
        conv_buttons_layout.addWidget(self.delete_selected_message_button)

        conv_layout.addLayout(conv_buttons_layout)
        conv_log_layout.addLayout(conv_layout)

        logs_layout = QVBoxLayout()
        logs_layout.addWidget(QLabel("Logs:"))
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        logs_layout.addWidget(self.logs)
        conv_log_layout.addLayout(logs_layout)

        self.main_layout.addLayout(conv_log_layout)

        message_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        message_layout.addWidget(self.message_input)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.add_message)
        message_layout.addWidget(self.send_button)
        self.main_layout.addLayout(message_layout)

        delay_layout = QHBoxLayout()
        delay_layout.addWidget(QLabel("Delay (seconds):"))
        self.delay_input = QSpinBox()
        self.delay_input.setMinimum(1)
        self.delay_input.setMaximum(60)
        self.delay_input.setValue(2)
        delay_layout.addWidget(self.delay_input)
        self.main_layout.addLayout(delay_layout)

        self.control_buttons_layout = QHBoxLayout()

        self.start_button = QPushButton("Start Simulation")
        self.start_button.clicked.connect(self.start_simulation)
        self.control_buttons_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Simulation")
        self.stop_button.clicked.connect(self.stop_simulation)
        self.stop_button.setEnabled(False)
        self.control_buttons_layout.addWidget(self.stop_button)

        self.clear_all_button = QPushButton("Clear All Data")
        self.clear_all_button.clicked.connect(self.clear_all_data)
        self.control_buttons_layout.addWidget(self.clear_all_button)

        self.help_button = QPushButton("❓ Help")
        self.help_button.clicked.connect(self.show_help)
        self.control_buttons_layout.addWidget(self.help_button)

        self.main_layout.addLayout(self.control_buttons_layout)

    def show_help(self):
        help_dialog = HelpDialog(self)
        help_dialog.exec_()

    def toggle_token_view(self, checked):
        self.token_input.setEchoMode(
            QLineEdit.Normal if checked else QLineEdit.Password
        )
        self.toggle_token_button.setText("Hide" if checked else "Show")

    def load_data(self):
        conn = sqlite3.connect('dialog_simulator.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS config
                     (key TEXT PRIMARY KEY, value TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS characters
                     (name TEXT PRIMARY KEY, avatar_url TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS conversation
                     (id INTEGER PRIMARY KEY, name TEXT, message TEXT)''')

        c.execute("SELECT * FROM config")
        config = dict(c.fetchall())
        self.token_input.setText(config.get('bot_token', ''))
        self.webhook_input.setText(config.get('webhook', ''))

        c.execute("SELECT * FROM characters")
        for name, avatar_url in c.fetchall():
            self.character_list.addItem(f"{name}: {avatar_url}")

        c.execute("SELECT name, message FROM conversation ORDER BY id")
        for name, message in c.fetchall():
            self.conversation.addItem(f"{name}: {message}")

        conn.close()

    def add_character(self):
        name = self.char_name_input.text()
        avatar = self.char_avatar_input.text()
        if name and avatar:

            if avatar.isdigit() or (avatar.startswith('http') and avatar.endswith(('.png', '.jpg', '.jpeg', '.gif'))):
                self.character_list.addItem(f"{name}: {avatar}")
                self.save_character(name, avatar)
                self.char_name_input.clear()
                self.char_avatar_input.clear()
            else:
                QMessageBox.warning(self, "Invalid Input", "Avatar must be either a Discord User ID or a direct image URL")

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

    def show_context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("Delete Message")
        action = menu.exec_(self.conversation.mapToGlobal(position))
        if action == delete_action:
            self.delete_selected_message()

    def delete_selected_message(self):
        current_item = self.conversation.currentItem()
        if current_item:
            row = self.conversation.row(current_item)
            self.conversation.takeItem(row)
            self.delete_message_from_db(row)
        else:
            QMessageBox.warning(self, "Warning", "Please select a message to delete.")

    def delete_message_from_db(self, row):
        conn = sqlite3.connect('dialog_simulator.db')
        c = conn.cursor()
        c.execute("DELETE FROM conversation WHERE id = (SELECT id FROM conversation ORDER BY id LIMIT 1 OFFSET ?)",
                  (row,))
        conn.commit()
        conn.close()

    def clear_conversation(self):
        self.conversation.clear()
        conn = sqlite3.connect('dialog_simulator.db')
        c = conn.cursor()
        c.execute("DELETE FROM conversation")
        conn.commit()
        conn.close()

    def add_message(self):
        message = self.message_input.text().strip()
        if not message:
            QMessageBox.warning(self, "Warning", "Please enter a message.")
            return

        selected_items = self.character_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "Please select a character before sending a message.")
            return

        try:

            character = selected_items[0].text().split(':')[0].strip()

            list_item = QListWidgetItem(f"{character}: {message}")
            self.conversation.addItem(list_item)

            conn = None
            try:
                conn = sqlite3.connect('dialog_simulator.db')
                c = conn.cursor()
                c.execute("INSERT INTO conversation (name, message) VALUES (?, ?)",
                          (character, message))
                conn.commit()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error",
                                     f"Failed to save message to database: {str(e)}")

                self.conversation.takeItem(self.conversation.row(list_item))
            finally:
                if conn:
                    conn.close()

            self.message_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 f"An unexpected error occurred: {str(e)}")
            return

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

        bot_token = self.token_input.text().strip()
        if not bot_token:
            QMessageBox.warning(self, "Warning", "Please enter a bot token before starting the simulation.")
            return

        webhook_url = self.webhook_input.text().strip()
        if not webhook_url:
            QMessageBox.warning(self, "Warning", "Please enter a webhook URL before starting the simulation.")
            return

        valid_patterns = [
            'https://discord.com/api/webhooks/',
            'https://discordapp.com/api/webhooks/'
        ]

        if not any(webhook_url.startswith(pattern) for pattern in valid_patterns):
            QMessageBox.warning(
                self,
                "Warning",
                "Invalid webhook URL. Please enter a valid Discord webhook URL starting with:\n"
                "- https://discord.com/api/webhooks/\n"
                "- https://discordapp.com/api/webhooks/"
            )
            return

        conversation_data = self.get_conversation_data()
        if not conversation_data:
            QMessageBox.warning(self, "Warning",
                                "Please add some messages to the conversation before starting simulation.")
            return

        try:

            self.save_config()

            self.simulation_thread = SimulationThread(
                bot_token,
                webhook_url,
                self.get_character_config(),
                conversation_data,
                self.delay_input.value()
            )

            self.simulation_thread.message_sent.connect(self.on_message_sent)
            self.simulation_thread.error_occurred.connect(self.on_error)
            self.simulation_thread.finished.connect(self.on_simulation_finished)

            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.logs.append("Starting simulation...")

            self.simulation_thread.start()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start simulation: {str(e)}")
            self.on_simulation_finished()

    def on_message_sent(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")

    def on_error(self, error_message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        error_log = f"[{timestamp}] Error: {error_message}"
        self.logs.append(error_log)

        if "webhook" in error_message.lower() or "connection" in error_message.lower():
            QMessageBox.critical(self, "Error", error_message)

    def on_simulation_finished(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.logs.append("Simulation completed.")

    def stop_simulation(self):
        if self.simulation_thread and self.simulation_thread.isRunning():
            self.simulation_thread.stop()
            self.simulation_thread.wait()
            self.on_simulation_finished()

    def on_simulation_finished(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.logs.append("Simulation completed.")
        QMessageBox.information(self, "Simulation Completed", "The dialog simulation has finished.")

    def save_config(self):
        conn = sqlite3.connect('dialog_simulator.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO config VALUES (?, ?)",
                  ('bot_token', self.token_input.text()))
        c.execute("INSERT OR REPLACE INTO config VALUES (?, ?)",
                  ('webhook', self.webhook_input.text()))
        conn.commit()
        conn.close()

    def get_character_config(self):
        config = {}
        for i in range(self.character_list.count()):
            name, avatar_url = self.character_list.item(i).text().split(': ')

            config[name] = {"avatar_url": avatar_url}
        return config
    def get_conversation_data(self):
        data = []
        for i in range(self.conversation.count()):
            item = self.conversation.item(i)
            name, message = item.text().split(': ', 1)
            data.append({"name": name, "message": message})
        return data

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
            self.webhook_input.clear()
            self.character_list.clear()
            self.conversation.clear()
            self.logs.clear()
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

        self.main_layout.addLayout(credits_layout)

    def show_credits(self):
        credit_dialog = CreditDialog(self)
        credit_dialog.exec_()

class SimulationThread(QThread):
    message_sent = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, bot_token, webhook, character_config, conversation_data, delay):
        super().__init__()
        self.bot_token = bot_token
        self.webhook_url = webhook
        self.character_config = character_config
        self.conversation_data = conversation_data
        self.delay = delay
        self.is_running = True

    def run(self):
        loop = None
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.simulate_dialog())
        except Exception as e:
            self.error_occurred.emit(f"Simulation error: {str(e)}")
        finally:
            if loop:
                loop.close()

    def stop(self):
        self.is_running = False

    async def simulate_dialog(self):
        try:
            # Создаём SSL контекст с сертификатами
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            connector = aiohttp.TCPConnector(ssl=ssl_context)

            async with aiohttp.ClientSession(connector=connector) as session:
                for message in self.conversation_data:
                    if not self.is_running:
                        break

                    try:
                        name = message["name"]
                        avatar_info = self.character_config[name]["avatar_url"]

                        if avatar_info.isdigit():
                            avatar_url = await self.get_avatar_by_id(session, avatar_info)
                        else:
                            avatar_url = avatar_info

                        await self.send_webhook_message(
                            session,
                            self.webhook_url,
                            message["message"],
                            name,
                            avatar_url
                        )

                        self.message_sent.emit(f"Message sent as {name}: {message['message'][:30]}...")
                        await asyncio.sleep(self.delay)

                    except Exception as e:
                        self.error_occurred.emit(f"Error processing message: {str(e)}")
                        await asyncio.sleep(1)
                        continue

        except Exception as e:
            self.error_occurred.emit(f"Simulation error: {str(e)}")
        finally:
            self.finished.emit()

    async def get_avatar_by_id(self, session, user_id: str) -> str:
        """Получает URL аватара пользователя Discord по его ID"""
        try:
            headers = {
                'Authorization': f'Bot {self.bot_token}',
                'User-Agent': 'DiscordWebhookSimulator/1.0'
            }
            async with session.get(
                f"https://discord.com/api/v10/users/{user_id}",
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    avatar_hash = data.get('avatar')
                    if avatar_hash:
                        ext = 'gif' if avatar_hash.startswith('a_') else 'png'
                        return f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.{ext}?size=256"
                else:
                    self.error_occurred.emit(f"API Error {response.status}: {await response.text()}")

            # Дефолтный аватар если не удалось получить
            default_id = int(user_id) % 5
            return f"https://cdn.discordapp.com/embed/avatars/{default_id}.png"
        except Exception as e:
            self.error_occurred.emit(f"Avatar fetch error: {str(e)}")
            return "https://cdn.discordapp.com/embed/avatars/0.png"

    async def send_webhook_message(self, session, webhook_url, content, username, avatar_url):
        """
        Отправляет сообщение через webhook с повторными попытками при ошибке.
        """
        data = {
            "content": content,
            "username": username,
            "avatar_url": avatar_url
        }

        max_retries = 3
        for attempt in range(max_retries):
            try:
                async with session.post(webhook_url, json=data) as response:
                    if response.status == 204:
                        return
                    error_text = await response.text()
                    if attempt == max_retries - 1:
                        self.error_occurred.emit(
                            f"Failed to send message after {max_retries} attempts. "
                            f"Status: {response.status}, Error: {error_text}"
                        )
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DialogSimulator()
    window.show()
    sys.exit(app.exec_())
