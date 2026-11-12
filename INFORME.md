# Informe del Parcial 3 - Ingeniería de Software

## Parte 1. Requisitos y criterios de aceptación

**Estudiante:** Yeleinys Gomez  
**Código estudiantil:** 0182410068  
**Asignatura:** Ingeniería de Software I (273365)  
**Proyecto:** Cotizador de envíos EnvíaYa

## 1.1 Parámetros personalizados

Los seis últimos dígitos de `0182410068` son `410068`; en orden: **A=4, B=1, C=0, D=0, E=6, F=8**.

| Parámetro | Cálculo propio | Valor |
|---|---|---:|
| PMAX | 30 + 5 × A = 30 + 5 × 4 | 50 kg |
| L1 | 2 + (B mod 3) = 2 + (1 mod 3) | 3 kg |
| L2 | 10 + C = 10 + 0 | 10 kg |
| RR | 10 + 5 × (E mod 4) = 10 + 5 × 2 | 20 % |
| RN | 40 + 5 × (F mod 3) = 40 + 5 × 2 | 50 % |
| V | 10 + 5 × (A mod 3) = 10 + 5 × 1 | 15 % |
| S | 2.000 + 500 × (C mod 4) = 2.000 + 0 | $2.000 |
| CAMBIO | (A + F) mod 3 = (4 + 8) mod 3 | 0 |

**Reglas de paridad:** D=0 es par, así que el tramo 1 incluye `peso = 3 kg`; E=6 es par, así que el recargo de fin de semana se suma antes de los descuentos; B=1 es impar, así que se aplican los descuentos de cliente y cupón de manera secuencial, primero cliente y luego cupón; F=8 es par, así que un cupón desconocido se ignora.

La solicitud asignada por CAMBIO=0 es añadir la zona insular con 70 % de recargo y sin cupones. Se analizará e implementará como evolución en la Parte 8.

## 1.2 Especificación del cálculo (R1–R8)

| ID | Requisito personalizado |
|---|---|
| **R1 — Peso** | El peso debe ser numérico y cumplir `0 < peso ≤ 50 kg`. Si no, se lanza `ValueError("peso inválido")`. |
| **R2 — Dominio** | La zona debe ser `urbana`, `rural` o `nacional`; el día debe ser un entero entre 1 y 7, donde 6 es sábado y 7 es domingo. Si la zona o el día no son válidos, se lanza un error. |
| **R3 — Tarifa base** | Si `0 < peso ≤ 3 kg`, la tarifa es $6.000. Si `3 < peso ≤ 10 kg`, es $9.000. Si `peso > 10 kg`, es `$9.000 + $800 × (peso − 10)`, proporcional para pesos decimales. |
| **R4 — Zona** | Urbana: sin recargo. Rural: sumar 20 % de la tarifa base. Nacional: sumar 50 % de la tarifa base. |
| **R5 — Fin de semana** | Para sábado o domingo, sumar $2.000 después del recargo de zona y antes de los descuentos, porque E=6 es par. En días 1–5 no se suma. |
| **R6 — Descuentos** | Cliente normal: 0 %. Frecuente: 5 %. VIP: 15 %. Cupón `ENVIO10`: 10 %. Si coinciden descuento de cliente y cupón, se aplican ambos de forma secuencial: primero cliente y luego cupón, porque B=1 es impar. |
| **R7 — Cupón desconocido** | Un cupón distinto de `ENVIO10` se ignora, porque F=8 es par. |
| **R8 — Piso y redondeo** | El costo final no puede ser menor que $5.000. Después se redondea al múltiplo de $100 más cercano; los empates de $50 se redondean hacia arriba. |

## 1.3 Historias de usuario y criterios de aceptación

### HU-01 — Validar la solicitud y calcular la tarifa base

**Como** auxiliar de EnvíaYa, **quiero** validar peso, zona y día, y obtener la tarifa base según el tramo, **para** evitar cotizar con entradas inválidas o con una tarifa incorrecta.

