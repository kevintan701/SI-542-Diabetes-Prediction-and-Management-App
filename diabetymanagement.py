# SI 542 Diabetes Management App
# Kevin Tan
# This script creates a simple diabetes management app using Tkinter with enhanced animations and emojis.


# Import necessary libraries
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkFont
from datetime import datetime
import random
import json
import numpy as np
import joblib
import time

# Load the trained diabetes risk model and scaler
xgb_model = joblib.load('diabetes_risk_model.pkl')
scaler = joblib.load('scaler.pkl')

class DiabetesManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diabetes Management App 😊")
        self.root.geometry("600x800")
        self.root.configure(bg="black")  # Black background for better contrast

        # Set a global style for fonts
        self.label_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.entry_font = tkFont.Font(family="Helvetica", size=16)
        self.header_font = tkFont.Font(family="Helvetica", size=22, weight="bold")
        self.button_font = tkFont.Font(family="Helvetica", size=18, weight="bold")
        self.tip_font = tkFont.Font(family="Helvetica", size=12, weight="bold", slant="italic")

        # User Information
        self.user_id = tk.StringVar()
        self.user_name = tk.StringVar()
        self.age = tk.StringVar()
        self.weight = tk.StringVar()
        self.height = tk.StringVar()
        self.activity_level = tk.StringVar()

        # Daily Data
        self.blood_glucose = tk.StringVar()
        self.diet = tk.StringVar()
        self.physical_activity = tk.StringVar()
        self.medication_adherence = tk.StringVar()
        self.stress_level = tk.StringVar()
        self.sleep_hours = tk.StringVar()
        self.hydration_level = tk.StringVar()

        # Add animation colors
        self.colors = ["#1abc9c", "#2ecc71", "#3498db", "#9b59b6", "#f1c40f"]
        self.current_color_index = 0
        
        # Start color animation
        self.animate_colors()

        self.create_user_interface()

    def animate_colors(self):
        """Animates the background color of buttons"""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg=self.colors[self.current_color_index])
        
        self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        self.root.after(1000, self.animate_colors)

    def create_user_interface(self):
        """Creates the user interface with improved animations and emojis"""
        # Animated welcome message
        welcome_text = "🌟 Welcome to Diabetes Management App 🌟"
        self.welcome_label = tk.Label(self.root, text="", font=self.header_font, bg="black", fg="white")
        self.welcome_label.pack(pady=20)
        self.animate_text(welcome_text, self.welcome_label)

        # Header Label
        tk.Label(self.root, text="👤 Enter User Details", font=self.header_font, bg="black", fg="white").pack(pady=20)

        # User Information Frame for better layout
        user_frame = tk.Frame(self.root, bg="black")
        user_frame.pack(pady=10)

        # User Information Fields
        self.create_label_and_entry(user_frame, "User ID", self.user_id, "This is your unique identifier.")
        self.create_label_and_entry(user_frame, "Name", self.user_name, "Your name helps to personalize the app experience.")
        self.create_label_and_entry(user_frame, "Age", self.age, "Age can influence your health risk factors.")
        self.create_label_and_entry(user_frame, "Weight (kg)", self.weight, "Your weight helps in determining your health status.")
        self.create_label_and_entry(user_frame, "Height (cm)", self.height, "Your height is used to calculate BMI.")
        
        # Activity Level Combobox
        tk.Label(user_frame, text="Activity Level 📝", font=self.label_font, bg="black", fg="white").grid(row=5, column=0, sticky='e', padx=10, pady=10)
        activity_level_combo = ttk.Combobox(user_frame, textvariable=self.activity_level, font=self.entry_font, width=20)
        activity_level_combo['values'] = ["low", "moderate", "high"]
        activity_level_combo.grid(row=5, column=1, pady=10)
        activity_level_combo.bind("<FocusIn>", lambda event: self.show_tip("Activity level helps to assess your physical activity, which affects your health risk."))

        # Submit Button
        submit_btn = tk.Button(self.root, text="Submit User Info", command=self.submit_user_info,
                               font=self.button_font, bg="#1abc9c", fg="black", activebackground="black", bd=3,
                               width=25, height=2)
        submit_btn.pack(pady=30)

        # Add animated emoji indicators
        self.status_label = tk.Label(self.root, text="💫", font=("Helvetica", 24), bg="black", fg="white")
        self.status_label.pack(side="bottom", pady=10)
        self.animate_status_emoji()

    def create_label_and_entry(self, parent_frame, label_text, text_var, tip_text):
        """ Utility function to create a label, entry widget, and tip for the user input form. """
        row = len(parent_frame.grid_slaves()) // 2  # Calculate current row to place fields
        tk.Label(parent_frame, text=f"{label_text} 📝", font=self.label_font, bg="black", fg="white").grid(row=row, column=0, sticky='e', padx=10, pady=10)
        entry = tk.Entry(parent_frame, textvariable=text_var, font=self.entry_font, relief="flat", width=22, bg="#2c3e50", fg="white")
        entry.grid(row=row, column=1, pady=10)
        entry.bind("<FocusIn>", lambda event: self.show_tip(tip_text))

    def show_tip(self, tip_text):
        """ Shows a tip to help users understand the importance of each input field. """
        tip_label = tk.Label(self.root, text=tip_text, font=self.tip_font, fg="yellow", bg="black")
        tip_label.pack(side="bottom", pady=5)
        self.root.after(5000, tip_label.destroy)  # Destroy the tip after 5 seconds

    def submit_user_info(self):
        """ Handles user information submission and proceeds to daily health data. """
        try:
            if not self.user_id.get() or not self.user_name.get():
                raise ValueError("User ID and Name are required.")
            if not self.age.get().isdigit() or int(self.age.get()) <= 0:
                raise ValueError("Age must be a positive integer.")
            if not self.weight.get().replace('.', '', 1).isdigit() or float(self.weight.get()) <= 0:
                raise ValueError("Weight must be a positive number.")
            if not self.height.get().replace('.', '', 1).isdigit() or float(self.height.get()) <= 0:
                raise ValueError("Height must be a positive number.")
            if self.activity_level.get().lower() not in ["low", "moderate", "high"]:
                raise ValueError("Activity level must be 'low', 'moderate', or 'high'.")

            # Proceed to Daily Data Input Form
            self.show_daily_data_form()

        except ValueError as e:
            messagebox.showerror("Input Error", f"🚫 {e}")

    def show_daily_data_form(self):
        """Enhanced daily data form with animations"""
        # Clear with fade effect
        self.fade_out_widgets()
        
        # Daily Data Header
        tk.Label(self.root, text="📊 Enter Daily Health Data", font=self.header_font, bg="black", fg="white").pack(pady=20)

        # Daily Data Frame
        daily_frame = tk.Frame(self.root, bg="black")
        daily_frame.pack(pady=10)

        # Daily Data Fields
        self.create_label_and_entry(daily_frame, "Blood Glucose (mg/dL)", self.blood_glucose, "Blood glucose levels help monitor diabetes.")
        
        tk.Label(daily_frame, text="Diet 📝", font=self.label_font, bg="black", fg="white").grid(row=1, column=0, sticky='e', padx=10, pady=10)
        diet_combo = ttk.Combobox(daily_frame, textvariable=self.diet, font=self.entry_font, width=20)
        diet_combo['values'] = ["healthy", "unhealthy"]
        diet_combo.grid(row=1, column=1, pady=10)
        diet_combo.bind("<FocusIn>", lambda event: self.show_tip("Diet quality affects your blood sugar levels and overall health."))

        self.create_label_and_entry(daily_frame, "Physical Activity (minutes)", self.physical_activity, "Physical activity helps regulate your blood sugar and improve your health.")

        tk.Label(daily_frame, text="Medication Adherence 📝", font=self.label_font, bg="black", fg="white").grid(row=3, column=0, sticky='e', padx=10, pady=10)
        medication_combo = ttk.Combobox(daily_frame, textvariable=self.medication_adherence, font=self.entry_font, width=20)
        medication_combo['values'] = ["good", "poor"]
        medication_combo.grid(row=3, column=1, pady=10)
        medication_combo.bind("<FocusIn>", lambda event: self.show_tip("Taking your medications as prescribed is crucial for managing diabetes."))

        tk.Label(daily_frame, text="Stress Level 📝", font=self.label_font, bg="black", fg="white").grid(row=4, column=0, sticky='e', padx=10, pady=10)
        stress_combo = ttk.Combobox(daily_frame, textvariable=self.stress_level, font=self.entry_font, width=20)
        stress_combo['values'] = ["low", "medium", "high"]
        stress_combo.grid(row=4, column=1, pady=10)
        stress_combo.bind("<FocusIn>", lambda event: self.show_tip("Stress can impact blood sugar levels, so it's important to manage it."))

        self.create_label_and_entry(daily_frame, "Sleep Hours", self.sleep_hours, "Good sleep is crucial for blood sugar control and overall health.")

        tk.Label(daily_frame, text="Hydration Level 📝", font=self.label_font, bg="black", fg="white").grid(row=6, column=0, sticky='e', padx=10, pady=10)
        hydration_combo = ttk.Combobox(daily_frame, textvariable=self.hydration_level, font=self.entry_font, width=20)
        hydration_combo['values'] = ["yes", "no"]
        hydration_combo.grid(row=6, column=1, pady=10)
        hydration_combo.bind("<FocusIn>", lambda event: self.show_tip("Staying hydrated helps in regulating blood sugar levels."))

        # Submit Button for Daily Data
        submit_btn = tk.Button(self.root, text="Submit Daily Data", command=self.submit_daily_data,
                               font=self.button_font, bg="#e74c3c", fg="black", activebackground="#c0392b", bd=0,
                               width=20, height=2)
        submit_btn.pack(pady=30)

        # Add more emojis to labels
        daily_data_fields = [
            ("Blood Glucose", "🩺 Blood Glucose (mg/dL) 📊"),
            ("Diet", "🍎 Diet 🥗"),
            ("Physical Activity", "🏃‍♂️ Physical Activity (minutes) 🎯"),
            ("Medication Adherence", "💊 Medication Adherence 📅"),
            ("Stress Level", "🧘‍♂️ Stress Level 😌"),
            ("Sleep Hours", "😴 Sleep Hours 🌙"),
            ("Hydration Level", "💧 Hydration Level 🚰")
        ]

    def fade_out_widgets(self):
        """Creates a fade-out effect for widgets"""
        for widget in self.root.winfo_children():
            widget.pack_forget()
        self.root.update()
        time.sleep(0.3)

    def submit_daily_data(self):
        """ Handles daily data submission and calculates risk score. """
        try:
            # Validate Daily Data Inputs
            if not self.blood_glucose.get().isdigit() or int(self.blood_glucose.get()) <= 0:
                raise ValueError("Blood Glucose must be a positive integer.")
            if self.diet.get().lower() not in ["healthy", "unhealthy"]:
                raise ValueError("Diet must be 'healthy' or 'unhealthy'.")
            if not self.physical_activity.get().isdigit() or int(self.physical_activity.get()) < 0:
                raise ValueError("Physical activity must be a non-negative integer.")
            if self.medication_adherence.get().lower() not in ["good", "poor"]:
                raise ValueError("Medication adherence must be 'good' or 'poor'.")
            if self.stress_level.get().lower() not in ["low", "medium", "high"]:
                raise ValueError("Stress level must be 'low', 'medium', or 'high'.")
            if not self.sleep_hours.get().replace('.', '', 1).isdigit() or float(self.sleep_hours.get()) < 0:
                raise ValueError("Sleep hours must be a non-negative number.")
            if self.hydration_level.get().lower() not in ["yes", "no"]:
                raise ValueError("Hydration level must be 'yes' or 'no'.")

            # Map input data to numeric values for model prediction
            diet = 1 if self.diet.get().lower() == "healthy" else 0
            medication_adherence = 1 if self.medication_adherence.get().lower() == "good" else 0
            stress_level_map = {"low": 0, "medium": 1, "high": 2}
            stress_level = stress_level_map[self.stress_level.get().lower()]
            hydration_level = 1 if self.hydration_level.get().lower() == "yes" else 0

            # Create input feature array (ensure number of features matches training data)
            features = np.array([[
                float(self.blood_glucose.get()),
                float(self.physical_activity.get()),
                diet,
                medication_adherence,
                stress_level,
                float(self.sleep_hours.get())
            ]])

            # Transform features using the saved scaler
            features_scaled = scaler.transform(features)

            # Predict risk score using the trained model
            risk_score = xgb_model.predict(features_scaled)[0]
            self.show_feedback(risk_score)

        except ValueError as e:
            messagebox.showerror("Input Error", f"🚫 {e}")
        except Exception as e:
            messagebox.showerror("Error", f"⚠️ An error occurred: {e}")

    def show_feedback(self, risk_score):
        """Enhanced feedback with animated emojis"""
        motivational_quotes = [
            "🌟 Every step you take is a step towards a healthier you!",
            "👍 Consistency is key, keep up the great work!",
            "💪 Believe in yourself, you've got this!",
            "✨ Your health journey is unique, and you're doing amazing!",
            "📈 Small changes lead to big results, stay positive!",
            "🔥 Your dedication is inspiring, keep pushing forward!"
        ]
        random_quote = random.choice(motivational_quotes)

        if risk_score < 20:
            feedback = f"🎉 Great job, {self.user_name.get()}! Your risk is currently low! Keep maintaining your lifestyle!"
        elif 20 <= risk_score < 50:
            feedback = f"⚠️ Moderate risk. Please consult your care team or try to improve your physical activity, diet, and stress management, {self.user_name.get()}."
        else:
            feedback = f"🚨 High risk. Please seek medical attention and follow your care plan closely, {self.user_name.get()}."

        messagebox.showinfo("Risk Score and Feedback", f"Risk Score: {risk_score:.2f}\n\n{feedback}\n\nMotivational Message: {random_quote}")

        # Simulate sharing data with clinician
        self.share_data_with_clinician(risk_score)

        # Add animated celebration effect for low risk
        if risk_score < 20:
            self.show_celebration_animation()

    def share_data_with_clinician(self, risk_score):
        """ Simulate sharing patient's data with clinician's EHR."""
        # Convert data to JSON-serializable format
        fhir_data = {
            "user_id": self.user_id.get(),
            "name": self.user_name.get(),
            "age": int(self.age.get()),
            "records": [
                {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "blood_glucose": int(self.blood_glucose.get()),
                    "diet": self.diet.get(),
                    "physical_activity": int(self.physical_activity.get()),
                    "medication_adherence": self.medication_adherence.get(),
                    "stress_level": self.stress_level.get(),
                    "sleep_hours": float(self.sleep_hours.get()),
                    "hydration_level": self.hydration_level.get(),
                    "risk_score": float(risk_score)  # Convert to Python float to ensure JSON compatibility
                }
            ]
        }

        # Simulating HL7 FHIR data exchange by converting to JSON
        try:
            fhir_payload = json.dumps(fhir_data, indent=4)
            print(f"FHIR Data Exchange with EHR: {fhir_payload}")
            messagebox.showinfo("Data Sync", "✅ Data successfully shared with clinician's EHR!")
        except TypeError as e:
            messagebox.showerror("Serialization Error", f"🚫 Failed to serialize data: {e}")

    def animate_text(self, text, label, index=0):
        """Animates text appearing letter by letter"""
        if index < len(text):
            label.config(text=text[:index + 1])
            self.root.after(100, lambda: self.animate_text(text, label, index + 1))

    def animate_status_emoji(self):
        """Animates the status emoji"""
        emojis = ["💫", "✨", "🌟", "⭐", "🌠"]
        current = self.status_label.cget("text")
        next_emoji = emojis[(emojis.index(current) + 1) % len(emojis)]
        self.status_label.config(text=next_emoji)
        self.root.after(800, self.animate_status_emoji)

    def show_celebration_animation(self):
        """Shows a celebration animation"""
        celebration_emojis = ["🎉", "🎊", "✨", "💫", "🌟"]
        
        def animate_celebration(index=0):
            if index < len(celebration_emojis) * 3:  # Repeat 3 times
                emoji = celebration_emojis[index % len(celebration_emojis)]
                celebration_label = tk.Label(self.root, text=emoji, font=("Helvetica", 40), bg="black", fg="white")
                celebration_label.place(relx=0.5, rely=0.5, anchor="center")
                self.root.after(300, celebration_label.destroy)
                self.root.after(300, lambda: animate_celebration(index + 1))
        
        animate_celebration()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = DiabetesManagementApp(root)
    root.mainloop()