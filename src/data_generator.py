import pandas as pd
import numpy as np
import os

# Define paths so it works perfectly in VS Code regardless of where you click 'run'
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '../data')
output_path = os.path.join(data_dir, 'synthetic_patient_flow_data.csv')

# Ensure the data directory exists
os.makedirs(data_dir, exist_ok=True)

print("Initializing patient data simulation...")

# Set seed for reproducibility so your results match your README
np.random.seed(42)

# Generate 5,000 synthetic patient records
n_patients = 5000

data = {
    'patient_id': range(1, n_patients + 1),
    'age': np.random.normal(65, 15, n_patients).clip(18, 100).astype(int),
    'comorbidity_score': np.random.randint(0, 10, n_patients),
    
    # Workflow Metrics (The "bottlenecks" from your resume)
    'time_to_bed_hours': np.random.exponential(4, n_patients).round(1),
    'med_recon_delay_hours': np.random.exponential(12, n_patients).round(1),
    'discharge_summary_delay_days': np.random.normal(2, 1.5, n_patients).clip(0, 10).round(1),
    'follow_up_scheduled': np.random.choice([0, 1], n_patients, p=[0.4, 0.6]),
}

df = pd.DataFrame(data)

# Create the Target Variable: 30-Day Readmission
# We engineer the math here so that workflow delays logically *cause* higher readmission probabilities
readmit_prob = (
    (df['age'] * 0.001) + 
    (df['comorbidity_score'] * 0.02) + 
    (df['med_recon_delay_hours'] * 0.005) + 
    (df['discharge_summary_delay_days'] * 0.03) - 
    (df['follow_up_scheduled'] * 0.15)
)

# Normalize probabilities to be between 0.05 and 0.40 (realistic hospital readmission rates)
readmit_prob = np.clip(readmit_prob, 0.05, 0.40)

# Generate the final binary outcome (1 = readmitted, 0 = not readmitted)
df['readmitted_30_days'] = np.random.binomial(1, readmit_prob)

# Save to CSV
df.to_csv(output_path, index=False)
print(f"Success! Generated {n_patients} records and saved to {output_path}")