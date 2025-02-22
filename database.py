import sqlite3
from main_classes import BmiCalculator, CaloricDemandCalculator
import csv

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("kcalkulator.db")
        self.cursor = self.conn.cursor()

    def save_profile(self, profile):
        self.cursor.execute("""
        INSERT INTO profiles (nickname, age, weight, height, gender, intention, training_activity, nontraining_activity, hip, waist, neck)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, profile)
        self.conn.commit()

    def load_profiles(self, combobox):
        # Loads profiles from the database
        self.cursor.execute("SELECT nickname FROM profiles")
        profiles = self.cursor.fetchall()
        combobox.clear()
        for profile in profiles:
            combobox.addItem(profile[0])

    def get_profile_name(self, id):
        self.cursor.execute("SELECT nickname FROM profiles WHERE id = ?", (id,))
        result = self.cursor.fetchone()
        return result[0]

    def profile_exists(self, id):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM profiles WHERE id = ?)", (id,))
        return self.cursor.fetchone()[0]

    def get_profile_data(self, nickname):
        # Fetches all profile data from the database based on the nickname
        self.cursor.execute("""
            SELECT nickname, age, weight, height, gender, intention, 
                   training_activity, nontraining_activity, hip, waist, neck
            FROM profiles 
            WHERE nickname = ?
        """, (nickname,))
        result = self.cursor.fetchone()

        if result:
            # Create dictionary with all fields including nickname
            keys = ["nickname", "age", "weight", "height", "gender", "intention",
                   "training_activity", "nontraining_activity", "hip", "waist", "neck"]
            return dict(zip(keys, result))

        return None

    def get_profile_id(self, nickname):
        self.cursor.execute("SELECT id FROM profiles WHERE nickname = ?", (nickname,))
        result = self.cursor.fetchone()

        if result:
            return result[0]

    def get_profile_bmi(self, profile_id):
        # Fetches a list of BMI values and corresponding dates for the given profile from the database.
        try:
            self.cursor.execute("""
               SELECT bmi_history.date_weight, bmi_history.weight, profiles.height 
               FROM bmi_history
               JOIN profiles ON bmi_history.profile_id = profiles.id
               WHERE bmi_history.profile_id = ?
               ORDER BY bmi_history.date_weight ASC
            """, (profile_id,))
            records = self.cursor.fetchall()

            if not records:
                print(f"No BMI data found for profile ID: {profile_id}")
                return [], []

            dates = []
            bmi_list = []
            for date_weight, weight, height in records:
                if weight and height:
                    bmi_calculator = BmiCalculator(weight, height)
                    dates.append(date_weight)
                    bmi_list.append(bmi_calculator.calculate_bmi())

            return dates, bmi_list

        except Exception as e:
            print(f"Błąd podczas pobierania danych BMI: {e}")
            return [], []

    def get_weight_measurements(self, profile_id):
        self.cursor.execute("""
            SELECT weight, date_weight 
            FROM bmi_history 
            WHERE profile_id = ?
            ORDER BY date_weight ASC
        """, (profile_id,))

        # Retrieve all results
        records = self.cursor.fetchall()

        # Check if there is any data
        if not records:
            print(f"No weight data found for profile_id: {profile_id}")
            return [], []

        # Unpack results into the dates and weights lists
        dates, weights = zip(*records)
        return list(dates), list(weights)


    def get_caloric_demand_history(self, profile_id):
        # Fetches the caloric baseline history based on weight for the user's profile
        try:
            self.cursor.execute("""
                    SELECT weight, caloric_demand 
                    FROM bmi_history 
                    WHERE profile_id = ?
                    ORDER BY date_weight ASC
                """, (profile_id,))
            records = self.cursor.fetchall()

            if not records:
                return [], []

            weights = []
            caloric_demands = []
            for weight, calorie_zero in records:
                if weight and calorie_zero:
                    weights.append(weight)
                    caloric_demands.append(calorie_zero)

            return weights, caloric_demands
        except Exception as e:
            print(f"Błąd podczas pobierania historii zera kalorycznego: {e}")
            return [], []

    def save_profiles_from_file(self, file_path):
        # Loads profiles from a text or CSV file and saves them to the database.
        # Added the ability to import initial BMI history for a profile.
        errors = []
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    try:
                        # Load the basic profile
                        profile = (
                            row["nickname"],
                            int(row["age"]),
                            float(row["weight"]),
                            float(row["height"]),
                            row["gender"],
                            row["intention"],
                            row["training_activity"],
                            row["nontraining_activity"],
                            float(row["hip"]),
                            float(row["waist"]),
                            float(row["neck"])
                        )

                        # Save profile data in the "profiles" table
                        self.cursor.execute("""
                            INSERT INTO profiles (nickname, age, weight, height, gender, intention, training_activity, 
                                                  nontraining_activity, hip, waist, neck)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, profile)

                        # Retrieve the ID of the new profile record (profile_id)
                        profile_id = self.cursor.lastrowid

                        # Check if there is BMI history in the file
                        if "date_weight" in row and "weight_history" in row:
                            weights = row["weight_history"].split(";")
                            dates = row["date_weight"].split(";")

                            # Add data to the "bmi_history" table
                            for date, weight in zip(dates, weights):
                                weight = float(weight)
                                bmi_calculator = BmiCalculator(weight, profile[3])  # height
                                bmi = bmi_calculator.calculate_bmi()

                                caloric_demand = CaloricDemandCalculator.calculate_static_zero_caloric(
                                    weight=weight,
                                    height=profile[3],
                                    age=profile[1],
                                    gender=profile[4],
                                    training_activity=profile[6],
                                    nontraining_activity=profile[7]
                                )

                                # Save BMI data
                                self.cursor.execute("""
                                    INSERT INTO bmi_history (profile_id, weight, date_weight, bmi, caloric_demand)
                                    VALUES (?, ?, ?, ?, ?)
                                """, (profile_id, weight, date, bmi, caloric_demand))

                    except (ValueError, KeyError) as e:
                        # Error handling: invalid data in the file
                        errors.append(f"Niepoprawne dane: {row}, Błąd: {e}")

                self.conn.commit()

        except Exception as e:
            errors.append(f"Nie udało się odczytać pliku: {e}")

        return errors

    def delete_profile(self, profile_id, refresh_callback=None):
        #Removes the profile from the database along with related data in the bmi_history table based on the user ID.
        try:
            self.cursor.execute("DELETE FROM bmi_history WHERE profile_id = ?", (profile_id,))
            self.cursor.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
            self.conn.commit()
            if refresh_callback:
                refresh_callback()

        except Exception as e:
            print(f"Błąd podczas usuwania profilu: {e}")