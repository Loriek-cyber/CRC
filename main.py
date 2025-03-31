import tkinter as tk
from tkinter import ttk

def xor(a, b):
    """Esegue l'operazione XOR tra due stringhe binarie della stessa lunghezza."""
    return ''.join('0' if bit_a == bit_b else '1' for bit_a, bit_b in zip(a, b))

def crc_division_gui(dividend, divisor, output_tree):
    """Esegue la divisione binaria XOR per calcolare il quoziente e il resto (CRC) e aggiorna la GUI."""
    # Pulisci la Treeview
    for item in output_tree.get_children():
        output_tree.delete(item)

    # Lunghezze
    dividend_len = len(dividend)
    divisor_len = len(divisor)

    # Aggiunta di zeri per l'operazione (non necessaria qui, l'input dovrebbe già averli)
    temp_dividend = dividend[:divisor_len]
    quotient_list = []
    steps = []

    # Inserisci l'intestazione nella Treeview
    output_tree.insert("", tk.END, values=("Passo", "Dividendo Temporaneo", "Divisore", "Risultato XOR", "Quoziente Parziale"))
    steps.append(("Intestazione", temp_dividend, divisor, "", ""))

    for i in range(divisor_len, dividend_len + 1):
        step = i - divisor_len + 1
        divisor_display = divisor if temp_dividend[0] == '1' else '0' * divisor_len
        xor_result = xor(temp_dividend, divisor_display)
        temp_dividend_before_shift = temp_dividend
        temp_dividend = xor_result[1:]  # XOR e shift
        quotient_bit = '1' if divisor_display == divisor else '0'
        quotient_list.append(quotient_bit)

        if i < dividend_len:
            temp_dividend += dividend[i]

        steps.append((step, temp_dividend_before_shift, divisor_display, xor_result, "".join(quotient_list)))
        output_tree.insert("", tk.END, values=(step, temp_dividend_before_shift, divisor_display, xor_result, "".join(quotient_list)))

    quotient = "".join(quotient_list)
    crc_remainder = temp_dividend

    return quotient, crc_remainder

def calculate_crc():
    data = data_entry.get()
    polynomial = polynomial_entry.get()
    if not all(bit in '01' for bit in data + polynomial):
        result_label.config(text="Errore: Dividendo e divisore devono essere stringhe binarie.")
        return
    if len(data) < len(polynomial):
        result_label.config(text="Errore: Il dividendo deve essere lungo almeno quanto il divisore.")
        return
    if '1' not in polynomial:
        result_label.config(text="Errore: Il divisore deve contenere almeno un '1'.")
        return

    quotient, crc_remainder = crc_division_gui(data, polynomial, output_tree)
    result_label.config(text=f"Quoziente: {quotient}\nCRC (Resto): {crc_remainder}")

# Creazione della finestra principale
window = tk.Tk()
window.title("Calcolatore CRC")

# Etichette e campi di input
data_label = ttk.Label(window, text="Inserisci il messaggio (con zeri aggiunti):")
data_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
data_entry = ttk.Entry(window)
data_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

polynomial_label = ttk.Label(window, text="Inserisci il divisore (polinomio generatore):")
polynomial_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
polynomial_entry = ttk.Entry(window)
polynomial_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Bottone di calcolo
calculate_button = ttk.Button(window, text="Calcola CRC", command=calculate_crc)
calculate_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

# Area di output passo-passo
output_label = ttk.Label(window, text="Passaggi della divisione:")
output_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")

output_tree = ttk.Treeview(window, columns=("Passo", "Dividendo Temporaneo", "Divisore", "Risultato XOR", "Quoziente Parziale"))
output_tree.heading("#1", text="Passo")
output_tree.heading("#2", text="Dividendo Temporaneo")
output_tree.heading("#3", text="Divisore")
output_tree.heading("#4", text="Risultato XOR")
output_tree.heading("#5", text="Quoziente Parziale")

# Imposta la larghezza delle colonne (puoi regolarle)
output_tree.column("#1", width=50)
output_tree.column("#2", width=150)
output_tree.column("#3", width=100)
output_tree.column("#4", width=120)
output_tree.column("#5", width=120)

output_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Etichetta per il risultato finale
result_label = ttk.Label(window, text="Risultato:")
result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

# Configurazione del ridimensionamento delle colonne e delle righe
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(4, weight=1)

# Esecuzione della GUI
window.mainloop()