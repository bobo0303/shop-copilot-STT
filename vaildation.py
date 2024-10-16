import os
import csv
from api.model import Model
from metrics import wer
import evaluate

PERSON = ['Jake', 'Bobo', 'MH', 'John', 'Sam']  # ['Fake'] ['Jake', 'Bobo', 'MH']

# Initialize model and metrics
model = Model()
default_model = 'paraformer'
print(f"using model: {default_model}")
model.load_model(default_model)

metric = evaluate.load('metrics/wer.py')

# Define the base data directory
base_dir = 'asr_data'
results = []

# Variables for tracking correct and total files
correct_count = 0
total_count = 0

# Iterate over the directories and process each file
for person in PERSON:
    for session in ['1', '2']:
        session_path = os.path.join(base_dir, person, session)

        # Check if the directory exists
        if not os.path.exists(session_path):
            print(f"Directory {session_path} not found. Skipping.")
            continue

        for file_name in os.listdir(session_path):
            if file_name.endswith('.wav'):
                audio_path = os.path.join(session_path, file_name)
                decoded_labels = file_name.replace('.wav', '').lower()  # Use filename as the reference label
                
                # Transcribe the audio file
                result, _ = model.transcribe(audio_path)
                decoded_preds = result['transcription'].lower()
                
                # Add batch for WER calculation
                metric.add_batch(predictions=[decoded_preds], references=[decoded_labels])
                
                # Store the result for later use
                results.append({
                    'file': file_name,
                    'audio_path': audio_path,
                    'prediction': decoded_preds,
                    'reference': decoded_labels
                })

                # Update the total count
                total_count += 1

# Compute WER for all batches
m = metric.compute()
print(f"Overall WER={round(m, 5)}")

# Write the results to a CSV file, but only for errors (WER > 0)
csv_file = f'{default_model}_transcription_results.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['data_file', 'gt', 'predict', 'wer'])

    # Load WER metric once outside the loop
    individual_metric = evaluate.load('metrics/wer.py')

    for res in results:
        # Reset the metric for individual calculation
        individual_metric.add_batch(predictions=[res['prediction']], references=[res['reference']])
        individual_wer = individual_metric.compute()
        writer.writerow([res['audio_path'], res['reference'], res['prediction'], round(individual_wer, 5)])
        file.flush()  # Ensure data is written to the file after each entry

        # Only log entries where WER > 0
        if round(individual_wer, 5) > 0:
            print(f"WER > 0: {res['audio_path']} - WER: {round(individual_wer, 5)}")
            
        else:
            # Increment correct count when WER == 0 (perfect transcription)
            correct_count += 1

    # Write the average WER at the end of the file
    writer.writerow(['avg', '', '', round(m, 5)])

    # Calculate and write the overall accuracy
    accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
    writer.writerow(['Accuracy', f'{round(accuracy, 2)}%', f'{correct_count}', f'{total_count}'])

print(f"Results saved to {csv_file}")
