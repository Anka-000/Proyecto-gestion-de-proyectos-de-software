#Librerias para la interfaz grafica y manejo de archivos para guardar datos
import tkinter as tk
from tkinter import messagebox
import json
import os
# Nombre del archivo para guardar los datos del usuario
ARCHIVO_USUARIO = "usuario.json"

# Función para validar campos numéricos
def validar_numero(valor, campo_nombre, min_valor, max_valor):
    """Valida que un valor sea numérico y esté dentro de un rango razonable"""
    try:
        numero = float(valor)
        if numero < min_valor or numero > max_valor:
            return False, f"{campo_nombre} debe estar entre {min_valor} y {max_valor}"
        return True, ""
    except ValueError:
        return False, f"{campo_nombre} debe ser un número válido"

# Función para validar edad
def validar_edad(edad_str):
    return validar_numero(edad_str, "Edad", 1, 120)

# Función para validar peso
def validar_peso(peso_str):
    return validar_numero(peso_str, "Peso", 1, 300)

# Función para validar altura con conversión automática
def validar_altura(altura_str):
    """Valida altura, convirtiendo automáticamente de metros a centímetros si es necesario"""
    try:
        altura = float(altura_str)
        
        # Si el valor es menor a 10, probablemente está en metros
        if altura < 10:
            altura_cm = altura * 100  # Convertir metros a cm
            if 50 <= altura_cm <= 250:
                return True, "", altura_cm  # Devolver el valor convertido
            else:
                return False, f"Altura en metros ({altura}m) equivale a {altura_cm}cm, que está fuera del rango permitido (50-250cm)", altura
        else:
            # Ya está en centímetros
            if 50 <= altura <= 250:
                return True, "", altura
            else:
                return False, f"Altura debe estar entre 50 y 250 cm", altura
                
    except ValueError:
        return False, "Altura debe ser un número válido", 0

# Función para validar todos los campos antes de guardar
def validar_campos():
    """Valida todos los campos del formulario antes de guardar"""
    # Validar género
    genero = combo_genero.get()
    if not genero:
        return False, "Por favor selecciona tu género"
    
    # Validar edad
    edad = entry_edad.get().strip()
    if not edad:
        return False, "Por favor ingresa tu edad"
    es_valido, mensaje = validar_edad(edad)
    if not es_valido:
        return False, mensaje
    
    # Validar peso
    peso = entry_peso.get().strip()
    if not peso:
        return False, "Por favor ingresa tu peso"
    es_valido, mensaje = validar_peso(peso)
    if not es_valido:
        return False, mensaje
    
    # Validar altura
    altura = entry_altura.get().strip()
    if not altura:
        return False, "Por favor ingresa tu altura"
    es_valido, mensaje, altura_convertida = validar_altura(altura)
    if not es_valido:
        return False, mensaje
    
    # Validar actividad
    actividad = combo_actividad.get()
    if not actividad:
        return False, "Por favor selecciona tu nivel de actividad"
    
    # Validar objetivo
    objetivo = combo_objetivo.get()
    if not objetivo:
        return False, "Por favor selecciona tu objetivo nutricional"
    
    return True, "Todos los campos son válidos"

# Función para validar entrada en tiempo real (números con punto decimal)
def validar_entrada_numerica(texto):
    """Permite números, punto decimal y backspace"""
    if texto == "":  # Permite borrar
        return True
    # Verificar si es un número decimal válido (solo un punto decimal)
    if texto.count('.') <= 1 and texto.replace('.', '').isdigit():
        return True
    return False

# Función para validar entrada de números enteros
def validar_entrada_entero(texto):
    """Permite solo números enteros y backspace"""
    if texto == "":  # Permite borrar
        return True
    return texto.isdigit()

#Funcion para guardar los datos del usuario en un archivo JSON
def guardar_datos_usuario():
    """Guarda los datos actuales del cuestionario en un archivo JSON."""
    # Primero validar todos los campos
    es_valido, mensaje_error = validar_campos()
    if not es_valido:
        messagebox.showerror("Error de validación", mensaje_error)
        return
    
    try:
        # Obtener y convertir altura si es necesario
        altura_str = entry_altura.get().strip()
        es_valido, mensaje, altura_convertida = validar_altura(altura_str)
        
        datos = {
            "genero": combo_genero.get(),
            "edad": entry_edad.get(),
            "peso": entry_peso.get(),
            "altura": str(altura_convertida),  # Guardar el valor convertido
            "actividad": combo_actividad.get(),
            "objetivo": combo_objetivo.get()
        }
        
        with open(ARCHIVO_USUARIO, "w") as f:
            json.dump(datos, f)
        messagebox.showinfo("Guardado", "Datos guardados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron guardar los datos.\n{e}")

#Funcion para cargar los datos del usuario desde el archivo JSON
def cargar_datos_usuario():
    """Carga los datos del usuario si el archivo existe."""
    if os.path.exists(ARCHIVO_USUARIO):
        try:
            with open(ARCHIVO_USUARIO, "r") as f:
                return json.load(f)
        except Exception:
            messagebox.showwarning("Advertencia", "No se pudieron cargar los datos guardados.")
    return None

