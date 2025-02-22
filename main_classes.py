from sklearn.linear_model import LinearRegression
import numpy as np

class BmiCalculator:
    def __init__(self, weight, height):
        self.weight = weight
        self.height = height / 100

    def calculate_bmi(self):
        bmi = self.weight / self.height ** 2
        return round(bmi, 2)

    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class CaloricDemandCalculator:
    def __init__(self, weight_data, caloric_demand_data):
        # Initialization of the caloric maintenance calculator.
        self.weight_data = np.array(weight_data).reshape(-1, 1)
        self.caloric_demand_data = np.array(caloric_demand_data)

    def fit_model(self):
        # Fitting the linear regression model
        self.model = LinearRegression()
        self.model.fit(self.weight_data, self.caloric_demand_data)

    def predict(self, new_weight):
        # Estimates caloric maintenance based on the new weight
        if not hasattr(self, 'model'):
            self.fit_model()
        return round(self.model.predict(np.array([[new_weight]]))[0], 2)

    @staticmethod
    def calculate_static_zero_caloric(weight, height, age, gender,  training_activity, nontraining_activity):
        # Static method to calculate caloric maintenance for given parameters
        if gender == 'M':  # Male
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:  # Female
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # Physical activity level
        training_activities = {
            "Brak treningów": 1.2,
            "Brak / jeden lekki trening": 1.3,
            "Pojedyncze lekkie treningi": 1.4,
            "Pojedyncze treningi": 1.5,
            "Kilka treningów (2-4x)": 1.6,
            "Częste treningi(3-5x)": 1.7,
            "Częste treningi(4-6x)": 1.8,
            "Częste ciężkie treningi": 1.9,
            "Codzienne treningi": 2,
            "Codzienne ciężkie treningi": 2.2
        }

        nontraining_activities = {
            "Brak aktywności, osoba leżąca": 1.2,
            "Bardzo niska aktywność, codzienne obowiązki": 1.3,
            "Niska aktywność / praca biurowa": 1.4,
            "Umiarkowana aktywność / praca mieszana": 1.5,
            "Średnia aktywność / praca mieszana": 1.6,
            "Średnia aktywność / lekka praca fizyczna": 1.7,
            "Wysoka aktywność / praca fizyczna": 1.8,
            "Wysoka aktywność / ciężka praca fizyczna": 1.9,
            "Wysoka aktywność": 2,
            "Bardzo wysoka aktywność": 2.2
        }

        # Calculation of the average multiplier from training and non-training activities
        training_multiplier = training_activities.get(training_activity, 1.2)
        nontraining_multiplier = nontraining_activities.get(nontraining_activity, 1.2)

        multiplier = (training_multiplier + nontraining_multiplier) / 2
        caloric_demand = bmr * multiplier
        return round(caloric_demand, 2)

class CaloricDemandAdjuster(CaloricDemandCalculator):
    def __init__(self, weight_data, caloric_demand_data, surplus=300, deficit=500):
        # Initialization of a class calculating the calories needed for weight gain or weight loss
        super().__init__(weight_data, caloric_demand_data)
        self.surplus = surplus
        self.deficit = deficit

    # Property calculating the calories required for weight gain
    @property
    def calories_to_gain(self):
        if not hasattr(self, 'model'):
            self.fit_model()
        return self.predict(self.weight_data[-1][0]) + self.surplus

    # Property calculating the calories required for weight loss
    @property
    def calories_to_lose(self):
        if not hasattr(self, 'model'):
            self.fit_model()
        return self.predict(self.weight_data[-1][0]) - self.deficit
