\newpage

## Introducción

En esta práctica se estudian conceptos fundamentales de los procesos estocásticos y su aplicación a las **series de tiempo**.  
Una serie de tiempo puede entenderse como una realización de un proceso aleatorio, y su análisis permite modelar fenómenos dependientes del tiempo, como temperatura, precios, o señales financieras.

Se implementaron dos simulaciones en Python para observar de forma empírica:
1. El comportamiento del **ruido blanco** y su función de autocorrelación.  
2. Un proceso **autoregresivo AR(1)** y cómo estimar su parámetro $\phi$ mediante regresión lineal.

---

## Inciso 1 — Simetría de la autocovarianza

### 1) Partimos de la definición de covarianza

$$
\gamma(h)=\mathrm{Cov}(X_t,X_{t+h})
=\mathbb{E}\big[(X_t-\mu)(X_{t+h}-\mu)\big].
$$

Análogamente,

$$
\gamma(-h)=\mathrm{Cov}(X_t,X_{t-h})
=\mathbb{E}\big[(X_t-\mu)(X_{t-h}-\mu)\big].
$$

### 2) Reindexamos el tiempo en $\gamma(-h)$

Hacemos el cambio de variable de índice $s=t-h$ (equivalente a “correr” la línea de tiempo). Entonces $t=s+h$ y:

$$
\gamma(-h)
=\mathbb{E}\big[(X_{s+h}-\mu)(X_s-\mu)\big].
$$

### 3) Usamos conmutatividad del producto dentro de la esperanza

El producto de reales conmute:
$$
(X_{s+h}-\mu)(X_s-\mu)=(X_s-\mu)(X_{s+h}-\mu).
$$
Por tanto,
$$
\gamma(-h)=\mathbb{E}\big[(X_s-\mu)(X_{s+h}-\mu)\big].
$$

### 4) Invocamos estacionariedad (depende solo del desfase)

Para un proceso débilmente estacionario, la cantidad
$\mathbb{E}[(X_s-\mu)(X_{s+h}-\mu)]$ **no depende de $s$**, solo del lag $h$. Es precisamente $\gamma(h)$. Luego:

$$
\gamma(-h)=\mathbb{E}\big[(X_s-\mu)(X_{s+h}-\mu)\big]=\gamma(h).
$$

Con esto queda probado que $\gamma(h)=\gamma(-h)$, es decir, la función de autocovarianza es **par** (simétrica respecto a 0).

---

### Observación alternativa (propiedad básica de covarianza)

Otra forma muy corta (pero misma idea):

1. $\mathrm{Cov}(X,Y)=\mathrm{Cov}(Y,X)$ siempre (definición simétrica).
2. Entonces
   $$
   \gamma(h)=\mathrm{Cov}(X_t,X_{t+h})=\mathrm{Cov}(X_{t+h},X_t).
   $$
3. Si el proceso es débilmente estacionario, $\mathrm{Cov}(X_{t+h},X_t)$ depende solo de la diferencia $(t)-(t+h)=-h$, y por definición es $\gamma(-h)$.

Así, $\gamma(h)=\gamma(-h)$.

---

### Nota sobre la hipótesis

* La **simetría** $\mathrm{Cov}(X_s,X_t)=\mathrm{Cov}(X_t,X_s)$ es siempre cierta.
* Para poder llamar a esa cantidad “$\gamma(h)$” sin mencionar $t$, necesitamos **estacionariedad débil**, que garantiza que la covarianza solo depende del desfase $h$ y no del tiempo absoluto. Bajo esa hipótesis, la conclusión $\gamma(h)=\gamma(-h)$ es inmediata.

---

\newpage

## Inciso 2 — Estacionariedad: motivación, ejemplo con tendencia y transformación

### (a) ¿Por qué nos “conviene” que una serie sea estacionaria?

**Intuición corta:** si la serie es estacionaria, sus propiedades básicas (media, varianza y autocovarianza) **no cambian en el tiempo**. Eso permite:

* **Aprender patrones estables**: lo que inferimos hoy (correlaciones, varianza) seguirá siendo válido mañana.
* **Modelos más simples y robustos**: muchos métodos (ARMA/ARIMA, Box–Jenkins, pruebas de raíz unitaria, etc.) **suponen** estacionariedad o la requieren para que la inferencia sea válida.
* **Pronósticos más confiables**: al no “moverse” las reglas del juego en el tiempo, la extrapolación es más sensata.
* **Comparabilidad**: podemos comparar periodos distintos sin que la media/varianza cambien por tendencias o cambios de escala.

