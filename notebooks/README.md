# Broker Behavior Prediction System

## Overview
This system predicts broker classifications for the following month using a three-stage machine learning pipeline.

## Pipeline Stages

### Stage 1: Others vs nonOthers (Target: 90% accuracy)
- **Others**: Brokers expected to have < 2 competitive loans next month
- **nonOthers**: Brokers expected to have ≥ 2 competitive loans next month

### Stage 2: Confirm nonOthers (Target: 80% accuracy)
- Takes brokers predicted as nonOthers in Stage 1
- Confirms they will remain nonOthers next month
- Acts as a validation layer to reduce false positives

### Stage 3: Whale/Dolphin/Minnow Classification (Target: 70% accuracy)
- **Whale (W)**: ≥ 6 competitive loans (HIGH PRIORITY)
- **Dolphin (D)**: 4-5 competitive loans (MEDIUM PRIORITY)
- **Minnow (M)**: 2-3 competitive loans (LOWER PRIORITY)

## Files

### 01_broker_classification_pipeline.ipynb
**Purpose**: Train the three-stage classification models

**What it does**:
1. Loads historical broker data (6 months)
2. Creates target variables for next month predictions
3. Engineers features from current month metrics
4. Trains and evaluates multiple models for each stage
5. Selects best performing models
6. Saves trained models for production use

**When to run**:
- Initial setup (first time)
- Monthly retraining (recommended)
- When model performance degrades

**Outputs**:
- Trained models saved in `../data/models/`
- Performance metrics and visualizations
- Feature importance analysis

### 02_predict_new_month.ipynb
**Purpose**: Make predictions on new monthly data

**What it does**:
1. Loads pre-trained models
2. Processes new month's broker data
3. Runs three-stage prediction pipeline
4. Generates confidence scores for each prediction
5. Exports results to Excel with multiple sheets

**When to run**:
- Monthly, when new broker data is available

**Outputs**:
- Excel file with predictions by class
- Separate sheets for Whales, Dolphins, Minnows, Others
- Confidence scores for each prediction

## Getting Started

### 1. Initial Setup

```bash
# Create conda environment (if not already done)
conda env create -f ../environment.yml
conda activate ds-portfolio

# Launch Jupyter
jupyter lab
```

### 2. Train Models (First Time)

1. Place your historical data (6+ months) in `../data/raw/Master_One_Sheet.xlsx`
2. Open `01_broker_classification_pipeline.ipynb`
3. Run all cells
4. Check that accuracy targets are met:
   - Stage 1: ≥ 90%
   - Stage 2: ≥ 80%
   - Stage 3: ≥ 70%

### 3. Make Monthly Predictions

1. Place new month's data in `../data/raw/`
2. Open `02_predict_new_month.ipynb`
3. Update the filename in the "Load New Month's Data" section
4. Run all cells
5. Find results in `../data/processed/broker_predictions_[timestamp].xlsx`

## Data Requirements

### Required Columns
Your Excel data must include these columns:
- `Month`: Time period identifier
- `Account Name`: Broker identifier
- `Owner Name`: Broker owner
- `Competitor Loans this Month`: Current month competitive loan count
- UWM metrics (loans, Google Reviews, percentages)
- Binary flags (YES-1 through YES-6, NO-1 through NO-6)

### Data Format
- One row per broker per month
- Numeric features (percentages, counts)
- No formulas (values only)
- Consistent column names across all months

## Using Results in Google Colab

Since you're copying to Google Colab for your boss:

1. **Upload the notebooks to Colab**:
   - Go to https://colab.research.google.com
   - File → Upload notebook
   - Select the `.ipynb` file

2. **Upload your data**:
   - In Colab, use the Files panel (folder icon on left)
   - Upload your Excel file
   - Update file paths in the notebook

3. **Install required packages**:
   ```python
   # Run this in the first cell
   !pip install pandas numpy scikit-learn matplotlib seaborn openpyxl
   ```

## Model Performance Tracking

After each month, compare predictions with actual results:

1. Load previous month's predictions
2. Load actual results
3. Calculate accuracy for each stage
4. If accuracy drops below targets, retrain models

## Troubleshooting

### "File not found" error
- Check file path is correct
- Ensure file is in the right directory
- Use forward slashes (/) not backslashes (\\)

### "Missing features" warning
- Ensure new data has same columns as training data
- Check for typos in column names
- Verify data format matches training data

### Low accuracy
- Check for data quality issues
- Consider feature engineering improvements
- May need hyperparameter tuning
- Ensure sufficient training data (6+ months)

### Import errors in Colab
- Install missing packages: `!pip install package_name`
- Restart runtime if needed

## Next Steps

1. ✅ Train initial models
2. ✅ Validate accuracy targets are met
3. Make first monthly prediction
4. Compare with actual results next month
5. Set up monthly retraining schedule
6. Monitor model performance over time

## Questions?

- Check model performance metrics in notebook outputs
- Review feature importance to understand predictions
- Compare confidence scores - low confidence may need manual review

## Notes for Non-Technical Users

**What this does**: Predicts which brokers will be most active next month

**Why it matters**: Helps prioritize retention efforts on high-value brokers

**How to use**:
1. Run training notebook once (or monthly)
2. Run prediction notebook each month with new data
3. Focus on Whales and Dolphins in the results

**Confidence scores**: Higher = more certain prediction
- > 0.8: Very confident
- 0.6-0.8: Reasonably confident
- < 0.6: Less certain, may need manual review
