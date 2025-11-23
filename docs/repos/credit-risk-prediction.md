# credit-risk-prediction

Neural network models for credit risk prediction with explainable AI

[View on GitHub](https://github.com/Digital-AI-Finance/credit-risk-prediction){ .md-button .md-button--primary }


---




## Publications


### Publication 1



| Property | Value |
|----------|-------|
| DOI | [10.2139/ssrn.3456789](https://doi.org/10.2139/ssrn.3456789) |








---

### Publication 2



| Property | Value |
|----------|-------|


| SSRN | [3456789](https://ssrn.com/abstract=3456789) |






---



## Information

| Property | Value |
|----------|-------|
| Language | Unknown |
| Stars | 0 |
| Forks | 0 |
| Watchers | 0 |
| Open Issues | 0 |
| License | No License |
| Created | 2025-11-21 |
| Last Updated | 2025-11-21 |
| Last Push | 2025-11-21 |
| Contributors | 1 |
| Default Branch | main |
| Visibility | public |


## Topics

`credit-risk` `explainable-ai` `finance` `neural-networks` 







## Reproducibility


This repository includes reproducibility tools:


- Python requirements.txt













## Status





- Issues: Enabled
- Wiki: Disabled
- Pages: Disabled

## README

# Explainable Credit Risk Prediction

Repository for "Explainable Neural Networks for Credit Risk Assessment" (SSRN:3456789).

## Authors

- Maria Garcia (Financial Analytics Lab)
- Robert Chen (AI Research Center)

## Abstract

We develop an explainable neural network architecture for credit risk prediction that achieves state-of-the-art performance while providing interpretable feature importance scores using SHAP values.

## Published Paper

- **SSRN**: https://ssrn.com/abstract=3456789
- **DOI**: 10.2139/ssrn.3456789

## Dataset

We use the German Credit Dataset and a proprietary dataset from a major bank:
- `data/german_credit.csv` - Public German Credit Data
- `data/features.csv` - Engineered features

## Notebooks

- `notebooks/01_data_exploration.ipynb` - Exploratory data analysis
- `notebooks/02_feature_engineering.ipynb` - Feature creation and selection
- `notebooks/03_model_training.ipynb` - Neural network training
- `notebooks/04_explainability.ipynb` - SHAP analysis and interpretation

## Requirements

```
tensorflow>=2.8.0
scikit-learn>=1.0.0
shap>=0.40.0
pandas>=1.3.0
matplotlib>=3.4.0
jupyter>=1.0.0
```

## Citation

```bibtex
@article{garcia2023explainable,
  title={Explainable Neural Networks for Credit Risk Assessment},
  author={Garcia, Maria and Chen, Robert},
  journal={SSRN Electronic Journal},
  year={2023},
  doi={10.2139/ssrn.3456789}
}
```

## Replication

To replicate our results:

1. Install dependencies: `pip install -r requirements.txt`
2. Run notebooks in order: `jupyter notebook`
3. Train model: `python train.py`
4. Generate predictions: `python predict.py`