En cambio, una serie **no estacionaria** (p. ej., con tendencia) cambia sus reglas: la media se desplaza, la varianza puede crecer, y las covarianzas dependen de la fecha, lo que dificulta modelar y predecir.

---

### (b) ¿Es $Y_t = a + bt + \varepsilon_t$ estacionaria?

Supuestos: $\mathbb{E}[\varepsilon_t]=0,\ \mathrm{Var}(\varepsilon_t)=\sigma^2,\ \mathrm{Cov}(\varepsilon_t,\varepsilon_{t+h})=0$ para $h\neq 0$ (ruido blanco).

1. **Media**
   $$
   \mathbb{E}[Y_t]=\mathbb{E}[a+bt+\varepsilon_t]=a+bt+0=a+bt.
   $$
   Esta **depende de $t$** si $b\neq 0$. Por tanto, **no es constante**.

2. **Varianza**
   $$
   \mathrm{Var}(Y_t)=\mathrm{Var}(a+bt+\varepsilon_t)=\mathrm{Var}(\varepsilon_t)=\sigma^2,
   $$
   constante (bien).

3. **Autocovarianza**
   Para $h\neq 0$,
   $$
   \mathrm{Cov}(Y_t,Y_{t+h})
   = \mathrm{Cov}(a+bt+\varepsilon_t,\ a+b(t+h)+\varepsilon_{t+h})
   = \mathrm{Cov}(\varepsilon_t,\varepsilon_{t+h}) = 0,
   $$
   y para $h=0$, $\gamma(0)=\sigma^2$. Depende solo de $h$ (bien).

**Conclusión:** falla la condición $\mathbb{E}[X_t]=\mu$ constante cuando $b\neq 0$.  
$\Rightarrow$ **$Y_t$ no es (débilmente) estacionaria** salvo en el caso trivial $b=0$.

---

### (c) ¿Cómo transformar $Y_t$ para volverla estacionaria?

Dos caminos clásicos (equivalentes en este caso):

#### Opción 1: **Detrending (quitar tendencia)**

Si restamos la tendencia determinista $a+bt$:
$$
Z_t \;=\; Y_t - (a+bt) \;=\; \varepsilon_t.
$$
$\varepsilon_t$ es **ruido blanco**: media 0, varianza $\sigma^2$ constante y autocovarianza 0 para $h\neq 0$.  
$\Rightarrow$ $Z_t$ **sí es estacionaria**.

> En la práctica no conocemos $a,b$. Se **estiman** por MCO en la regresión $Y_t\sim 1+t$, y usamos los **residuales** $\widehat{\varepsilon}_t = Y_t - (\hat a + \hat b t)$, que suelen comportarse aproximadamente estacionarios.

#### Opción 2: **Diferenciación de primer orden**

Tomamos la primera diferencia:
$$
\Delta Y_t \;=\; Y_t - Y_{t-1} \;=\; (a+bt+\varepsilon_t) - (a+b(t-1)+\varepsilon_{t-1})
= b + (\varepsilon_t - \varepsilon_{t-1}).
$$

* **Media:** $\mathbb{E}[\Delta Y_t]=b$ (constante). Si deseamos media cero, restamos $b$ estimado (o simplemente centramos la serie).
* **Varianza:** $\mathrm{Var}(\Delta Y_t)=\mathrm{Var}(\varepsilon_t-\varepsilon_{t-1})
  = \sigma^2+\sigma^2-2\cdot 0=2\sigma^2$ (constante).
* **Autocovarianza:**  
  $\gamma_{\Delta}(1)=\mathrm{Cov}(\Delta Y_t,\Delta Y_{t+1})
  = \mathrm{Cov}(\varepsilon_t-\varepsilon_{t-1},\ \varepsilon_{t+1}-\varepsilon_t) = -\sigma^2$;  
  $\gamma_{\Delta}(h)=0$ para $|h|>1$.  
  Es decir, $\Delta Y_t$ es un **MA(1)** con parámetro $-1$ (más un término constante $b$). Es **estacionaria**.

---

## Resumen rápido

* (a) Estacionariedad = reglas estables → modelos más simples y pronósticos más fiables.
* (b) $Y_t=a+bt+\varepsilon_t$ **no es estacionaria** si $b\neq 0$ porque su **media cambia con $t$**.
* (c) Para hacerla estacionaria:
  * **Quitar tendencia**: usar residuales de $Y_t$ tras regresión en $(1,t)$.
  * **O diferenciar**: $\Delta Y_t = Y_t-Y_{t-1}$ (y, si se quiere, **demeanar** $\Delta Y_t$ restando $\hat b$).