| Dado | Cuando | Entonces |
|---|---|---|
| Una solicitud con peso numérico mayor que 0 y menor o igual a 50 kg, zona válida y día entero entre 1 y 7. | El auxiliar solicita el cálculo. | El sistema acepta la solicitud y continúa con las demás reglas del costo. |
| Un peso igual a 0, menor que 0 o mayor que 50 kg. | El auxiliar solicita el cálculo. | El sistema lanza `ValueError("peso inválido")`. |
| Una zona diferente de urbana, rural o nacional, o un día que no sea entero entre 1 y 7. | El auxiliar solicita el cálculo. | El sistema rechaza la solicitud con un error de validación. |
| Un envío urbano de 3 kg y otro de 10,5 kg, ambos en día hábil y sin descuentos. | El auxiliar solicita la tarifa base de cada uno. | El envío de 3 kg queda en el primer tramo y vale $6.000; el de 10,5 kg queda en el tercero y su base es $9.400. |

### HU-02 — Aplicar los recargos de zona y fin de semana

**Como** asesor de envíos, **quiero** aplicar el recargo del destino y el de fin de semana en el orden correcto, **para** informar el costo correspondiente a la ruta y al día del envío.

| Dado | Cuando | Entonces |
|---|---|---|
| Un envío urbano, rural o nacional con la misma tarifa base. | El asesor calcula el recargo territorial. | Urbana no aumenta; rural aumenta 20 %; nacional aumenta 50 %. |
| Un envío de $9.000 a zona urbana, sin descuentos, programado para el sábado. | El asesor calcula el total. | Se suman $2.000 antes de descuentos y el subtotal es $11.000. |
| Un envío programado de lunes a viernes (días 1–5). | El asesor calcula el total. | No se agrega el recargo de $2.000. |

### HU-03 — Aplicar descuentos y obtener un total consistente

**Como** cliente de EnvíaYa, **quiero** que se apliquen mis descuentos, el cupón y el redondeo según las reglas personalizadas, **para** conocer el importe final correcto.

| Dado | Cuando | Entonces |
|---|---|---|
| Un cliente frecuente o VIP con cupón `ENVIO10`. | El sistema calcula el total. | Aplica primero 5 % o 15 % al cliente y después 10 % al cupón. |
| Un cliente con un cupón desconocido. | El sistema calcula el total. | Ignora el cupón y conserva el descuento que corresponda al cliente. |
| Un envío cuyo total con descuentos sea menor que $5.000. | El sistema finaliza el cálculo. | Eleva el costo a $5.000 y luego lo redondea al múltiplo de $100 más cercano, con empate hacia arriba. |

## 1.4 Matriz inicial de trazabilidad

Los IDs de casos se incorporarán al diseñar la caja negra en la Parte 3.

| Requisito | Historia | Casos de prueba |
|---|---|---|
| R1 — Peso | HU-01 | Pendiente de Parte 3 |
| R2 — Dominio | HU-01 | Pendiente de Parte 3 |
| R3 — Tarifa base | HU-01 | Pendiente de Parte 3 |
| R4 — Zona | HU-02 | Pendiente de Parte 3 |
| R5 — Fin de semana | HU-02, HU-03 | Pendiente de Parte 3 |
| R6 — Descuentos | HU-03 | Pendiente de Parte 3 |
| R7 — Cupón desconocido | HU-03 | Pendiente de Parte 3 |
| R8 — Piso y redondeo | HU-03 | Pendiente de Parte 3 |


## Parte 2. Plan de pruebas

### 2.1 Alcance

El plan cubre el cálculo de costos de EnvíaYa definido en R1–R8: validación de peso, zona y día; tramos de tarifa; recargos rural y nacional; recargo de sábado y domingo; descuentos de cliente y cupón; tratamiento de cupón desconocido; piso de $5.000 y redondeo a $100. La solicitud asignada de zona insular (R9) se incorporará al plan de regresión cuando se analice e implemente en la Parte 8.

Se probará el módulo de cálculo desde su función pública, primero con el código heredado y después de corregir/refactorizarlo. No se incluyen interfaz gráfica, persistencia, pagos, integraciones con transportadoras ni rendimiento de un sistema de producción.

### 2.2 Niveles de prueba

