#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def simulate_ar1(phi: float, sigma: float, T: int, seed: int = 123):
    rng = np.random.default_rng(seed)
    eps = rng.normal(0.0, sigma, size=T)
    x = np.zeros(T)
    # Inicializar en la media estacionaria (0) para AR(1) con media cero
    for t in range(1, T):
        x[t] = phi * x[t - 1] + eps[t]
    return x

def sample_acf(x: np.ndarray, max_lag: int) -> np.ndarray:
    """
    ACF muestral r(h) = sum_{t=h+1..T} (X_t - X̄)(X_{t-h} - X̄) / sum_{t=1..T} (X_t - X̄)^2
    Retorna r(0)..r(max_lag)
    """
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    denom = np.sum(x**2)
    acf_vals = [1.0]
    for h in range(1, max_lag + 1):
        num = np.sum(x[h:] * x[:-h])
        acf_vals.append(num / denom if denom != 0 else 0.0)
    return np.array(acf_vals)

def ols_through_origin(y: np.ndarray, x: np.ndarray):
    """
    Estima beta en y = beta * x + e (sin intercepto).
    Retorna beta_hat, residuales, sigma2_hat, se_beta (OLS clásico).
    Nota: en series de tiempo, la se_beta de OLS ignora correlación serial posible.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    num = np.dot(x, y)
    den = np.dot(x, x)
    beta_hat = num / den if den != 0 else np.nan
    resid = y - beta_hat * x
    n = len(y)
    # Var(e) estimada: SSE / (n - k), con k=1 (solo beta)
    sigma2_hat = np.dot(resid, resid) / max(n - 1, 1)
    se_beta = np.sqrt(sigma2_hat / den) if den > 0 else np.nan
    return beta_hat, resid, sigma2_hat, se_beta

def main():
    parser = argparse.ArgumentParser(description="Simula AR(1) y estima phi por OLS.")
    parser.add_argument("--phi", type=float, default=0.7, help="phi verdadero (default 0.7)")
    parser.add_argument("--sigma", type=float, default=1.0, help="desv. estándar del ruido (default 1.0)")
    parser.add_argument("--T", type=int, default=200, help="número de observaciones (default 200)")
    parser.add_argument("--lags", type=int, default=40, help="lags máximos para ACF (default 40)")
    parser.add_argument("--seed", type=int, default=123, help="semilla (default 123)")
    parser.add_argument("--outdir", type=str, default="outputs", help="carpeta de salida (default outputs)")
    args = parser.parse_args()

    # 1) Simulación
    x = simulate_ar1(args.phi, args.sigma, args.T, seed=args.seed)

    # 2) Gráficos: serie y ACF
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Serie
    fig1 = plt.figure(figsize=(10, 4.5))
    plt.plot(np.arange(1, args.T + 1), x)
    plt.title(f"AR(1): phi={args.phi}, sigma={args.sigma}, T={args.T}, seed={args.seed}")
    plt.xlabel("t")
    plt.ylabel("X_t")
    plt.tight_layout()
    fig1_path = outdir / "ar1_series.png"
    fig1.savefig(fig1_path, dpi=150)

    # ACF muestral con bandas ±1.96/sqrt(T)
    acf_vals = sample_acf(x, args.lags)
    conf = 1.96 / np.sqrt(args.T)
    lags = np.arange(0, args.lags + 1)

    fig2 = plt.figure(figsize=(10, 4.5))
    plt.bar(lags, acf_vals, width=0.6)
    plt.axhline(0.0)
    plt.axhline(conf, linestyle="--")
    plt.axhline(-conf, linestyle="--")
    plt.title(f"ACF muestral hasta lag {args.lags}")
    plt.xlabel("Lag h")
    plt.ylabel("r(h)")
    plt.tight_layout()
    fig2_path = outdir / "ar1_acf.png"
    fig2.savefig(fig2_path, dpi=150)

    # 3) Estimación de phi por OLS en Xt = beta * Xt-1 + e
    y = x[1:]
    Xlag = x[:-1]
    beta_hat, resid, sigma2_hat, se_beta = ols_through_origin(y, Xlag)

    # 4) Comparación con el valor real
    diff = beta_hat - args.phi

    # Reporte por consola
    print("[RESULTADOS]")
    print(f"  phi verdadero       : {args.phi:.4f}")
    print(f"  phi estimado (OLS)  : {beta_hat:.4f}")
    print(f"  diferencia (hat-true): {diff:+.4f}")
    print(f"  se(beta_hat) [OLS]  : {se_beta:.4f}   (nota: OLS clásico)")
    print(f"  Var(e) estimada     : {sigma2_hat:.4f}")
    print()
    print("[ARCHIVOS]")
    print(f"  Serie: {fig1_path.resolve()}")
    print(f"  ACF  : {fig2_path.resolve()}")
    print()
    print("[NOTA]")
    print("  - La ACF teórica de un AR(1) estacionario es rho(h) = phi^h.")
    print("  - Si |phi| >= 1, el proceso NO es estacionario: la varianza crece sin cota")
    print("    (phi=1: random walk; phi=-1: alternancia con acumulación de choques).")
    print("  - En esos casos, la inferencia OLS usual es inválida (unit root, no varianza finita).")

    # Mostrar (opcional)
    plt.show()

if __name__ == "__main__":
    main()