---

\newpage

## Inciso 3 — Ruido Blanco y Función de Autocorrelación

### Definición recordada

$$
r(h) \;=\; \frac{\sum_{t=h+1}^{T} \big(X_t - \bar{X}\big)\big(X_{t-h} - \bar{X}\big)}
{\sum_{t=1}^{T}\big(X_t - \bar{X}\big)^2}
$$

donde:

- $X_t$ = valor de la serie en el tiempo $t$,
- $\bar{X}$ = media muestral de toda la serie,
- $h$ = desfase o “lag” (cuántos pasos atrás comparamos),
- $T$ = tamaño total de la muestra.

---

### 🔍 (a) ¿Qué estamos midiendo?

En palabras simples:

**$r(h)$ mide el grado de relación lineal entre los valores de la serie separados por $h$ periodos de tiempo.**

O sea, cuánto se parece la serie a sí misma cuando la desplazamos $h$ pasos.

---

### 💡 Interpretación intuitiva

* Si $r(h)$ es **positivo y grande** (cercano a 1), significa que los valores de la serie **tienden a repetirse** o moverse en la misma dirección cada $h$ pasos:
  👉 cuando $X_t$ es alto, $X_{t-h}$ también suele serlo.

* Si $r(h)$ es **negativo y grande en valor absoluto** (cercano a −1), significa que los valores de la serie **tienden a moverse en sentido contrario** cada $h$ pasos:
  👉 cuando $X_t$ es alto, $X_{t-h}$ suele ser bajo.

* Si $r(h) \approx 0$, no hay relación lineal apreciable entre $X_t$ y $X_{t-h}$:
  👉 la serie se comporta como ruido blanco (sin memoria).

---

### ⚙️ En otras palabras:

* Es la **versión estandarizada de la autocovarianza muestral**, por eso siempre:
  $$
  -1 \le r(h) \le 1
  $$
* Nos dice **qué tanta “memoria” o dependencia temporal** tiene la serie.
* Es la herramienta básica para:
  * Detectar **tendencias o periodicidades**,
  * Identificar **modelos AR(p)** o **MA(q)** (por ejemplo, mediante el **gráfico ACF**).

---

### 🔍 (b) Simule las realizaciones de una serie de tiempo de ruido blanco

**Objetivo.**  
Simular un proceso de **ruido blanco** $X_t \sim \mathcal{N}(\mu, \sigma^2)$ y calcular su **función de autocorrelación muestral (ACF)** para comprobar que los valores son prácticamente cero para todos los lags $h \ge 1$.

**Pasos realizados.**

1. **Configuración del entorno:**
   ```bash
   cd "Inciso 3"
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # En Windows
   pip install numpy matplotlib
```

2. **Ejecución del script:**

   ```bash
   python simulate_white_noise_acf.py --n 1000 --lags 40 --mean 0 --std 1 --seed 42
   ```

3. **Acciones del script:**

   * Genera una serie aleatoria con distribución normal $\mathcal{N}(0,1)$.
   * Calcula la ACF muestral mediante:
     $$
     r(h) = \frac{\sum_{t=h+1}^{T} (X_t - \bar{X})(X_{t-h} - \bar{X})}{\sum_{t=1}^{T}(X_t - \bar{X})^2}
     $$
   * Traza dos gráficos:

     * Serie simulada `white_noise_series.png`
     * ACF muestral `white_noise_acf.png` con bandas de confianza $\pm 1.96/\sqrt{T}$.

**Resultados.**

**Figura 1. Serie de tiempo simulada (ruido blanco):**

> ![Serie Ruido Blanco](../../Inciso%203/outputs/white_noise_series.png)

**Figura 2. Función de autocorrelación (ACF):**

> ![ACF Ruido Blanco](../../Inciso%203/outputs/white_noise_acf.png)

Los coeficientes $r(h)$ se encuentran dentro de las bandas de confianza para todos los $h \ge 1$, confirmando que **no existe dependencia temporal** y que la serie se comporta como ruido blanco.

---

\newpage

## Inciso 4 - Regresión lineal vs. AR(1) y el supuesto de independencia

### **Regresión lineal clásica:**

$$
Y = X\beta + \varepsilon
$$

con los supuestos clásicos de los errores:

