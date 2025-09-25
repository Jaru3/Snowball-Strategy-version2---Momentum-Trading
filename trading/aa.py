import pandas as pd
import numpy as np

# CSV 파일 로드
file_path = 'krw-btc-result.csv'
df = pd.read_csv(file_path).drop(columns=['Unnamed: 0'])

# 전략별 데이터
strategies = df.columns[:-2]  # original_price 제외

# 지표 계산 함수들
def calculate_cagr(data):
    start_value = data.iloc[0]
    end_value = data.iloc[-1]
    n = len(data) / 365
    return (end_value / start_value) ** (1 / n) - 1

def calculate_mdd(data):
    cumulative = data / data.iloc[0]
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

def calculate_sharpe(data, risk_free_rate=0.01):
    daily_returns = data.pct_change().dropna()
    excess_returns = daily_returns - risk_free_rate / 365
    return excess_returns.mean() / excess_returns.std()

def calculate_var(data, alpha=0.05):
    daily_returns = data.pct_change().dropna()
    return np.percentile(daily_returns, alpha * 100)

def calculate_cvar(data, alpha=0.05):
    daily_returns = data.pct_change().dropna()
    var = np.percentile(daily_returns, alpha * 100)
    return daily_returns[daily_returns <= var].mean()

# EWMA 지표 계산 함수
def calculate_ewma_metrics(data, lambda_):
    ewma_series = data.ewm(span=(1 / (1 - lambda_))).mean()
    cagr = calculate_cagr(ewma_series)
    mdd = calculate_mdd(ewma_series)
    sharpe = calculate_sharpe(ewma_series)
    var = calculate_var(ewma_series)
    cvar = calculate_cvar(ewma_series)
    return [cagr, mdd, sharpe, var, cvar]

# 일반 평가
evaluation = []
for strategy in strategies:
    series = df[strategy]
    evaluation.append([strategy, calculate_cagr(series), calculate_mdd(series), calculate_sharpe(series), calculate_var(series), calculate_cvar(series)])

evaluation_df = pd.DataFrame(evaluation, columns=['Strategy', 'CAGR', 'MDD', 'Sharpe', 'VaR', 'CVaR'])

# EWMA 평가
ewma_results = {}
for lambda_ in [0.999, 0.998, 0.997, 0.993]:
    ewma_eval = []
    for strategy in strategies:
        series = df[strategy]
        ewma_eval.append([strategy] + calculate_ewma_metrics(series, lambda_))
    ewma_results[lambda_] = pd.DataFrame(ewma_eval, columns=['Strategy', 'CAGR', 'MDD', 'Sharpe', 'VaR', 'CVaR'])

# 정렬
evaluation_df = evaluation_df.sort_values(by=['CAGR', 'Sharpe', 'MDD'], ascending=[False, False, True])
for lambda_, df_ in ewma_results.items():
    ewma_results[lambda_] = df_.sort_values(by=['CAGR', 'Sharpe', 'MDD'], ascending=[False, False, True])

# 데이터프레임 출력
print("\n일반 평가 결과:")
print(evaluation_df)
for lambda_, df_ in ewma_results.items():
    print(f"\nEWMA(\u03bb={lambda_}) 평가 결과:")
    print(df_)