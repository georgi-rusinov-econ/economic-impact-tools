# Economic Impact Tools

Python utilities for economic impact assessment, forecasting, and policy analysis. Designed for economists working on Green Book business cases, Magenta Book evaluations, and infrastructure appraisals.

## Features

- **Impact Assessment**: Input-output multiplier calculations, economic impact modelling
- **Cost-Benefit Analysis**: NPV/BCR calculations with Green Book discount rates
- **Forecasting**: Real estate market forecasting, macroeconomic scenario analysis
- **Spatial Analysis**: Location-based economic analysis utilities

## Installation

Clone the repository:
```bash
git clone https://github.com/georgi-rusinov-econ/economic-impact-tools.git
cd economic-impact-tools
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start
```python
from src.cba_tools import calculate_npv_greenbook

# Calculate NPV using Green Book discount rates
cash_flows = [-1000000, 200000, 250000, 300000, 350000, 400000]
years = [0, 1, 2, 3, 4, 5]

npv = calculate_npv_greenbook(cash_flows, years)
print(f"NPV: £{npv:,.0f}")
```

## Repository Structure
```
economic-impact-tools/
├── src/                   # Core Python modules
│   ├── cba_tools.py       # Cost-benefit analysis utilities
│   ├── multipliers.py     # Input-output multiplier calculations
│   └── utils.py           # Helper functions
├── examples/              # Usage examples
├── tests/                 # Unit tests
└── docs/                  # Documentation
```

## Use Cases

- Green Book business cases for infrastructure projects
- Regional economic impact assessments
- Real estate development appraisals
- Transport scheme evaluations
- Regeneration project feasibility studies

## Methodology

Tools are aligned with:
- **UK Green Book** (HM Treasury) for appraisal and evaluation
- **UK Magenta Book** for policy evaluation
- **TAG** (Transport Analysis Guidance) for transport appraisals

## Requirements

- Python 3.8+
- pandas
- numpy

## Contributing

Contributions welcome. Please open an issue to discuss proposed changes.

## License

MIT License - free to use, modify, and distribute.

## Author

**Georgi Rusinov**  
Economist | Real Estate, Urban Development, Transport, Infrastructure  
[LinkedIn](https://www.linkedin.com/in/YOUR-LINKEDIN-URL)

## Citation

If you use these tools in your work:
```
Rusinov, G. (2025). Economic Impact Tools. 
GitHub: https://github.com/georgi-rusinov-econ/economic-impact-tools
```
