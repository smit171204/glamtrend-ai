import pandas as pd
import numpy as np

# ==========================
# TASK 1: MISSING VALUE HANDLER
# ==========================
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import LinearRegression

class MissingValueHandler:
    def __init__(self, df):
        self.df = df.copy()
        self.report = {}

    def get_missing_summary(self):
        missing = self.df.isnull().sum()
        percent = (missing / len(self.df)) * 100

        summary = pd.DataFrame({
            "Missing Count": missing,
            "Missing %": percent
        })

        return summary[summary["Missing Count"] > 0]

    def smart_impute(self):
        summary = self.get_missing_summary()

        for col in summary.index:
            missing_percent = summary.loc[col, "Missing %"]

            if missing_percent < 5:
                self.df[col].fillna(self.df[col].median() if self.df[col].dtype != "object" else self.df[col].mode()[0], inplace=True)
                self.report[col] = "simple"

            elif missing_percent < 20:
                imputer = KNNImputer(n_neighbors=5)
                num_cols = self.df.select_dtypes(include=np.number).columns
                self.df[num_cols] = imputer.fit_transform(self.df[num_cols])
                self.report[col] = "knn"

            else:
                imputer = IterativeImputer(estimator=LinearRegression(), max_iter=10)
                num_cols = self.df.select_dtypes(include=np.number).columns
                self.df[num_cols] = imputer.fit_transform(self.df[num_cols])
                self.report[col] = "mice"

        return self.df, self.report


# ==========================
# TASK 2: DATA CLEANING PIPELINE
# ==========================
class DataCleaningPipeline:
    def __init__(self, df):
        self.df = df.copy()
        self.log = {
            "duplicates_removed": 0,
            "columns_removed": []
        }

    def run_pipeline(self):
        # Remove duplicates
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        self.log["duplicates_removed"] = before - len(self.df)

        # Remove irrelevant columns
        cols_to_remove = []

        for col in self.df.columns:
            if "id" in col.lower() or self.df[col].nunique() <= 1:
                cols_to_remove.append(col)

        self.df.drop(columns=cols_to_remove, inplace=True, errors="ignore")
        self.log["columns_removed"] = cols_to_remove

        return self.df, self.log


# ==========================
# TASK 3: STANDARDIZATION
# ==========================
class DataStandardizer:
    def __init__(self, df):
        self.df = df.copy()
        self.log = {}

    def run(self):
        # Column names
        self.df.columns = [col.strip().lower().replace(" ", "_") for col in self.df.columns]

        # Data type conversion
        for col in self.df.columns:
            try:
                self.df[col] = pd.to_numeric(self.df[col])
                self.log[col] = "numeric"
            except:
                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                    self.log[col] = "datetime"
                except:
                    self.df[col] = self.df[col].astype("category")
                    self.log[col] = "category"

        return self.df, self.log


# ==========================
# TASK 4: OUTLIER HANDLING
# ==========================
from scipy import stats

class OutlierHandler:
    def __init__(self, df):
        self.df = df.copy()
        self.log = {}

    def handle(self, method="cap"):
        num_cols = self.df.select_dtypes(include=np.number).columns

        for col in num_cols:
            z = np.abs(stats.zscore(self.df[col].dropna()))
            outliers = z > 3

            count = np.sum(outliers)

            if count == 0:
                continue

            if method == "cap":
                self.df[col] = np.clip(self.df[col],
                                       self.df[col].quantile(0.01),
                                       self.df[col].quantile(0.99))
            elif method == "remove":
                self.df = self.df[~outliers]
            elif method == "transform":
                self.df[col] = np.log1p(self.df[col])

            self.log[col] = count

        return self.df, self.log


# ==========================
# TASK 5: FEATURE SCALING
# ==========================
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

class FeatureScaler:
    def __init__(self, df):
        self.df = df.copy()
        self.scores = {}

    def scale(self):
        num_cols = self.df.select_dtypes(include=np.number).columns

        scalers = {
            "MinMax": MinMaxScaler(),
            "Standard": StandardScaler(),
            "Robust": RobustScaler()
        }

        results = {}

        for name, scaler in scalers.items():
            temp = self.df.copy()
            temp[num_cols] = scaler.fit_transform(temp[num_cols])

            score = temp[num_cols].var().mean()
            self.scores[name] = score
            results[name] = temp

        best = min(self.scores, key=self.scores.get)

        return results[best], best, self.scores