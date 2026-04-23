Phlebotomy Workflow Process Mining
This project analyzes patient workflow in a hospital phlebotomy unit to identify bottlenecks, standardize patient journeys, and optimize operational efficiency. By applying Process Mining techniques to log data, it abstracts complex, raw activity sequences into actionable process patterns.

🚀 Key Objectives
Process Standardization: Abstract complex, raw event logs into meaningful patient journeys.
Bottleneck Identification: Analyze time-based patterns to identify peak hours and inefficient workflows.
Operational Optimization: Provide data-driven insights to manage personnel and patient flow effectively.

🛠 Features
Activity Mapping: Categorizes raw clinical log data into functional groups (e.g., 'Consultation', 'Blood Collection Preparation', 'Prescription').
Sequence Abstraction: Cleans and collapses repetitive sequences to identify unique process pathways.
Exception Handling: Specifically identifies and labels cases of "No Blood Draw" (e.g., patients who entered the preparation phase but did not complete the collection).
Time-Series Visualization: Visualizes the distribution of process patterns across different time slots (hourly analysis) using stacked bar charts to reveal operational trends.

📊 Methodology
Preprocessing: Raw timestamps and event logs are cleaned and sorted by patient ID.
Mapping: Log events are mapped to unified activity groups (Activity_Group1, Activity_Group2).
Pattern Generation: Sequential patient activities are consolidated into distinct patterns (e.g., Consultation -> Blood Collection).
Trend Analysis: Aggregates patterns by time intervals to calculate the ratio of specific workflows throughout the day.

⚠️ Security & Privacy
Note: This repository contains the analysis methodology and source code only.
All sample data processed herein has been strictly anonymized. No Protected Health Information (PHI) or sensitive patient data is stored or shared in this repository.

💻 Technical Stack
Language: Python 
Libraries: * pandas: For data manipulation and sequence analysis.
matplotlib: For visualizing process trends.
numpy: For vectorized calculations.

📈 Example Visualization
(You can upload your generated chart here)
The current analysis provides a stacked bar chart displaying the hourly ratio of process patterns, allowing for easy identification of when specific workflows (e.g., 'Consultation -> Blood Collection') peak.

⚠️ Important Notice: Data Privacy & Compliance
This repository contains the analysis methodology and source code only. The original datasets used in this study belong to the hospital and contain sensitive Protected Health Information (PHI). 
** Due to strict patient privacy regulations and ethical standards, raw hospital data cannot be shared, uploaded, or made public.
** Access to this repository is limited to the analytical logic, data processing workflow, and visualization techniques. 
   All data samples used for testing the code have been strictly anonymized and do not represent any real-world patient records.