#Funcion para calular las calorias diarias recomendadas y macronutrientes
def calcular_calorias():
    try:
        # Intentar obtener datos del formulario si existe
        try:
            genero = combo_genero.get()
            edad = int(entry_edad.get())
            peso = float(entry_peso.get())
            
            # Obtener y convertir altura si es necesario
            altura_str = entry_altura.get().strip()
            es_valido, mensaje, altura_convertida = validar_altura(altura_str)
            if not es_valido:
                messagebox.showerror("Error", mensaje)
                return
            altura = altura_convertida
            
            actividad = combo_actividad.get()
            objetivo = combo_objetivo.get()
        except Exception:
            # Si el formulario no está activo, usar datos guardados
            datos_guardados = cargar_datos_usuario()
            if not datos_guardados:
                messagebox.showwarning("Advertencia", "Primero debes llenar y guardar tus datos en el cuestionario.")
                return

            genero = datos_guardados.get("genero", "Hombre")
            edad = int(datos_guardados.get("edad", 0))
            peso = float(datos_guardados.get("peso", 0))
            altura = float(datos_guardados.get("altura", 0))
            actividad = datos_guardados.get("actividad", "Sedentario")
            objetivo = datos_guardados.get("objetivo", "Mantener peso")

        # Validar datos básicos, asegurandose de que sean datos positivos mayores a cero
        if not (edad > 0 and peso > 0 and altura > 0):
            messagebox.showerror("Error", "Los datos de edad, peso y altura deben ser mayores que cero.")
            return

        # Fórmula simplificada de Harris-Benedict para calcula la TMB dependiendo si es hombre o mujer
        if genero == "Hombre":
            calorias_base = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
        else: #Mujer
            calorias_base = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

        # Ajuste por nivel de actividad
        if actividad == "Sedentario":
            calorias = calorias_base * 1.2
        elif actividad == "Ligero":
            calorias = calorias_base * 1.375
        elif actividad == "Moderado":
            calorias = calorias_base * 1.55
        elif actividad == "Activo":
            calorias = calorias_base * 1.725
        else:  # Muy activo
            calorias = calorias_base * 1.9

        #Ajuste por objetivo nutricional
        if objetivo == "Mantener peso":
            pass  # No se ajusta    
        elif objetivo == "Perder peso":
            calorias = calorias - 500
        elif objetivo == "Perder mucho peso":
            calorias = calorias - 1000
        elif objetivo == "Ganar masa muscular":
            calorias = calorias + 500
        else:  # Ganar mucha masa muscular
            calorias = calorias + 1000

        # Cálculo de macronutrientes según el objetivo
        if objetivo in ["Perder peso", "Perder mucho peso"]:
            # Dieta para pérdida de peso: más proteína, menos carbohidratos
            proteinas_gramos = peso * 2.2  # 2.2g por kg de peso
            grasas_gramos = (calorias * 0.25) / 9  # 25% de calorías de grasas
            calorias_proteinas = proteinas_gramos * 4
            calorias_grasas = grasas_gramos * 9
            calorias_carbohidratos = calorias - calorias_proteinas - calorias_grasas
            carbohidratos_gramos = calorias_carbohidratos / 4
            
        elif objetivo in ["Ganar masa muscular", "Ganar mucha masa muscular"]:
            # Dieta para ganar masa: alta en proteínas y carbohidratos
            proteinas_gramos = peso * 2.0  # 2.0g por kg de peso
            carbohidratos_gramos = (calorias * 0.50) / 4  # 50% de calorías de carbohidratos
            calorias_proteinas = proteinas_gramos * 4
            calorias_carbohidratos = carbohidratos_gramos * 4
            calorias_grasas = calorias - calorias_proteinas - calorias_carbohidratos
            grasas_gramos = calorias_grasas / 9
            
        else:  # Mantener peso
            # Distribución balanceada
            proteinas_gramos = peso * 1.8  # 1.8g por kg de peso
            grasas_gramos = (calorias * 0.25) / 9  # 25% de calorías de grasas
            carbohidratos_gramos = (calorias * 0.55) / 4  # 55% de calorías de carbohidratos

        #Muestra el resultado en una ventana emergente
        resultado = f"""Calorías diarias recomendadas: {calorias:.0f} kcal

Macronutrientes diarios:
• Proteínas: {proteinas_gramos:.1f}g
• Carbohidratos: {carbohidratos_gramos:.1f}g  
• Grasas: {grasas_gramos:.1f}g

Distribución aproximada:
• Proteínas: {(proteinas_gramos * 4 / calorias * 100):.1f}%
• Carbohidratos: {(carbohidratos_gramos * 4 / calorias * 100):.1f}%
• Grasas: {(grasas_gramos * 9 / calorias * 100):.1f}%"""
        
        messagebox.showinfo("Resultado", resultado)
    except:
        #Mensaje de error si no se logra el caculo por cualquier razon
        messagebox.showerror("Error", "Por favor ingresa valores válidos.")