| Nivel | Aplicación al caso EnvíaYa |
|---|---|
| **Unidad** | Verificar cada decisión del cálculo: validación de peso, elección de tramo, recargo por zona, calendario, descuentos, piso y redondeo. Cada prueba usa entradas controladas y un resultado esperado calculado de forma independiente. |
| **Integración** | Verificar el orden al combinar las reglas: tarifa base → zona → fin de semana → cliente → cupón → mínimo → redondeo. Para R9 se comprobará que la estrategia insular aplique 70 % y rechace todo cupón. |
| **Sistema** | Ejecutar la función completa con solicitudes válidas e inválidas y comprobar el precio final o la excepción observada desde la interfaz pública. Repetir sobre la línea base y la versión corregida. |
| **Aceptación** | Recorrer los criterios Dado/Cuando/Entonces de HU-01 a HU-03, vincular cada resultado con su caso y verificar que los valores coincidan con esta especificación personalizada. En la Parte 8 se añaden criterios de aceptación para R9. |

### 2.3 Estrategia, ambiente y roles

**Estrategia.** Derivar casos de particiones de equivalencia, valores límite y tabla de decisión; diseñar caminos independientes para caja blanca; calcular a mano al menos cinco resultados; escribir primero las pruebas de la solicitud de cambio; ejecutar la regresión después de cada corrección. Medir cobertura de sentencias y ramas y conservar la salida real. Una cobertura alta no se considerará prueba suficiente de corrección.

**Ambiente.** Windows y Python 3.12.14 en el entorno de trabajo observado. La suite se ejecutará con pytest y pytest-cov, administrados con uv. Al dejar el comando definitivo en el informe se anotarán las versiones exactas de pytest y pytest-cov, el commit evaluado y la fecha de ejecución. Git conservará la línea base y las ramas de trabajo.

**Roles.** La estudiante actúa como analista de requisitos, diseñadora y ejecutora de pruebas, y responsable del mantenimiento del código. El docente evalúa el informe y dirige la sustentación dinámica indicada en el parcial.

### 2.4 Riesgos y mitigaciones

| Riesgo | Efecto | Mitigación |
|---|---|---|
| Usar parámetros o reglas de otro estudiante como propios. | Resultados esperados, CONFIG e informe no corresponderían al código estudiantil. | Recalcular las fórmulas con `410068`, verificar las paridades y usar ejemplos y casos propios. |
| Interpretar mal el orden de recargos y descuentos. | Precio incorrecto aunque los porcentajes sean correctos. | Escribir el orden en R5–R6, incluir combinaciones en la tabla de decisión y mostrar los subtotales en cálculos manuales. |
| Omitir límites o empates de redondeo. | Defectos en transiciones de tramo o en valores monetarios cercanos a la centena. | Probar valores inmediatamente debajo, en y encima de 0, L1, L2 y PMAX; probar un empate de $50. |
| Registrar como defecto una diferencia causada por un oráculo incorrecto. | Correcciones innecesarias o falsas fallas. | Calcular los esperados a mano desde R1–R8 y revisar cada operación antes de ejecutar la prueba. |
| Perder evidencia o no poder reproducir la ejecución. | Métricas y reporte no verificables. | Guardar salida de pytest, cobertura y capturas en `evidencias/`; anotar comando, versión y commit. |
| Introducir regresiones durante la refactorización o R9. | Una corrección rompe reglas que ya funcionaban. | Mantener la misma matriz de casos, ejecutarla tras cada cambio y añadir primero los casos de R9. |
| Concentrar el historial en un único commit al final. | El proceso de avance solicitado por el docente no sería visible. | Registrar cada archivo o avance real en un commit separado y publicar esos commits en el remoto al terminar cada parte. |

### 2.5 Criterios de entrada y salida

**Entrada:** R1–R8 y sus parámetros revisados; R9 identificada como cambio asignado; función heredada disponible sin correcciones; casos con entradas y resultados esperados definidos; herramientas y repositorio identificados.

**Salida:** casos diseñados y trazados; resultados de ejecución conservados; defectos reproducibles documentados con severidad y prioridad; regresión de la versión corregida aprobada; cobertura de sentencias y ramas reportada; informe, CHANGELOG, etiquetas y evidencias coherentes con el repositorio entregado.
