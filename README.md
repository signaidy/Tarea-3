Este repositorio contiene dos mini-proyectos independientes (cada uno con su propio **.venv**) para:

* **Inciso 3**: simular **ruido blanco** y graficar su **ACF muestral**.
* **Inciso 6**: simular un **AR(1)**, graficar su **ACF**, **estimar φ por OLS** en (X_t=\beta X_{t-1}+\varepsilon_t) y comparar con el valor verdadero.

Estructura sugerida:

```
Tarea 3
├── Docs
├── Inciso 3
│   ├── .venv
│   ├── outputs
│   │   ├── white_noise_acf.png
│   │   └── white_noise_series.png
│   └── simulate_white_noise_acf.py
├── Inciso 6
│   ├── .venv
│   ├── outputs
│   │   ├── ar1_acf.png 
│   │   └── ar1_series.png 
│   └── simulate_ar1_acf.py
└── README.md
```

---

## Requisitos

* Python 3.8+
* Poder crear entornos virtuales con `venv`.

> Cada inciso usa su **propio** entorno virtual dentro de su carpeta (`Inciso 3/.venv` y `Inciso 6/.venv`).

---

## Inciso 3 — Ruido blanco y ACF

**Script:** `Inciso 3/simulate_white_noise_acf.py`
**Qué hace:**

* Simula una serie de **ruido blanco** (X_t \sim \mathcal{N}(\mu, \sigma^2)).
* Calcula la **ACF muestral** hasta un lag especificado.
* Genera 2 gráficos en `Inciso 3/outputs/`:

  * `white_noise_series.png`: serie simulada.
  * `white_noise_acf.png`: ACF con bandas ±(1.96/\sqrt{T}).

### Configuración y ejecución

1. Entrar a la carpeta:

```bash
cd "Inciso 3"
```

2. Crear y activar **.venv**:

* **Windows (PowerShell)**:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

* **macOS / Linux**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install numpy matplotlib
```

4. Ejecutar (ejemplo):

```bash
python simulate_white_noise_acf.py --n 1000 --lags 40 --mean 0 --std 1 --seed 42
```

**Parámetros útiles:**

* `--n` (int): tamaño de muestra (default: 1000)
* `--lags` (int): lags máximos ACF (default: 40)
* `--mean` (float): media (default: 0.0)
* `--std` (float): desviación estándar (default: 1.0)
* `--seed` (int): semilla aleatoria (default: 42)
* `--outdir` (str): carpeta salida (default: `outputs`)

**Salida esperada (insumos para el reporte):**

* ACF cercana a 0 para (h\ge1) (dentro de bandas), y (r(0)=1).

---

## Inciso 6 — AR(1), ACF y estimación de φ por OLS

**Script:** `Inciso 6/simulate_ar1_acf.py`
**Qué hace:**

* Simula un **AR(1)** (X_t=\phi X_{t-1}+\varepsilon_t) con (\varepsilon_t\sim\mathcal{N}(0,\sigma^2)).
* Grafica la **serie** y su **ACF muestral**.
* Estima (\phi) vía **OLS sin intercepto** en (X_t=\beta X_{t-1}+\varepsilon_t).
* Reporta (\hat\phi), su error estándar OLS y la diferencia frente al (\phi) verdadero.

### Configuración y ejecución

1. Entrar a la carpeta:

```bash
cd "Inciso 6"
```

2. Crear y activar **.venv**:

* **Windows (PowerShell)**:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

* **macOS / Linux**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install numpy matplotlib
```

4. Ejecutar (ejemplo pedido en el enunciado):

```bash
python simulate_ar1_acf.py --phi 0.7 --sigma 1 --T 200 --lags 40 --seed 123
```

**Parámetros útiles:**

* `--phi` (float): valor verdadero de (\phi) (default: 0.7)
* `--sigma` (float): (\sigma) del ruido (default: 1.0)
* `--T` (int): tamaño de la serie (default: 200)
* `--lags` (int): lags máximos ACF (default: 40)
* `--seed` (int): semilla (default: 123)
* `--outdir` (str): carpeta salida (default: `outputs`)

**Salidas:**

* `ar1_series.png`: serie simulada.
* `ar1_acf.png`: ACF muestral.
* Consola: (\phi) verdadero, (\hat\phi) (OLS), diferencia, error estándar y (\widehat{\mathrm{Var}}(\varepsilon)).

**Notas teóricas rápidas:**

* Para AR(1) estacionario ((|\phi|<1)), la ACF teórica es (\rho(h)=\phi^{h}).
* Si (|\phi|\ge1): **no estacionario** (p. ej. random walk si (\phi=1)); varianza no constante e inferencia OLS estándar inválida.

---

## Consejos de uso

* Para resultados **reproducibles**, fija `--seed`.
* Si corres ambos incisos en la misma terminal, recuerda activar el **.venv** de cada carpeta por separado.
* Si quieres integrar en un **reporte**, incluye las imágenes PNG generadas y comenta si los valores de la ACF caen dentro de las bandas (ruido blanco) o si decrecen geométricamente (AR(1)).

---

## Solución de problemas

* **No se abre la ventana de gráficos**: las imágenes se guardan siempre en `outputs/`. Verifica esa carpeta.
* **Permisos/activación**: en macOS/Linux puede requerir `chmod +x` si lo ejecutas como script; de lo contrario, usa `python <archivo>.py`.
* **Múltiples Pythons instalados**: usa `python3` en lugar de `python` si es necesario.