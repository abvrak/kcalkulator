import sys, csv
from database import Database
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QFrame,
    QLineEdit,
    QDialog,
    QFileDialog
)
from functools import partial
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from main_classes import BmiCalculator, CaloricDemandCalculator, CaloricDemandAdjuster

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("kcalkulator")
        self.resize(1205, 800)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.database = Database()

        self.mainmenu()
        self.profile_managament()
        self.profile_summary()
        self.profile_creator()
    def mainmenu(self):
        # Create central widget
        mainmenu_widget = QWidget()
        layout = QVBoxLayout()
        mainmenu_widget.setLayout(layout)

        self.stacked_widget.addWidget(mainmenu_widget)

        # Main label
        self.main_label = QLabel(mainmenu_widget)
        self.main_label.setGeometry(QRect(0, 30, 1201, 381))
        font_main_label = QFont()
        font_main_label.setFamily("Century Gothic")
        font_main_label.setPointSize(24)
        font_main_label.setBold(True)
        self.main_label.setFont(font_main_label)
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_label.setText("Witaj w aplikacji kcalkulator!")

        # ComboBox for select a profile
        self.choose_profile_combobox = QComboBox(mainmenu_widget)
        self.choose_profile_combobox.setGeometry(QRect(470, 430, 221, 31))
        font_profile_combo_box = QFont()
        font_profile_combo_box.setFamily("Century Gothic")
        font_profile_combo_box.setPointSize(9)
        self.choose_profile_combobox.setFont(font_profile_combo_box)
        self.choose_profile_combobox.setPlaceholderText("Wybierz profil")
        self.database.load_profiles(self.choose_profile_combobox)
        # Load profiles into the ComboBox
        self.choose_profile_combobox.currentIndexChanged.connect(self.load_selected_profile)


        # Label to select a profile
        self.choose_profile_label = QLabel(mainmenu_widget)
        self.choose_profile_label.setGeometry(QRect(470, 340, 221, 71))
        font_profile_label = QFont()
        font_profile_label.setFamily("Century Gothic")
        font_profile_label.setPointSize(9)
        self.choose_profile_label.setFont(font_profile_label)
        self.choose_profile_label.setAutoFillBackground(True)
        self.choose_profile_label.setFrameShape(QFrame.Shape.Box)
        self.choose_profile_label.setFrameShadow(QFrame.Shadow.Plain)
        self.choose_profile_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.choose_profile_label.setText("Wybierz profil")

        # Button to manage profiles
        self.profile_managament_button = QPushButton(mainmenu_widget)
        self.profile_managament_button.setGeometry(QRect(470, 710, 221, 31))
        font_profile_manag_button = QFont()
        font_profile_manag_button.setFamily("Century Gothic")
        font_profile_manag_button.setPointSize(9)
        self.profile_managament_button.setFont(font_profile_manag_button)
        self.profile_managament_button.setText("Zarządzanie profilami")
        # Add functionality for the profile management button
        self.profile_managament_button.clicked.connect(self.show_profile_management)

        # Button to navigate to the profile summary window
        self.next_button = QPushButton(mainmenu_widget)
        self.next_button.setGeometry(QRect(520, 470, 121, 31))
        font_next_button = QFont()
        font_next_button.setFamily("Century Gothic")
        font_next_button.setPointSize(9)
        self.next_button.setFont(font_next_button)
        self.next_button.setText("Dalej")
        self.next_button.clicked.connect(self.show_profile_summary)


    def profile_managament(self):
        self.profile_management_widget = QWidget()
        layout = QVBoxLayout()
        self.profile_management_widget.setLayout(layout)

        self.stacked_widget.addWidget(self.profile_management_widget)

        # Title for the profile management section
        self.profile_management_title = QLabel(self.profile_management_widget)
        self.profile_management_title.setGeometry(QRect(0, 0, 1201, 131))
        font_title = QFont()
        font_title.setFamily("Century Gothic")
        font_title.setPointSize(32)
        self.profile_management_title.setFont(font_title)
        self.profile_management_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_management_title.setText("Zarządzanie profilami")

        # Fetch profiles from the database
        self.cursor = self.database.conn.cursor()
        self.cursor.execute("SELECT id, nickname FROM profiles")
        profiles = self.cursor.fetchall()

        # Styling profile labels
        font_profile_label = QFont()
        font_profile_label.setPointSize(10)

        # Positions for labels and buttons, in rows (2x3)
        positions = [
            (240, 220),  # Slot 1
            (500, 220),  # Slot 2
            (760, 220),  # Slot 3
            (240, 460),  # Slot 4
            (500, 460),  # Slot 5
            (760, 460),  # Slot 6
        ]

        # Slot creation
        for i in range(6):
            profile_slot = QLabel(self.profile_management_widget)
            x, y = positions[i]
            profile_slot.setGeometry(QRect(x, y, 201, 121))
            profile_slot.setFont(font_profile_label)
            profile_slot.setAutoFillBackground(True)
            profile_slot.setFrameShape(QFrame.Shape.Box)
            profile_slot.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if i < len(profiles):
                profile_id, profile_nickname = profiles[i]
                profile_slot.setText(profile_nickname)

                delete_button = QPushButton(self.profile_management_widget)
                delete_button.setGeometry(QRect(x + 70, y + 130, 81, 24))  # Pozycja dla "Usuń"
                delete_button.setText("Usuń")
                delete_button.clicked.connect(partial(self.database.delete_profile, profile_id, self.refresh_profiles))

                # "Add" and "Import" buttons are hidden for existing slots
                add_button = QPushButton(self.profile_management_widget)
                add_button.setGeometry(QRect(x, y + 130, 81, 24))
                add_button.hide()

                import_button = QPushButton(self.profile_management_widget)
                import_button.setGeometry(QRect(x + 120, y + 130, 81, 24))
                import_button.hide()

            else:
                # If the slot is empty, display information about free space with "Add" and "Import" buttons
                profile_slot.setText("Wolne miejsce na profil")

                add_button = QPushButton(self.profile_management_widget)
                add_button.setGeometry(QRect(x, y + 130, 81, 24))
                add_button.setText("Dodaj")
                add_button.clicked.connect(self.show_profile_creator)

                import_button = QPushButton(self.profile_management_widget)
                import_button.setGeometry(QRect(x + 120, y + 130, 81, 24))
                import_button.setText("Importuj")
                import_button.clicked.connect(self.open_file_dialog)

        # Return button to the main menu
        self.goback_button_2 = QPushButton(self.profile_management_widget)
        self.goback_button_2.setGeometry(QRect(10, 10, 81, 41))
        font = QFont()
        font.setFamily("Century Gothic")
        self.goback_button_2.setFont(font)
        self.goback_button_2.setText("Powrót")
        self.goback_button_2.clicked.connect(self.show_mainmenu)

    def open_file_dialog(self):
        # Open the dialog to select a CSV or TXT file
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Wybierz plik do importu")
        dialog.setNameFilters(["Pliki CSV (*.csv)", "Pliki TXT (*.txt)", "Wszystkie pliki (*.*)"])

        # Open the dialog and check if the user selected a file
        if dialog.exec():
            file_path = dialog.selectedFiles()[0]
            self.import_file(file_path)

    def import_file(self, file_path):
        try:
            errors = self.database.save_profiles_from_file(file_path)
            if errors:
                print("Wystąpiły błędy podczas importu pliku:")
                for e in errors:
                    print(e)
            else:
                self.refresh_profiles()
                print("Pomyślnie zaimportowano dane profili.")
        except Exception as e:
            print(f"Błąd podczas importu danych: {e}")

    def refresh_profiles(self):
        self.database.load_profiles(self.choose_profile_combobox)
        self.profile_managament()

        # Handle the situation when there are no profiles
        if self.choose_profile_combobox.count() > 0:
            self.choose_profile_combobox.setCurrentIndex(0)
            self.load_selected_profile()
        else:
            self.choose_profile_combobox.setPlaceholderText("Brak dostępnych profili")
            self.show_mainmenu()

    def profile_summary(self):
        self.profile_summary_widget = QWidget()
        layout = QVBoxLayout()
        self.profile_summary_widget.setLayout(layout)
        self.stacked_widget.addWidget(self.profile_summary_widget)

        # Label displaying profile nickname
        self.nickname_label = QLabel(self.profile_summary_widget)
        self.nickname_label.setGeometry(QRect(0, 0, 1201, 131))
        self.nickname_label.setText("Nickname")
        font_nickname_label = QFont()
        font_nickname_label.setFamily("Century Gothic")
        font_nickname_label.setPointSize(32)
        self.nickname_label.setFont(font_nickname_label)
        self.nickname_label.setAutoFillBackground(True)
        self.nickname_label.setFrameShape(QFrame.Shape.NoFrame)
        self.nickname_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nickname_label.setObjectName("nickname_label")

        # Font
        font = QFont()
        font_nickname_label.setFamily("Century Gothic")
        font_nickname_label.setPointSize(9)


        # Label displaying age
        self.age_label = QLabel(self.profile_summary_widget)
        self.age_label.setText("Wiek")
        self.age_label.setGeometry(QRect(370, 140, 71, 31))
        self.age_label.setFont(font)
        self.age_label.setAutoFillBackground(True)
        self.age_label.setFrameShape(QFrame.Shape.Box)
        self.age_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.age_label.setObjectName("age_label")

        # Label displaying height
        self.height_label = QLabel(self.profile_summary_widget)
        self.height_label.setText("Wzrost")
        self.height_label.setGeometry(QRect(590, 140, 71, 31))
        self.height_label.setFont(font)
        self.height_label.setAutoFillBackground(True)
        self.height_label.setFrameShape(QFrame.Shape.Box)
        self.height_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.height_label.setObjectName("height_label")

        # Label displaying weight
        self.weight_label = QLabel(self.profile_summary_widget)
        self.weight_label.setText("Waga")
        self.weight_label.setGeometry(QRect(480, 140, 81, 31))
        self.weight_label.setFont(font)
        self.weight_label.setAutoFillBackground(True)
        self.weight_label.setFrameShape(QFrame.Shape.Box)
        self.weight_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.weight_label.setObjectName("weight_label")

        # Label displaying gender
        self.gender_label = QLabel(self.profile_summary_widget)
        self.gender_label.setText("Płeć")
        self.gender_label.setGeometry(QRect(260, 140, 71, 31))
        self.gender_label.setFont(font)
        self.gender_label.setAutoFillBackground(True)
        self.gender_label.setFrameShape(QFrame.Shape.Box)
        self.gender_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gender_label.setObjectName("gender_label")

        # Label displaying training activity
        self.training_activity_label = QLabel(self.profile_summary_widget)
        self.training_activity_label.setText("Aktywność treningowa")
        self.training_activity_label.setGeometry(QRect(480, 230, 181, 31))
        self.training_activity_label.setFont(font)
        self.training_activity_label.setAutoFillBackground(True)
        self.training_activity_label.setFrameShape(QFrame.Shape.Box)
        self.training_activity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.training_activity_label.setObjectName("training_activity_label")

        # Label displaying non-training activity
        self.nontraining_activity_label = QLabel(self.profile_summary_widget)
        self.nontraining_activity_label.setText("Aktywność poza treningowa")
        self.nontraining_activity_label.setGeometry(QRect(260, 230, 181, 31))
        self.nontraining_activity_label.setFont(font)
        self.nontraining_activity_label.setAutoFillBackground(True)
        self.nontraining_activity_label.setFrameShape(QFrame.Shape.Box)
        self.nontraining_activity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nontraining_activity_label.setObjectName("nontraining_activity_label")

        # Label displaying BMI
        self.bmi_label = QLabel(self.profile_summary_widget)
        self.bmi_label.setText("BMI")
        self.bmi_label.setGeometry(QRect(220, 710, 141, 31))
        self.bmi_label.setFont(font)
        self.bmi_label.setAutoFillBackground(True)
        self.bmi_label.setFrameShape(QFrame.Shape.Box)
        self.bmi_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bmi_label.setObjectName("bmi_label")

        # Label for body weight chart section
        self.lean_bodymass_label = QLabel(self.profile_summary_widget)
        self.lean_bodymass_label.setText("Waga ciała")
        self.lean_bodymass_label.setGeometry(QRect(840, 710, 181, 31))
        self.lean_bodymass_label.setFont(font)
        self.lean_bodymass_label.setAutoFillBackground(True)
        self.lean_bodymass_label.setFrameShape(QFrame.Shape.Box)
        self.lean_bodymass_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lean_bodymass_label.setObjectName("lean_bodymass_label")

        # Label for caloric demand
        self.caloric_demand_label = QLabel(self.profile_summary_widget)
        self.caloric_demand_label.setText("Zero kaloryczne")
        self.caloric_demand_label.setGeometry(QRect(530, 320, 141, 31))
        self.caloric_demand_label.setFont(font)
        self.caloric_demand_label.setAutoFillBackground(True)
        self.caloric_demand_label.setFrameShape(QFrame.Shape.Box)
        self.caloric_demand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.caloric_demand_label.setObjectName("caloric_demand_label")

        # Upper dividing graphic line
        self.line_1 = QFrame(self.profile_summary_widget)
        self.line_1.setGeometry(QRect(0, 300, 1201, 20))
        self.line_1.setFrameShape(QFrame.Shape.HLine)
        self.line_1.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_1.setObjectName("line_1")

        # Bottom dividing graphic line
        self.line_2 = QFrame(self.profile_summary_widget)
        self.line_2.setGeometry(QRect(0, 680, 1201, 20))
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")

        # Neck label
        self.neck_label = QLabel(self.profile_summary_widget)
        self.neck_label.setText("Obwód szyi")
        self.neck_label.setGeometry(QRect(840, 140, 111, 31))
        self.neck_label.setFont(font)
        self.neck_label.setAutoFillBackground(True)
        self.neck_label.setFrameShape(QFrame.Shape.Box)
        self.neck_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.neck_label.setObjectName("neck_label")

        # Label displaying waist circumference
        self.waist_label = QLabel(self.profile_summary_widget)
        self.waist_label.setText("Obwód talii")
        self.waist_label.setGeometry(QRect(840, 230, 111, 31))
        self.waist_label.setFont(font)
        self.waist_label.setAutoFillBackground(True)
        self.waist_label.setFrameShape(QFrame.Shape.Box)
        self.waist_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.waist_label.setObjectName("waist_label")

        # Label displaying hip circumference
        self.hip_label = QLabel(self.profile_summary_widget)
        self.hip_label.setText("Obwód bioder")
        self.hip_label.setGeometry(QRect(700, 230, 121, 31))
        self.hip_label.setFont(font)
        self.hip_label.setAutoFillBackground(True)
        self.hip_label.setFrameShape(QFrame.Shape.Box)
        self.hip_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.hip_label.setObjectName("hip_label")

        # Label displaying user goal
        self.intention_label = QLabel(self.profile_summary_widget)
        self.intention_label.setText("Cel")
        self.intention_label.setGeometry(QRect(700, 140, 121, 31))
        self.intention_label.setFont(font)
        self.intention_label.setAutoFillBackground(True)
        self.intention_label.setFrameShape(QFrame.Shape.Box)
        self.intention_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.intention_label.setObjectName("intention_label")

        self.label_kcal_surplus = QLabel(self.profile_summary_widget)
        self.label_kcal_surplus.setText("Nadwyżka")
        self.label_kcal_surplus.setGeometry(QRect(840, 420, 161, 61))
        self.label_kcal_surplus.setAutoFillBackground(True)
        self.label_kcal_surplus.setFrameShape(QFrame.Shape.Box)
        self.label_kcal_surplus.setObjectName("label")
        self.label_kcal_surplus.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_kcal_deficit = QLabel(self.profile_summary_widget)
        self.label_kcal_deficit.setText("Deficyt")
        self.label_kcal_deficit.setGeometry(QRect(840, 550, 161, 61))
        self.label_kcal_deficit.setAutoFillBackground(True)
        self.label_kcal_deficit.setFrameShape(QFrame.Shape.Box)
        self.label_kcal_deficit.setObjectName("label_2")
        self.label_kcal_deficit.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # Hip result field
        self.hip_result = QLabel(self.profile_summary_widget)
        self.hip_result.setGeometry(QRect(700, 260, 121, 31))
        self.hip_result.setFont(font)
        self.hip_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hip_result.setObjectName("hip_result")

        # Waist result field
        self.waist_result = QLabel(self.profile_summary_widget)
        self.waist_result.setGeometry(QRect(840, 260, 101, 31))
        self.waist_result.setFont(font)
        self.waist_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.waist_result.setObjectName("waist_result")

        # Training activity result field
        self.training_activity_result = QLabel(self.profile_summary_widget)
        self.training_activity_result.setGeometry(QRect(480, 260, 181, 31))
        self.training_activity_result.setFont(font)
        self.training_activity_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.training_activity_result.setObjectName("training_activity_result")

        # Non training activity result field
        self.nontraining_activity_result = QLabel(self.profile_summary_widget)
        self.nontraining_activity_result.setGeometry(QRect(260, 260, 181, 31))
        self.nontraining_activity_result.setFont(font)
        self.nontraining_activity_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nontraining_activity_result.setObjectName("nontraining_activity_result")

        # Gender result field
        self.gender_result = QLabel(self.profile_summary_widget)
        self.gender_result.setGeometry(QRect(260, 170, 71, 31))
        self.gender_result.setFont(font)
        self.gender_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gender_result.setObjectName("gender_result")

        # Age result field
        self.age_result = QLabel(self.profile_summary_widget)
        self.age_result.setGeometry(QRect(370, 170, 71, 31))
        self.age_result.setFont(font)
        self.age_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.age_result.setObjectName("age_result")

        # Weight result field
        self.weight_result = QLabel(self.profile_summary_widget)
        self.weight_result.setGeometry(QRect(480, 170, 71, 31))
        self.weight_result.setFont(font)
        self.weight_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weight_result.setObjectName("weight_result")

        # Height result field
        self.height_result = QLabel(self.profile_summary_widget)
        self.height_result.setGeometry(QRect(590, 170, 71, 31))
        self.height_result.setFont(font)
        self.height_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.height_result.setObjectName("height_result")

        # Intention result field
        self.intention_result = QLabel(self.profile_summary_widget)
        self.intention_result.setGeometry(QRect(700, 170, 121, 31))
        self.intention_result.setFont(font)
        self.intention_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.intention_result.setObjectName("intention_result")

        # Neck result field
        self.neck_result = QLabel(self.profile_summary_widget)
        self.neck_result.setGeometry(QRect(840, 170, 101, 31))
        self.neck_result.setFont(font)
        self.neck_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.neck_result.setObjectName("neck_result")

        # Button to export the current profile
        self.edit_profile_button = QPushButton(self.profile_summary_widget)
        self.edit_profile_button.setText("Eksportuj profil")
        self.edit_profile_button.setGeometry(QRect(1100, 10, 91, 41))
        self.edit_profile_button.setFont(font)
        self.edit_profile_button.setObjectName("edit_profile_button")
        self.edit_profile_button.clicked.connect(self.export_profile_data)

        # Font for push buttons
        font_button = QFont()
        font_button.setFamily("Century Gothic")
        font_button.setPointSize(16)
        font_button.setBold(False)

        # Button to add a new weight measurement
        self.pushButton = QPushButton(self.profile_summary_widget)
        self.pushButton.setText("+")
        self.pushButton.setGeometry(QRect(530, 140, 31, 31))
        self.pushButton.setFont(font_button)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.open_measurement_dialog)

        # Button to return to main menu
        self.goback_button = QPushButton(self.profile_summary_widget)
        self.goback_button.setText("Powrót")
        self.goback_button.setGeometry(QRect(10, 10, 81, 41))
        self.goback_button.setFont(font)
        self.goback_button.setObjectName("goback_button")
        self.goback_button.clicked.connect(self.show_mainmenu)

        # Container for weight history chart
        self.chart_frame = QFrame(self.profile_summary_widget)
        self.chart_frame.setGeometry(QRect(700, 750, 451, 261))

        # Initialize weight history chart
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.chart_frame.setLayout(layout)

        # Container for BMI chart
        self.bmi_chart_frame = QFrame(self.profile_summary_widget)
        self.bmi_chart_frame.setGeometry(QRect(60, 750, 451, 261))

        self.figure_bmi = Figure()
        self.canvas_bmi = FigureCanvas(self.figure_bmi)

        layout_bmi = QVBoxLayout()
        layout_bmi.addWidget(self.canvas_bmi)
        self.bmi_chart_frame.setLayout(layout_bmi)

        # Container for caloric demand history chart
        self.caloric_demand_chart_frame = QFrame(self.profile_summary_widget)
        self.caloric_demand_chart_frame.setGeometry(QRect(60, 380, 611, 261))

        self.figure_caloric_demand = Figure()
        self.canvas_caloric_demand = FigureCanvas(self.figure_caloric_demand)

        layout_caloric_demand = QVBoxLayout()
        layout_caloric_demand.addWidget(self.canvas_caloric_demand)
        self.caloric_demand_chart_frame.setLayout(layout_caloric_demand)

    def export_profile_data(self):
        try:
            # Retrieve the ID and nickname of the selected profile
            selected_nickname = self.nickname_label.text()
            if not selected_nickname:
                raise ValueError("Nie wybrano profilu do eksportu.")

            profile_id = self.database.get_profile_id(selected_nickname)

            # Retrieve profile data for export
            weights, caloric_demands = self.database.get_caloric_demand_history(profile_id)
            profile_data = self.database.get_profile_data(selected_nickname)

            if not profile_data or not weights or not caloric_demands:
                raise ValueError("Brak wystarczających danych do eksportu.")

            # Calculate the latest BMI and the last caloric zero
            latest_weight = weights[-1]
            latest_caloric_zero = caloric_demands[-1]
            bmi_calculator = BmiCalculator(latest_weight, profile_data['height'])
            latest_bmi = bmi_calculator.calculate_bmi()

            # Calculate the caloric surplus and deficit
            adjuster = CaloricDemandAdjuster(weights, caloric_demands)
            surplus_calories = adjuster.calories_to_gain
            deficit_calories = adjuster.calories_to_lose

            # Open the file save dialog
            dialog = QFileDialog(self)
            dialog.setWindowTitle("Eksportuj dane profilu")
            dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            dialog.setNameFilters(["Pliki tekstowe (*.txt)", "Pliki CSV (*.csv)"])

            if dialog.exec():
                file_path = dialog.selectedFiles()[0]
                if file_path.endswith(".txt"):
                    # Saving data to a text file
                    with open(file_path, mode="w", encoding="utf-8") as file:
                        file.write("Dane profilu\n")
                        file.write(f"Nazwa: {selected_nickname}\n")
                        file.write(f"Deficyt kaloryczny: {deficit_calories} kcal\n")
                        file.write(f"Nadwyżka kaloryczna: {surplus_calories} kcal\n")
                        file.write(f"Zero kaloryczne: {latest_caloric_zero} kcal\n")
                        file.write(f"BMI: {latest_bmi}\n")
                        file.write(f"Waga: {latest_weight} kg\n")
                elif file_path.endswith(".csv"):
                    # Saving data to a csv file
                    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            ["Nazwa", "Deficyt", "Nadwyżka", "Ostatnie zero kaloryczne", "Ostatni BMI", "Ostatnia waga"]
                        )
                        writer.writerow([
                            selected_nickname,
                            deficit_calories,
                            surplus_calories,
                            latest_caloric_zero,
                            latest_bmi,
                            latest_weight
                        ])
                else:
                    raise ValueError("Nieobsługiwany format pliku. Wybierz *.txt lub *.csv.")

        except ValueError as e:
            print(f"Błąd: {e}")
        except Exception as e:
            print(f"Nieoczekiwany błąd: {e}")

    def open_measurement_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dodaj pomiar")

        # Form fields
        weight_edit = QLineEdit()
        date_edit = QLineEdit()

        # Save button
        height_string = self.height_result.text()
        trimmed = height_string[:5]

        btn_save = QPushButton("Zapisz")
        btn_save.clicked.connect(lambda: self.save_measurement(
            weight_edit.text(),
            date_edit.text(),
            trimmed
        ))

        # Layout definition
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Waga (kg):"))
        layout.addWidget(weight_edit)
        layout.addWidget(QLabel("Data (RRRR-MM-DD):"))
        layout.addWidget(date_edit)
        layout.addWidget(btn_save)
        dialog.setLayout(layout)
        dialog.exec()

    def save_measurement(self, weight, date, height):
        try:
            # Validation of input data
            if not weight or not date or not height:
                raise ValueError("Wszystkie pola muszą być wypełnione.")

            weight = float(weight)
            height = float(height)

            # Date validation (format YYYY-MM-DD)
            import datetime
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Niepoprawny format daty. Podaj datę w formacie RRRR-MM-DD.")

            # BMI Calculation
            bmi_calculator = BmiCalculator(weight, height)
            bmi_rounded = bmi_calculator.calculate_bmi()

            # Retrieving user data for caloric zero calculation
            profile_id = self.database.get_profile_id(self.nickname_label.text())
            if not profile_id:
                raise ValueError("Nie można znaleźć ID aktualnego profilu.")

            profile_data = self.database.get_profile_data(self.nickname_label.text())
            age = profile_data['age']
            gender = profile_data['gender']
            activity_level = profile_data['training_activity']
            nontraining_activity_level = profile_data['nontraining_activity']

            # Caloric Zero Calculation
            caloric_demand = CaloricDemandCalculator.calculate_static_zero_caloric(
                weight=weight,
                height=height,
                age=age,
                gender=gender,
                training_activity=activity_level,
                nontraining_activity=nontraining_activity_level
            )

            # Saving to the database (weight, date, BMI, caloric zero)
            self.database.cursor.execute("""
                INSERT INTO bmi_history (profile_id, weight, date_weight, bmi, caloric_demand)
                VALUES (?, ?, ?, ?, ?)
            """, (profile_id, weight, date, bmi_rounded, caloric_demand))
            self.database.conn.commit()

            # Data refresh
            self.load_selected_profile()

        except ValueError as e:
            print(f"Błąd walidacji: {e}")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")

    def profile_creator(self):
        self.profile_creator_widget = QWidget()
        layout = QVBoxLayout()
        self.profile_creator_widget.setLayout(layout)

        self.stacked_widget.addWidget(self.profile_creator_widget)

        # Title
        self.create_profile_mainlabel = QLabel(self.profile_creator_widget)
        self.create_profile_mainlabel.setText("Tworzenie profilu")
        self.create_profile_mainlabel.setGeometry(QRect(0, 0, 1201, 131))
        font_mainlabel = QFont()
        font_mainlabel.setFamily("Century Gothic")
        font_mainlabel.setPointSize(32)
        self.create_profile_mainlabel.setFont(font_mainlabel)
        self.create_profile_mainlabel.setAutoFillBackground(True)
        self.create_profile_mainlabel.setFrameShape(QFrame.Shape.NoFrame)
        self.create_profile_mainlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_profile_mainlabel.setObjectName("create_profile_mainlabel")

        # Font
        font = QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)

        # Age label
        self.create_profile_age_label = QLabel(self.profile_creator_widget)
        self.create_profile_age_label.setText("Wiek")
        self.create_profile_age_label.setGeometry(QRect(460, 240, 71, 31))
        font = QFont()
        font.setFamily("Century Gothic")
        self.create_profile_age_label.setFont(font)
        self.create_profile_age_label.setAutoFillBackground(True)
        self.create_profile_age_label.setFrameShape(QFrame.Shape.Box)
        self.create_profile_age_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_profile_age_label.setObjectName("create_profile_age_label")

        # Hip label
        self.create_profile_hip_label = QLabel(self.profile_creator_widget)
        self.create_profile_hip_label.setText("Obwód bioder")
        self.create_profile_hip_label.setGeometry(QRect(430, 440, 101, 31))
        font = QFont()
        font.setFamily("Century Gothic")
        self.create_profile_hip_label.setFont(font)
        self.create_profile_hip_label.setAutoFillBackground(True)
        self.create_profile_hip_label.setFrameShape(QFrame.Shape.Box)
        self.create_profile_hip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_profile_hip_label.setObjectName("create_profile_hip_label")

        # Waist label
        self.create_profile_waist_label = QLabel(self.profile_creator_widget)
        self.create_profile_waist_label.setText("Obwód talii")
        self.create_profile_waist_label.setGeometry(QRect(430, 540, 101, 31))
        font = QFont()
        font.setFamily("Century Gothic")
        self.create_profile_waist_label.setFont(font)
        self.create_profile_waist_label.setAutoFillBackground(True)
        self.create_profile_waist_label.setFrameShape(QFrame.Shape.Box)
        self.create_profile_waist_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_profile_waist_label.setObjectName("create_profile_waist_label")

        # Gender label
        self.create_profile_gender_label = QLabel(self.profile_creator_widget)
        self.create_profile_gender_label.setText("Płeć")
        self.create_profile_gender_label.setGeometry(QRect(460, 190, 71, 31))
        font = QFont()
        font.setFamily("Century Gothic")
        self.create_profile_gender_label.setFont(font)
        self.create_profile_gender_label.setAutoFillBackground(True)
        self.create_profile_gender_label.setFrameShape(QFrame.Shape.Box)
        self.create_profile_gender_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_profile_gender_label.setObjectName("create_profile_gender_label")

        # Neck label
        self.create_profile_neck_label = QLabel(self.profile_creator_widget)
        self.create_profile_neck_label.setText("Obwód szyi")
        self.create_profile_neck_label.setGeometry(QRect(430, 490, 101, 31))
        font = QFont()
        font.setFamily("Century Gothic")
        self.create_profile_neck_label.setFont(font)
        self.create_profile_neck_label.setAutoFillBackground(True)
        self.create_profile_neck_label.setFrameShape(QFrame.Shape.Box)
        self.create_profile_neck_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_profile_neck_label.setObjectName("create_profile_neck_label")

        # Training activity label
        self.create_profile_training_activity_label = QLabel(self.profile_creator_widget)
        self.create_profile_training_activity_label.setText("Aktywność treningowa")
        self.create_profile_training_activity_label.setGeometry(QRect(350, 640, 181, 31))
        font = QFont()
        font.setFamily("Century Gothic")
        self.create_profile_training_activity_label.setFont(font)
        self.create_profile_training_activity_label.setAutoFillBackground(True)
        self.create_profile_training_activity_label.setFrameShape(QFrame.Shape.Box)
        self.create_profile_training_activity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_profile_training_activity_label.setObjectName("create_profile_training_activity_label")

        # Intention label
        self.create_profile_intention_label = QLabel(self.profile_creator_widget)
        self.create_profile_intention_label.setText("Cel")
        self.create_profile_intention_label.setGeometry(QRect(430, 390, 101, 31))
        font = QFont()
        font.setFamily("Century Gothic")
        self.create_profile_intention_label.setFont(font)
        self.create_profile_intention_label.setAutoFillBackground(True)
        self.create_profile_intention_label.setFrameShape(QFrame.Shape.Box)
        self.create_profile_intention_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_profile_intention_label.setObjectName("create_profile_intention_label")

        # Non training activity label
        self.create_profile_nontraining_activity_label = QLabel(self.profile_creator_widget)
        self.create_profile_nontraining_activity_label.setText("Aktywność poza treningowa")
        self.create_profile_nontraining_activity_label.setGeometry(QRect(350, 590, 181, 31))
        font = QFont()
        font.setFamily("Century Gothic")
        self.create_profile_nontraining_activity_label.setFont(font)
        self.create_profile_nontraining_activity_label.setAutoFillBackground(True)
        self.create_profile_nontraining_activity_label.setFrameShape(QFrame.Shape.Box)
        self.create_profile_nontraining_activity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_profile_nontraining_activity_label.setObjectName("create_profile_nontraining_activity_label")

        # Weight label
        self.create_profile_weight_label = QLabel(self.profile_creator_widget)
        self.create_profile_weight_label.setText("Waga")
        self.create_profile_weight_label.setGeometry(QRect(460, 290, 71, 31))
        font = QFont()
        font.setFamily("Century Gothic")
        self.create_profile_weight_label.setFont(font)
        self.create_profile_weight_label.setAutoFillBackground(True)
        self.create_profile_weight_label.setFrameShape(QFrame.Shape.Box)
        self.create_profile_weight_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_profile_weight_label.setObjectName("create_profile_weight_label")

        # Height label
        self.create_profile_height_label = QLabel(self.profile_creator_widget)
        self.create_profile_height_label.setText("Wzrost")
        self.create_profile_height_label.setGeometry(QRect(460, 340, 71, 31))
        font = QFont()
        font.setFamily("Century Gothic")
        self.create_profile_height_label.setFont(font)
        self.create_profile_height_label.setAutoFillBackground(True)
        self.create_profile_height_label.setFrameShape(QFrame.Shape.Box)
        self.create_profile_height_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_profile_height_label.setObjectName("create_profile_height_label")

        # Nickname label
        self.create_profile_nickname_label = QLabel(self.profile_creator_widget)
        self.create_profile_nickname_label.setText("Nazwa")
        self.create_profile_nickname_label.setGeometry(QRect(460, 140, 71, 31))
        font = QFont()
        font.setFamily("Century Gothic")
        self.create_profile_nickname_label.setFont(font)
        self.create_profile_nickname_label.setAutoFillBackground(True)
        self.create_profile_nickname_label.setFrameShape(QFrame.Shape.Box)
        self.create_profile_nickname_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.create_profile_nickname_label.setObjectName("create_profile_nickname_label")

        # Done button
        self.create_profile_done_button = QPushButton(self.profile_creator_widget)
        self.create_profile_done_button.setText("Gotowe")
        self.create_profile_done_button.setGeometry(QRect(500, 710, 161, 61))
        self.create_profile_done_button.setObjectName("create_profile_done_button")

        # Nickname line edit
        self.create_profile_nickname_lineEdit = QLineEdit(self.profile_creator_widget)
        self.create_profile_nickname_lineEdit.setGeometry(QRect(550, 140, 191, 31))
        self.create_profile_nickname_lineEdit.setObjectName("create_profile_nickname_lineEdit")

        # Age line edit
        self.create_profile_age_lineEdit = QLineEdit(self.profile_creator_widget)
        self.create_profile_age_lineEdit.setGeometry(QRect(550, 240, 191, 31))
        self.create_profile_age_lineEdit.setObjectName("create_profile_age_lineEdit")

        # Weight line edit
        self.create_profile_weight_lineEdit = QLineEdit(self.profile_creator_widget)
        self.create_profile_weight_lineEdit.setGeometry(QRect(550, 290, 191, 31))
        self.create_profile_weight_lineEdit.setObjectName("create_profile_weight_lineEdit")

        # Intention combo box
        self.create_profile_intention_comboBox = QComboBox(self.profile_creator_widget)
        self.create_profile_intention_comboBox.setGeometry(QRect(550, 390, 191, 31))
        self.create_profile_intention_comboBox.setObjectName("create_profile_intention_comboBox")

        # Height line edit
        self.create_profile_height_lineEdit = QLineEdit(self.profile_creator_widget)
        self.create_profile_height_lineEdit.setGeometry(QRect(550, 340, 191, 31))
        self.create_profile_height_lineEdit.setObjectName("create_profile_height_lineEdit")

        # Gender line edit
        self.create_profile_gender_lineEdit = QLineEdit(self.profile_creator_widget)
        self.create_profile_gender_lineEdit.setGeometry(QRect(550, 190, 191, 31))
        self.create_profile_gender_lineEdit.setObjectName("create_profile_gender_lineEdit")

        # Non training activity combo box
        self.create_profile_nontraining_activity_comboBox = QComboBox(self.profile_creator_widget)
        self.create_profile_nontraining_activity_comboBox.setGeometry(QRect(550, 590, 191, 31))
        self.create_profile_nontraining_activity_comboBox.setObjectName("create_profile_nontraining_activity_comboBox")

        # Training activity combo box
        self.create_profile_training_activity_comboBox = QComboBox(self.profile_creator_widget)
        self.create_profile_training_activity_comboBox.setGeometry(QRect(550, 640, 191, 31))
        self.create_profile_training_activity_comboBox.setObjectName("create_profile_training_activity_comboBox")

        # Hip line edit
        self.create_profile_hip_lineEdit = QLineEdit(self.profile_creator_widget)
        self.create_profile_hip_lineEdit.setGeometry(QRect(550, 440, 191, 31))
        self.create_profile_hip_lineEdit.setObjectName("create_profile_hip_lineEdit")

        # Neck line edit
        self.create_profile_neck_lineEdit = QLineEdit(self.profile_creator_widget)
        self.create_profile_neck_lineEdit.setGeometry(QRect(550, 490, 191, 31))
        self.create_profile_neck_lineEdit.setObjectName("create_profile_neck_lineEdit")

        # Waist line edit
        self.create_profile_waist_lineEdit = QLineEdit(self.profile_creator_widget)
        self.create_profile_waist_lineEdit.setGeometry(QRect(550, 540, 191, 31))
        self.create_profile_waist_lineEdit.setObjectName("create_profile_waist_lineEdit")

        # Go back button
        self.create_profile_goback_button = QPushButton(self.profile_creator_widget)
        self.create_profile_goback_button.setText("Powrót")

        self.create_profile_goback_button.setGeometry(QRect(10, 10, 81, 41))
        self.create_profile_goback_button.setFont(font)
        self.create_profile_goback_button.setObjectName("create_profile_goback_button")
        self.create_profile_goback_button.clicked.connect(self.show_profile_management)

    def load_selected_profile(self):
        # Check if the combobox has a selected profile
        selected_nickname = self.choose_profile_combobox.currentText()
        if not selected_nickname:
            print("Nie wybrano profilu.")
            return

        print("Selected Nickname: ", selected_nickname)

        # Retrieve data from database
        profile_data = self.database.get_profile_data(selected_nickname)
        if not profile_data:
            print(f"Nie znaleziono danych dla profilu: {selected_nickname}")
            return

        # Update the profile data view
        self.nickname_label.setText(profile_data['nickname'])
        self.age_result.setText(f"{profile_data['age']}")
        self.weight_result.setText(f"{profile_data['weight']} kg")
        self.height_result.setText(f"{profile_data['height']} cm")
        self.gender_result.setText(profile_data['gender'])
        self.intention_result.setText(profile_data['intention'])
        self.training_activity_result.setText(profile_data['training_activity'])
        self.nontraining_activity_result.setText(profile_data['nontraining_activity'])
        self.hip_result.setText(f"{profile_data['hip']} cm")
        self.waist_result.setText(f"{profile_data['waist']} cm")
        self.neck_result.setText(f"{profile_data['neck']} cm")

        # Retrieve profile ID
        profile_id = self.database.get_profile_id(selected_nickname)

        # Update charts
        self.draw_weight_chart(profile_id)
        self.draw_bmi_chart(profile_id)
        self.draw_caloric_demand_chart(profile_id)

        # Retrieve weight history and calorie zeros from the database
        weights, caloric_demands = self.database.get_caloric_demand_history(profile_id)

        if weights and caloric_demands:
            adjuster = CaloricDemandAdjuster(weights, caloric_demands)

            # Calculate calorie surplus and deficit
            surplus_calories = adjuster.calories_to_gain
            deficit_calories = adjuster.calories_to_lose

            # Display the results in the interface
            self.label_kcal_surplus.setText(f"Nadwyżka: {surplus_calories} kcal")
            self.label_kcal_deficit.setText(f"Deficyt: {deficit_calories} kcal")
        else:
            self.label_kcal_surplus.setText("Brak danych")
            self.label_kcal_deficit.setText("Brak danych")

    # Methods for drawing charts:
    def draw_weight_chart(self, profile_id):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Retrieve data from the database
        dates, weights = self.database.get_weight_measurements(profile_id)

        # Create weight history chart
        ax.plot(weights, dates, marker="o")
        ax.set_title("Historia wagi")
        ax.set_ylabel("Waga (kg)")
        ax.set_xlabel("Data")
        self.canvas.draw()

    def draw_bmi_chart(self, profile_id):
        self.figure_bmi.clear()
        ax_bmi = self.figure_bmi.add_subplot(111)

        # Retrieve BMI data from the database
        bmi_dates, bmi_values = self.database.get_profile_bmi(profile_id)

        # Create BMI chart
        ax_bmi.plot(bmi_dates, bmi_values, marker="o", label="BMI", color="red")
        ax_bmi.set_title("Historia BMI")
        ax_bmi.set_ylabel("BMI")
        ax_bmi.set_xlabel("Data")
        ax_bmi.legend(loc="upper left")
        self.canvas_bmi.draw()

    def draw_caloric_demand_chart(self, profile_id):
        self.figure_caloric_demand.clear()
        ax_caloric = self.figure_caloric_demand.add_subplot(111)

        # Retrieve calorie zero data from the database
        caloric_dates, caloric_values = self.database.get_caloric_demand_history(profile_id)
        print(caloric_dates, caloric_values)

        # Force point order using a category axis
        ax_caloric.plot(range(len(caloric_dates)), caloric_values, marker="o", label="Zero kaloryczne", color="blue")
        ax_caloric.set_title("Historia zera kalorycznego")
        ax_caloric.set_ylabel("Kalorie")
        ax_caloric.set_xlabel("Data")
        ax_caloric.legend(loc="upper right")

        # Set a custom X-axis as a category axis
        ax_caloric.set_xticks(range(len(caloric_dates)))
        ax_caloric.set_xticklabels(caloric_dates)

        self.canvas_caloric_demand.draw()

    def show_profile_creator(self):
        self.stacked_widget.setCurrentWidget(self.profile_creator_widget)

    def show_profile_summary(self):
        self.stacked_widget.setCurrentWidget(self.profile_summary_widget)

    def show_profile_management(self):
        self.stacked_widget.setCurrentWidget(self.profile_management_widget)

    def show_mainmenu(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.widget(0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
