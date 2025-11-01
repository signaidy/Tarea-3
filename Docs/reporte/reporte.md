# 📊 Tarea 3 — Análisis de Series de Tiempo  
**Curso:** Análisis de Datos  
**Tema:** Procesos aleatorios, estacionariedad y autocorrelación  
**Autor:** [Tu nombre aquí]  
**Fecha:** [Fecha de entrega]

---

## 🧩 Introducción

En esta práctica se estudian conceptos fundamentales de los procesos estocásticos y su aplicación a las **series de tiempo**.  
Una serie de tiempo puede entenderse como una realización de un proceso aleatorio, y su análisis permite modelar fenómenos dependientes del tiempo, como temperatura, precios, o señales financieras.

Se implementaron dos simulaciones en Python para observar de forma empírica:
1. El comportamiento del **ruido blanco** y su función de autocorrelación.  
2. Un proceso **autoregresivo AR(1)** y cómo estimar su parámetro φ mediante regresión lineal.

---

## 🧪 Inciso 3 — Ruido Blanco y Función de Autocorrelación

### 📘 Objetivo
Simular un proceso de **ruido blanco** \( X_t \sim \mathcal{N}(\mu, \sigma^2) \) y calcular su **función de autocorrelación muestral (ACF)** para comprobar que los valores son prácticamente cero para todos los lags \( h \ge 1 \).

---

### ⚙️ Pasos realizados

1. **Configuración del entorno:**
   ```bash
   cd "Inciso 3"
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # En Windows
   pip install numpy matplotlib
````

2. **Ejecución del script:**

   ```bash
   python simulate_white_noise_acf.py --n 1000 --lags 40 --mean 0 --std 1 --seed 42
   ```

3. **Acciones del script:**

   * Genera una serie aleatoria con distribución normal ( N(0,1) ).
   * Calcula la ACF muestral mediante:
     [
     r(h) = \frac{\sum_{t=h+1}^{T} (X_t - \bar{X})(X_{t-h} - \bar{X})}{\sum_{t=1}^{T}(X_t - \bar{X})^2}
     ]
   * Traza dos gráficos:

     * Serie simulada `white_noise_series.png`
     * ACF muestral `white_noise_acf.png` con bandas de confianza ±(1.96/\sqrt{T}).

---

### 📈 Resultados

**Figura 1. Serie de tiempo simulada (ruido blanco):**

> ![Serie Ruido Blanco](../Inciso%203/outputs/white_noise_series.png)

**Figura 2. Función de autocorrelación (ACF):**

> ![ACF Ruido Blanco](../Inciso%203/outputs/white_noise_acf.png)

Los coeficientes ( r(h) ) se encuentran dentro de las bandas de confianza para todos los ( h \ge 1 ), confirmando que **no existe dependencia temporal** y que la serie se comporta como ruido blanco.

---

## 🔁 Inciso 6 — Simulación de un Proceso AR(1)

### 📘 Objetivo

Simular un proceso **autoregresivo de primer orden**:
[
X_t = \phi X_{t-1} + \varepsilon_t, \qquad \varepsilon_t \sim \mathcal{N}(0, \sigma^2)
]
con parámetros:
[
\phi = 0.7,\quad \sigma = 1,\quad T = 200
]
y realizar:

* (a) Graficar la serie y su ACF.
* (b) Estimar φ mediante OLS.
* (c) Comparar con el valor verdadero.
* (d) Analizar el caso (|\phi| \ge 1).

---

### ⚙️ Pasos realizados

1. **Configuración del entorno:**

   ```bash
   cd "Inciso 6"
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # En Windows
   pip install numpy matplotlib
   ```

2. **Ejecución del script:**

   ```bash
   python simulate_ar1_acf.py --phi 0.7 --sigma 1 --T 200 --lags 40 --seed 123
   ```

3. **Acciones del script:**

   * Simula el proceso AR(1) con media cero y ruido normal.
   * Calcula la ACF muestral y grafica la serie.
   * Estima ( \phi ) usando regresión OLS sin intercepto en:
     [
     X_t = \beta X_{t-1} + \varepsilon_t
     ]
   * Reporta:

     * ( \hat{\phi} ) estimado
     * Error estándar OLS
     * Diferencia ( \hat{\phi} - 0.7 )
   * Muestra notas sobre el comportamiento cuando (|\phi|\ge 1).

---

### 📈 Resultados

**Figura 3. Serie de tiempo AR(1) con φ = 0.7:**

> ![Serie AR1](../Inciso%206/outputs/ar1_series.png)

**Figura 4. Función de autocorrelación (ACF) del AR(1):**

> ![ACF AR1](../Inciso%206/outputs/ar1_acf.png)

El patrón de la ACF decrece geométricamente como ( r(h) = \phi^h ), lo cual coincide con el comportamiento teórico del modelo AR(1).

El valor estimado ( \hat{\phi} ) obtenido mediante OLS fue **muy cercano a 0.7**, confirmando que el procedimiento de estimación reproduce el parámetro verdadero bajo estacionariedad.

---

### 🧠 Discusión

* Para (|\phi| < 1), el proceso es **estacionario** y la varianza converge:
  [
  \mathrm{Var}(X_t) = \frac{\sigma^2}{1 - \phi^2}
  ]
* Si (|\phi| \ge 1):

  * (\phi = 1) → proceso **no estacionario** (random walk), la varianza crece sin límite ((\propto t\sigma^2)).
  * (\phi = -1) → alternancia de signo, pero también varianza no acotada.
  * En ambos casos, los estimadores OLS pierden validez estadística.

---

## 🧾 Conclusiones

1. El **ruido blanco** presenta autocorrelaciones nulas, validando su independencia temporal.
2. El **AR(1)** con (\phi=0.7) muestra correlaciones positivas que decrecen con el lag, siguiendo (r(h)=\phi^h).
3. La estimación por OLS de (\phi) es consistente y cercana al valor verdadero mientras el proceso sea estacionario.
4. Cuando (|\phi|\ge1), la varianza diverge y el proceso deja de ser estacionario, por lo que los métodos clásicos dejan de ser válidos.

---

## 📂 Archivos generados

| Carpeta             | Archivo                  | Descripción           |
| ------------------- | ------------------------ | --------------------- |
| `Inciso 3/outputs/` | `white_noise_series.png` | Serie de ruido blanco |
| `Inciso 3/outputs/` | `white_noise_acf.png`    | ACF del ruido blanco  |
| `Inciso 6/outputs/` | `ar1_series.png`         | Serie AR(1) simulada  |
| `Inciso 6/outputs/` | `ar1_acf.png`            | ACF del proceso AR(1) |

---

## 🧩 Referencias

* Hamilton, J.D. (1994). *Time Series Analysis*. Princeton University Press.
* Box, G.E.P., Jenkins, G.M., Reinsel, G.C. (2008). *Time Series Analysis: Forecasting and Control*. Wiley.
* Chatfield, C. (2003). *The Analysis of Time Series: An Introduction*. Chapman & Hall/CRC.

---