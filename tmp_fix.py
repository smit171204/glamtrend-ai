import json
import os

filepath = "c:/Users/smitd/OneDrive/Desktop/brainy_beam/notebooks/NLP_Analysis.ipynb"
with open(filepath, "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source_str = "".join(cell['source'])
        if "BASE_DIR = os.path.dirname(__file__)" in source_str:
            new_source = """import os\nfrom pathlib import Path\n\n_cwd = Path.cwd()\nBASE_DIR = str(_cwd.parent if _cwd.name.lower() == "notebooks" else _cwd)\n\nrf_path = os.path.join(BASE_DIR, "model", "random_forest.pkl")\nlr_path = os.path.join(BASE_DIR, "model", "logistic_model.pkl")\n"""
            lines = new_source.split('\n')
            
            # format properly into cell['source'] array
            cell['source'] = [line + '\n' for line in lines[:-1]]
            
            # Clear outputs since it failed
            cell['outputs'] = []

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print("Notebook cell fixed.")