# Se crea la ventana principal con su nombre y su dimension
ventana = tk.Tk()
ventana.title("Cálculo de Calorías Diarias")
ventana.geometry("450x550")
#Se crea un frame para contener los elementos de las diferentes secciones
frame_contenido = tk.Frame(ventana)
frame_contenido.pack(fill="both", expand=True)


#Funcion para mostrar el cuestionario del usuario
def mostrar_cuestionario():
    #Limpia el frame antes de que se muestre
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    #Le da un titulo a la seccion y crea los elementos del formulario
    tk.Label(frame_contenido, text="Cuestionario del Usuario", font=("Arial", 14, "bold")).pack(pady=10)
    #Define las variables como globales para que se usen en otras funciones
    global combo_genero, entry_edad, entry_peso, entry_altura, combo_actividad, combo_objetivo
    
    # Registrar las funciones de validación
    vcmd_numeros = (ventana.register(validar_entrada_numerica), '%P')
    vcmd_entero = (ventana.register(validar_entrada_entero), '%P')
    
    #El combobox para seleccionar el genero
    tk.Label(frame_contenido, text="Género:").pack()
    combo_genero = tk.StringVar()
    tk.OptionMenu(frame_contenido, combo_genero, "Hombre", "Mujer").pack()
    
    #El campo de texto para los años de edad (solo enteros)
    tk.Label(frame_contenido, text="Edad (años):").pack()
    entry_edad = tk.Entry(frame_contenido, validate="key", validatecommand=vcmd_entero)
    entry_edad.pack()
    
    #El campo de texto para el peso en kg (puede ser decimal)
    tk.Label(frame_contenido, text="Peso (kg):").pack()
    entry_peso = tk.Entry(frame_contenido, validate="key", validatecommand=vcmd_numeros)
    entry_peso.pack()
    
    #El campo de texto para la altura (puede ser decimal y en metros o cm)
    tk.Label(frame_contenido, text="Altura (cm o m):").pack()
    entry_altura = tk.Entry(frame_contenido, validate="key", validatecommand=vcmd_numeros)
    entry_altura.pack()
    tk.Label(frame_contenido, text="Ej: 160 cm o 1.60 m", font=("Arial", 8), fg="gray").pack()
    
    #El combobox para seleccionar la actividad fisica
    tk.Label(frame_contenido, text="Nivel de actividad:").pack()
    combo_actividad = tk.StringVar()
    tk.OptionMenu(frame_contenido, combo_actividad, "Sedentario", "Ligero", "Moderado", "Activo", "Muy activo").pack()
    
    #El combobox para seleccionar el objetivo nutricional
    tk.Label(frame_contenido, text="Objetivo nutricional:").pack()
    combo_objetivo = tk.StringVar()
    tk.OptionMenu(frame_contenido, combo_objetivo, "Mantener peso", "Perder peso", "Perder mucho peso",
                  "Ganar masa muscular", "Ganar mucha masa muscular").pack()
    
    #Boton para guardar los datos del usuario, cada vez que se usa llama a la funcion guardar_datos_usuario
    tk.Button(frame_contenido, text="Guardar Datos", bg="blue", fg="white",
              font=("Arial", 11, "bold"), command=guardar_datos_usuario).pack(pady=15)

    # Cargar datos si existen
    datos = cargar_datos_usuario()
    if datos:
        combo_genero.set(datos.get("genero", "Hombre"))
        entry_edad.insert(0, datos.get("edad", ""))
        entry_peso.insert(0, datos.get("peso", ""))
        entry_altura.insert(0, datos.get("altura", ""))
        combo_actividad.set(datos.get("actividad", "Sedentario"))
        combo_objetivo.set(datos.get("objetivo", "Mantener peso"))

#Funcion para mostrar el inicio de la app
def mostrar_inicio():
    #Primero limpia el frame antes de que se muestre
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    #Se agrega un label para el titulo y una descripcion
    tk.Label(frame_contenido, text="Bienvenido a tu Calculadora de Calorías",
             font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(frame_contenido, text="Usa el menú superior para ingresar tus datos.").pack(pady=10)
    #Se agrega un boton para calcular las calorias, llamando a la funcion calcular_calorias
    tk.Button(frame_contenido, text="Calcular Calorías", bg="green", fg="white",
              font=("Arial", 12, "bold"), command=calcular_calorias).pack(pady=20)


#Menu de la app para navegar entre secciones
menu_bar = tk.Menu(ventana)
menu_secciones = tk.Menu(menu_bar, tearoff=0)
#Se agregan las opciones del menu, define la funcion mostrar_inicio como inicio
menu_secciones.add_command(label="Inicio", command=mostrar_inicio)
#Define la funcion mostrar_cuestionario para el cuestionario del usuario
menu_secciones.add_command(label="Cuestionario del Usuario", command=mostrar_cuestionario)
#Se agrega una separacion y la opcion de salir de la app
menu_secciones.add_separator()
menu_secciones.add_command(label="Salir", command=ventana.quit)
#Se agrega el menu a la ventana principal
menu_bar.add_cascade(label="Menú", menu=menu_secciones)
ventana.config(menu=menu_bar)
#Muestra la pantalla de inicio al abrir la app
mostrar_inicio()
ventana.mainloop()