1. $\mathbb{E}[\varepsilon] = 0$
2. $\mathrm{Var}(\varepsilon) = \sigma^2 I$  (homocedasticidad e independencia)
3. $\mathrm{Cov}(\varepsilon_i, \varepsilon_j) = 0$ para $i \neq j$  (**no autocorrelación**)

---

### **Modelo autoregresivo de orden 1 (AR(1)):**

$$
X_t = \phi X_{t-1} + \varepsilon_t, \quad \varepsilon_t \sim \text{ruido blanco}
$$

Aquí, cada valor depende **del anterior** → hay **dependencia temporal**.

---

### Comparación estructural

| Aspecto                  | Regresión lineal ($Y = X\beta + \varepsilon$) | Autoregresivo ($X_t = \phi X_{t-1} + \varepsilon_t$)         |
| ------------------------ | --------------------------------------------- | ------------------------------------------------------------ |
| Variable dependiente     | $Y$ (obs. independientes)                     | $X_t$ (depende del pasado)                                   |
| Independencia            | Los $\varepsilon_i$ son independientes        | Los $X_t$ están correlacionados                              |
| Covarianza entre errores | $0$                                           | $\mathrm{Cov}(X_t, X_{t-1}) = \frac{\phi\sigma^2}{1-\phi^2}$ |
| Objetivo                 | Explicar $Y$ con $X$ exógenas                 | Explicar $X_t$ con su propio pasado                          |
| Estimación adecuada      | OLS                                           | Máx. verosimilitud, Yule–Walker, etc.                        |

---

### ¿Qué supuesto se viola al ignorar la dependencia temporal?

👉 **Se viola el supuesto de independencia de los errores.**

En un modelo autoregresivo, las observaciones están correlacionadas a lo largo del tiempo, y eso implica que los **errores del modelo de regresión lineal estarían autocorrelacionados** si tratamos la serie como independiente.

Formalmente:

$$
\mathrm{Cov}(\varepsilon_t, \varepsilon_{t+h}) \neq 0
$$

para algunos $h \neq 0$.

**Consecuencias:**

1. Estimadores aún insesgados (si hay exogeneidad), pero **ineficientes**.
2. **Errores estándar mal estimados**, pruebas t/F e IC inválidos.
3. **Se sobrestima la información efectiva** (datos “repetidos” por autocorrelación).

---

\newpage

## Inciso 5 — AR(1): media, varianza, estacionariedad y ACF

Considere $X_t=\phi X_{t-1}+\varepsilon_t$, con $\varepsilon_t\sim \mathcal N(0,\sigma^2)$, independientes.

### (a) $\mathbb{E}[X_t]$ y $\mathrm{Var}(X_t)$ bajo estacionariedad

**Media.** Tomando esperanza a ambos lados:
$$
\mathbb{E}[X_t]=\phi,\mathbb{E}[X_{t-1}]+\mathbb{E}[\varepsilon_t]
=\phi,\mathbb{E}[X_{t-1}]+0.
$$
En estacionariedad $\mathbb{E}[X_t]=\mathbb{E}[X_{t-1}]=\mu$, así que $\mu=\phi\mu\Rightarrow (1-\phi)\mu=0$.
Si $|\phi|<1$ (caso estacionario no degenerado), entonces $\mu=0$.

**Varianza.** Usando independencia:
$$
\mathrm{Var}(X_t)=\phi^2,\mathrm{Var}(X_{t-1})+\mathrm{Var}(\varepsilon_t)
=\phi^2,\mathrm{Var}(X_{t-1})+\sigma^2.
$$
En estacionariedad $\mathrm{Var}(X_t)=\mathrm{Var}(X_{t-1})=v$, entonces:
$$
v=\phi^2 v+\sigma^2 ;\Rightarrow; v(1-\phi^2)=\sigma^2 ;\Rightarrow; \boxed{\mathrm{Var}(X_t)=\dfrac{\sigma^2}{1-\phi^2}}.
$$

---

### (b) Estacionariedad si y solo si $|\phi|<1$

**($\Rightarrow$) Si el proceso es estacionario, entonces $|\phi|<1$.**
Para $|\phi|=1$:

* $\phi=1$: $X_t=X_{t-1}+\varepsilon_t$ (random walk) ⇒ $\mathrm{Var}(X_t)=\mathrm{Var}(X_0)+t\sigma^2$ crece con $t$ ⇒ no estacionario.
* $\phi=-1$: $X_t=-X_{t-1}+\varepsilon_t$ ⇒ la varianza también crece (acumulación de choques) ⇒ no estacionario.

