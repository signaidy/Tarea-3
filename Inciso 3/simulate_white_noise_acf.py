import argparse
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def sample_acf(x: np.ndarray, max_lag: int) -> np.ndarray:
    """
    ACF muestral r(h) = sum_{t=h+1..T} (X_t - X̄)(X_{t-h} - X̄) / sum_{t=1..T} (X_t - X̄)^2
    Devuelve un vector de tamaño max_lag+1 con r(0)..r(max_lag).
    """
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    denom = np.sum(x**2)
    acf_vals = [1.0]  # r(0) = 1
    for h in range(1, max_lag + 1):
        num = np.sum(x[h:] * x[:-h])
        acf_vals.append(num / denom if denom != 0 else 0.0)
    return np.array(acf_vals)

def main():
    parser = argparse.ArgumentParser(description="Simula ruido blanco y grafica su ACF.")
    parser.add_argument("--n", type=int, default=1000, help="Tamaño de la muestra (default: 1000)")
    parser.add_argument("--mean", type=float, default=0.0, help="Media del ruido blanco (default: 0.0)")
    parser.add_argument("--std", type=float, default=1.0, help="Desv. estándar del ruido (default: 1.0)")
    parser.add_argument("--lags", type=int, default=40, help="Lags máximos para la ACF (default: 40)")
    parser.add_argument("--seed", type=int, default=42, help="Semilla aleatoria (default: 42)")
    parser.add_argument("--outdir", type=str, default="outputs", help="Carpeta para guardar gráficos (default: outputs)")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    x = rng.normal(loc=args.mean, scale=args.std, size=args.n)

    # Calcula ACF muestral
    acf_vals = sample_acf(x, args.lags)

    # Bandas de confianza aproximadas bajo H0 (ruido blanco): ±1.96/sqrt(T)
    conf = 1.96 / np.sqrt(args.n)

    # Crear carpeta de salida
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # --- Figura 1: Serie de tiempo ---
    fig1 = plt.figure(figsize=(10, 4.5))
    plt.plot(np.arange(1, args.n + 1), x)
    plt.title(f"Ruido blanco N({args.mean}, {args.std}^2) — n={args.n}, seed={args.seed}")
    plt.xlabel("t")
    plt.ylabel("X_t")
    plt.tight_layout()
    fig1_path = outdir / "white_noise_series.png"
    fig1.savefig(fig1_path, dpi=150)

    # --- Figura 2: ACF muestral ---
    lags = np.arange(0, args.lags + 1)
    fig2 = plt.figure(figsize=(10, 4.5))
    plt.bar(lags, acf_vals, width=0.6, align="center")
    plt.axhline(0.0)
    plt.axhline(conf, linestyle="--")
    plt.axhline(-conf, linestyle="--")
    plt.title(f"ACF muestral hasta lag {args.lags}")
    plt.xlabel("Lag h")
    plt.ylabel("r(h)")
    plt.tight_layout()
    fig2_path = outdir / "white_noise_acf.png"
    fig2.savefig(fig2_path, dpi=150)

    print(f"[OK] Gráficos guardados en: {outdir.resolve()}")
    print(f" - Serie: {fig1_path.name}")
    print(f" - ACF:   {fig2_path.name}")

    # Mostrar en pantalla (opcional)
    plt.show()

if __name__ == "__main__":
    main()