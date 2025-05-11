import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QWidget, QStackedWidget, QMessageBox,
    QGridLayout, QInputDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QTransform, QFont, QPainter, QColor

class PoleChudesGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Поле Чудес")
        self.setGeometry(100, 100, 800, 600)
        
        # Настройки игры
        self.difficulty = None
        self.words = {
            "Легкий": ["КОТ", "ДОМ", "СОН", "РОТ", "МАК"],
            "Средний": ["ПИТОН", "КОДИНГ", "ПРОГРАММА", "КЛАВИАТУРА"],
            "Сложный": ["АЛГОРИТМ", "ИСКУССТВЕННЫЙ", "ПРОГРАММИРОВАНИЕ"]
        }
        self.sectors = {
            "Легкий": ["+100", "+200", "+300", "ПРИЗ", "+500"],
            "Средний": ["+200", "+400", "+600", "ПРОПУСК ХОДА", "+1000"],
            "Сложный": ["+300", "+600", "+900", "БАНКРОТ", "+1500"]
        }
        
        # Игровые переменные
        self.hidden_word = ""
        self.guessed_word = []
        self.total_score = 0
        self.spin_angle = 0
        
        # Создаем стек виджетов
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Создаем экраны
        self.create_start_screen()
        self.create_game_screen()
    
    def create_start_screen(self):
        start_widget = QWidget()
        layout = QVBoxLayout()
        start_widget.setLayout(layout)
        
        # Установка стиля фона
        start_widget.setStyleSheet("""
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #2c3e50, stop:1 #4ca1af
            );
            border-radius: 15px;
        """)
        
        # Приветственное сообщение
        welcome_label = QLabel("Добро пожаловать в игру\n'Поле Чудес'!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #f1c40f;
            margin-bottom: 40px;
            text-shadow: 2px 2px 4px #000000;
        """)
        welcome_label.setFont(QFont("Arial", 32, QFont.Bold))
        layout.addWidget(welcome_label)
        
        # Подзаголовок
        subtitle_label = QLabel("Выберите уровень сложности:")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            font-size: 20px; 
            color: #ecf0f1;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px #000000;
        """)
        subtitle_label.setFont(QFont("Arial", 20))
        layout.addWidget(subtitle_label)
        
        # Кнопки сложности
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(20)
        buttons_layout.setContentsMargins(100, 0, 100, 0)
        
        # Кнопка легкого уровня
        easy_button = QPushButton("Легкий уровень")
        easy_button.setStyleSheet("""
            QPushButton {
                font-size: 20px; 
                padding: 15px;
                border-radius: 10px; 
                background-color: #27ae60; 
                color: white;
                min-width: 250px;
                border: 2px solid #ecf0f1;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        easy_button.clicked.connect(lambda: self.start_game("Легкий"))
        
        # Кнопка среднего уровня
        medium_button = QPushButton("Средний уровень")
        medium_button.setStyleSheet("""
            QPushButton {
                font-size: 20px; 
                padding: 15px;
                border-radius: 10px; 
                background-color: #f39c12; 
                color: white;
                min-width: 250px;
                border: 2px solid #ecf0f1;
            }
            QPushButton:hover {
                background-color: #f1c40f;
            }
        """)
        medium_button.clicked.connect(lambda: self.start_game("Средний"))
        
        # Кнопка сложного уровня
        hard_button = QPushButton("Сложный уровень")
        hard_button.setStyleSheet("""
            QPushButton {
                font-size: 20px; 
                padding: 15px;
                border-radius: 10px; 
                background-color: #e74c3c; 
                color: white;
                min-width: 250px;
                border: 2px solid #ecf0f1;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        hard_button.clicked.connect(lambda: self.start_game("Сложный"))
        
        buttons_layout.addWidget(easy_button)
        buttons_layout.addWidget(medium_button)
        buttons_layout.addWidget(hard_button)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        self.stacked_widget.addWidget(start_widget)
    
    def create_game_screen(self):
        self.game_widget = QWidget()
        game_layout = QVBoxLayout()
        self.game_widget.setLayout(game_layout)
        
        # Установка стиля фона
        self.game_widget.setStyleSheet("""
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #34495e, stop:1 #2c3e50
            );
        """)
        
        # Отображение уровня сложности
        self.difficulty_label = QLabel()
        self.difficulty_label.setAlignment(Qt.AlignCenter)
        self.difficulty_label.setStyleSheet("""
            font-size: 18px; 
            color: #ecf0f1;
            text-shadow: 1px 1px 2px #000000;
        """)
        game_layout.addWidget(self.difficulty_label)
        
        # Отображение очков
        self.score_label = QLabel("Очки: 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("""
            font-size: 24px; 
            color: #f1c40f;
            text-shadow: 1px 1px 2px #000000;
        """)
        game_layout.addWidget(self.score_label)
        
        # Сетка для отображения слова
        self.word_grid = QGridLayout()
        self.word_grid.setAlignment(Qt.AlignCenter)
        self.word_boxes = []
        game_layout.addLayout(self.word_grid)
        
        # Изображение барабана
        self.wheel_label = QLabel()
        self.wheel_pixmap = self.create_wheel_pixmap()
        self.wheel_label.setPixmap(self.wheel_pixmap)
        self.wheel_label.setAlignment(Qt.AlignCenter)
        self.wheel_label.setFixedSize(300, 300)
        game_layout.addWidget(self.wheel_label, alignment=Qt.AlignCenter)
        
        # Кнопка вращения барабана
        self.spin_button = QPushButton("Вращать барабан")
        self.spin_button.setStyleSheet("""
            QPushButton {
                font-size: 18px; 
                padding: 10px;
                border-radius: 10px; 
                background-color: #3498db; 
                color: white;
                border: 2px solid #ecf0f1;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.spin_button.clicked.connect(self.start_wheel_spin)
        game_layout.addWidget(self.spin_button, alignment=Qt.AlignCenter)
        
        # Поле для ввода буквы
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(100, 0, 100, 0)
        
        self.letter_input = QPushButton("Нажмите, чтобы ввести букву")
        self.letter_input.setStyleSheet("""
            QPushButton {
                font-size: 16px; 
                padding: 10px;
                border-radius: 10px; 
                background-color: #9b59b6; 
                color: white;
                border: 2px solid #ecf0f1;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.letter_input.clicked.connect(self.input_letter)
        input_layout.addWidget(self.letter_input)
        
        game_layout.addLayout(input_layout)
        
        # Таймер для анимации барабана
        self.spin_timer = QTimer()
        self.spin_timer.timeout.connect(self.update_wheel_rotation)
        
        self.stacked_widget.addWidget(self.game_widget)
    
    def create_wheel_pixmap(self):
        """Создает изображение барабана"""
        pixmap = QPixmap(300, 300)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Цвета секторов
        colors = [
            QColor("#3498db"), QColor("#e74c3c"), QColor("#2ecc71"),
            QColor("#f1c40f"), QColor("#9b59b6"), QColor("#1abc9c"),
            QColor("#e67e22"), QColor("#34495e")
        ]
        
        # Надписи на секторах
        sectors = ["100", "200", "300", "500", "1000", "БАНКРОТ", "ПРИЗ", "ПРОПУСК"]
        angle_per_sector = 360 / len(sectors)
        
        # Рисуем сектора
        for i in range(len(sectors)):
            painter.setBrush(colors[i % len(colors)])
            painter.setPen(Qt.black)
            painter.drawPie(0, 0, 300, 300, i * angle_per_sector * 16, angle_per_sector * 16)
            
            # Рисуем текст
            painter.setPen(Qt.white)
            font = QFont("Arial", 10, QFont.Bold)
            painter.setFont(font)
            painter.drawText(100, 100, 100, 100, Qt.AlignCenter, sectors[i])
        
        painter.end()
        return pixmap
    
    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.difficulty_label.setText(f"Уровень сложности: {difficulty}")
        self.total_score = 0
        self.update_score()
        
        # Выбираем случайное слово
        self.hidden_word = random.choice(self.words[difficulty])
        self.guessed_word = ["_" for _ in self.hidden_word]
        
        # Очищаем предыдущие буквы
        for i in reversed(range(self.word_grid.count())): 
            self.word_grid.itemAt(i).widget().setParent(None)
        self.word_boxes = []
        
        # Создаем новые поля для букв
        for i, char in enumerate(self.guessed_word):
            letter_box = QLabel(char)
            letter_box.setAlignment(Qt.AlignCenter)
            letter_box.setStyleSheet("""
                font-size: 24px; 
                font-weight: bold; 
                border: 2px solid #ecf0f1; 
                min-width: 40px; 
                min-height: 40px; 
                background-color: rgba(44, 62, 80, 150);
                color: #f1c40f;
                margin: 5px;
                padding: 5px;
            """)
            self.word_boxes.append(letter_box)
            self.word_grid.addWidget(letter_box, 0, i)
        
        self.stacked_widget.setCurrentIndex(1)
    
    def start_wheel_spin(self):
        self.spin_angle = 0
        self.spin_button.setEnabled(False)
        self.letter_input.setEnabled(False)
        self.spin_timer.start(50)
    
    def update_wheel_rotation(self):
        self.spin_angle += 30
        transform = QTransform().rotate(self.spin_angle)
        rotated_pixmap = self.wheel_pixmap.transformed(transform, Qt.SmoothTransformation)
        self.wheel_label.setPixmap(rotated_pixmap)
        
        if self.spin_angle >= 360 * random.randint(2, 4):
            self.spin_timer.stop()
            self.spin_button.setEnabled(True)
            self.letter_input.setEnabled(True)
            self.finalize_spin()
    
    def finalize_spin(self):
        result = random.choice(self.sectors[self.difficulty])
        
        if result == "БАНКРОТ":
            self.total_score = 0
            QMessageBox.information(self, "Результат", "Банкрот! Вы потеряли все очки!")
        elif result == "ПРОПУСК ХОДА":
            QMessageBox.information(self, "Результат", "Пропуск хода!")
        elif result == "ПРИЗ":
            prize = random.randint(100, 500)
            self.total_score += prize
            QMessageBox.information(self, "Результат", f"Вы выиграли приз: +{prize} очков!")
        else:
            points = int(result.strip("+"))
            self.total_score += points
            QMessageBox.information(self, "Результат", f"Вы выиграли: {result} очков!")
        
        self.update_score()
    
    def update_score(self):
        self.score_label.setText(f"Очки: {self.total_score}")
    
    def input_letter(self):
        letter, ok = QInputDialog.getText(
            self, 
            "Ввод буквы", 
            "Введите букву:", 
            maxLength=1
        )
        
        if ok and letter:
            letter = letter.upper()
            if letter in self.hidden_word:
                for i, char in enumerate(self.hidden_word):
                    if char == letter:
                        self.guessed_word[i] = letter
                        self.word_boxes[i].setText(letter)
                
                if "_" not in self.guessed_word:
                    QMessageBox.information(
                        self, 
                        "Победа!", 
                        f"Поздравляем! Вы угадали слово: {self.hidden_word}\n"
                        f"Ваш итоговый счет: {self.total_score}"
                    )
                    self.stacked_widget.setCurrentIndex(0)
            else:
                QMessageBox.information(self, "Неудача", "Такой буквы нет в слове")

if __name__ == "__main__":
    app = QApplication([])
    window = PoleChudesGame()
    window.show()
    app.exec_()