**($\Leftarrow$) Si $|\phi|<1$, entonces es estacionario.**
Desenrollando recursivamente:
$$
X_t=\sum_{j=0}^{\infty}\phi^{j}\varepsilon_{t-j},
$$
la serie **converge en $L^2$** cuando $|\phi|<1$ (pues $\sum \phi^{2j}<\infty$). Entonces:
$$
\mathbb{E}[X_t]=0,\qquad \mathrm{Var}(X_t)=\sum_{j=0}^{\infty}\phi^{2j}\sigma^2=\frac{\sigma^2}{1-\phi^2},
$$
y
$$
\mathrm{Cov}(X_t,X_{t+h})=\sigma^2\sum_{j=0}^{\infty}\phi^{j}\phi^{j+h}=\frac{\sigma^2}{1-\phi^2},\phi^{h},
$$
que no depende de $t$ (solo del lag). Por tanto, el proceso es (débilmente) estacionario.

**Conclusión:** $\boxed{\text{AR(1) es estacionario } \iff |\phi|<1.}$

---

### (c) Función de autocorrelación $r(h)$ (ACF teórica)

La autocovarianza en lag $h\ge 0$ para $|\phi|<1$ es:
$$
\gamma(h)=\mathrm{Cov}(X_t,X_{t+h})=\frac{\sigma^2}{1-\phi^2}\,\phi^{h}.
$$

La ACF es $r(h)=\rho(h)=\dfrac{\gamma(h)}{\gamma(0)}$. Como $\gamma(0)=\dfrac{\sigma^2}{1-\phi^2}$,
$$
\boxed{\,r(h)=\rho(h)=\phi^{|h|},\qquad h=0,1,2,\dots\,}.
$$

---

\newpage

## Inciso 6 — Simulación de un Proceso AR(1)

### Objetivo

Simular un proceso **autoregresivo de primer orden**:
$$
X_t = \phi X_{t-1} + \varepsilon_t, \qquad \varepsilon_t \sim \mathcal{N}(0, \sigma^2)
$$
con parámetros:
$$
\phi = 0.7,\quad \sigma = 1,\quad T = 200
$$
y realizar:

* (a) Graficar la serie y su ACF.
* (b) Estimar $\phi$ mediante OLS.
* (c) Comparar con el valor verdadero.
* (d) Analizar el caso $|\phi| \ge 1$.

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
   * Estima $\phi$ usando regresión OLS sin intercepto en:
     $$
     X_t = \beta X_{t-1} + \varepsilon_t
     $$
   * Reporta:

     * $\hat{\phi}$ estimado
     * Error estándar OLS
     * Diferencia $\hat{\phi} - 0.7$
   * Muestra notas sobre el comportamiento cuando $|\phi|\ge 1$.

---

### 📈 Resultados

**Figura 3. Serie de tiempo AR(1) con $\phi = 0.7$:**

> ![Serie AR1](../../Inciso%206/outputs/ar1_series.png)

**Figura 4. Función de autocorrelación (ACF) del AR(1):**

> ![ACF AR1](../../Inciso%206/outputs/ar1_acf.png)

El patrón de la ACF decrece geométricamente como $r(h) = \phi^h$, lo cual coincide con el comportamiento teórico del modelo AR(1).

El valor estimado $\hat{\phi}$ obtenido mediante OLS fue **muy cercano a 0.7**, confirmando que el procedimiento de estimación reproduce el parámetro verdadero bajo estacionariedad.

---

### 🧠 Discusión

* Para $|\phi| < 1$, el proceso es **estacionario** y la varianza converge:
  $$
  \mathrm{Var}(X_t) = \frac{\sigma^2}{1 - \phi^2}
  $$
* Si $|\phi| \ge 1$:

  * $\phi = 1$ → proceso **no estacionario** (random walk), la varianza crece sin límite ($\propto t\sigma^2$).
  * $\phi = -1$ → alternancia de signo, pero también varianza no acotada.
  * En ambos casos, los estimadores OLS pierden validez estadística.

---

## 🧾 Conclusiones

1. El **ruido blanco** presenta autocorrelaciones nulas, validando su independencia temporal.
2. El **AR(1)** con $\phi=0.7$ muestra correlaciones positivas que decrecen con el lag, siguiendo $r(h)=\phi^h$.
3. La estimación por OLS de $\phi$ es consistente y cercana al valor verdadero mientras el proceso sea estacionario.
4. Cuando $|\phi|\ge1$, la varianza diverge y el proceso deja de ser estacionario, por lo que los métodos clásicos dejan de ser válidos.

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