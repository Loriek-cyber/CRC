import tkinter as tk
from tkinter import ttk, messagebox

def xor(a, b):
    """Esegue l'operazione XOR tra due stringhe binarie della stessa lunghezza."""
    return ''.join('0' if bit_a == bit_b else '1' for bit_a, bit_b in zip(a, b))

def crc_division(dividend, divisor):
    """Esegue la divisione binaria XOR e restituisce i passaggi."""
    dividend_len = len(dividend)
    divisor_len = len(divisor)
    steps = []
    
    temp_dividend = dividend[:divisor_len]
    quotient = ''
    
    for i in range(divisor_len, dividend_len + 1):
        step_num = i - divisor_len + 1
        current_dividend = temp_dividend
        
        if current_dividend[0] == '1':
            quotient_bit = '1'
            divisor_used = divisor
        else:
            quotient_bit = '0'
            divisor_used = '0' * divisor_len
        
        xor_result = xor(current_dividend, divisor_used)
        new_dividend = xor_result[1:]
        
        appended_bit = ''
        if i < dividend_len:
            appended_bit = dividend[i]
            new_dividend += appended_bit
        
        steps.append({
            'step': step_num,
            'current_dividend': current_dividend,
            'divisor_used': divisor_used,
            'xor_result': xor_result,
            'quotient_bit': quotient_bit,
            'new_dividend': new_dividend,
            'appended_bit': appended_bit
        })
        
        quotient += quotient_bit
        temp_dividend = new_dividend
    
    return quotient, temp_dividend, steps

class CRCGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizzatore CRC passo per passo")
        self.geometry("1200x600")
        
        # Configurazione griglia principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Frame input
        input_frame = ttk.Frame(self, padding=10)
        input_frame.grid(row=0, column=0, sticky='ew')
        
        ttk.Label(input_frame, text="Messaggio (binario):").grid(row=0, column=0, padx=5, sticky='w')
        self.data_entry = ttk.Entry(input_frame, width=50)
        self.data_entry.grid(row=0, column=1, padx=5, sticky='ew')
        
        ttk.Label(input_frame, text="Divisore (binario):").grid(row=1, column=0, padx=5, sticky='w')
        self.divisor_entry = ttk.Entry(input_frame, width=50)
        self.divisor_entry.grid(row=1, column=1, padx=5, sticky='ew')
        
        self.calc_button = ttk.Button(input_frame, text="Calcola CRC", command=self.calcola)
        self.calc_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Frame risultati
        results_frame = ttk.Frame(self, padding=10)
        results_frame.grid(row=2, column=0, sticky='ew')
        
        ttk.Label(results_frame, text="Quoziente:").grid(row=0, column=0, padx=5, sticky='w')
        self.quotient_label = ttk.Label(results_frame, text="")
        self.quotient_label.grid(row=0, column=1, padx=5, sticky='w')
        
        ttk.Label(results_frame, text="Resto CRC:").grid(row=1, column=0, padx=5, sticky='w')
        self.crc_label = ttk.Label(results_frame, text="")
        self.crc_label.grid(row=1, column=1, padx=5, sticky='w')
        
        # Frame tabella
        table_frame = ttk.Frame(self)
        table_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        
        # Albero per visualizzazione passaggi
        self.tree = ttk.Treeview(table_frame, columns=('Passo', 'Dividendo', 'Divisore', 'XOR', 'Bit Quoziente', 'Nuovo Dividendo', 'Bit Aggiunto'), show='headings')
        
        # Configurazione colonne
        columns = [
            ('Passo', 50),
            ('Dividendo', 150),
            ('Divisore', 150),
            ('XOR', 200),
            ('Bit Quoziente', 100),
            ('Nuovo Dividendo', 150),
            ('Bit Aggiunto', 100)
        ]
        
        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
            
        # Scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

    def calcola(self):
        # Pulizia risultati precedenti
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        data = self.data_entry.get()
        divisor = self.divisor_entry.get()
        
        # Validazione input
        errori = []
        if not data or not divisor:
            errori.append("Inserire entrambi i campi")
        if len(data) < len(divisor):
            errori.append("Il messaggio deve essere più lungo del divisore")
        if any(c not in {'0', '1'} for c in data):
            errori.append("Il messaggio contiene caratteri non binari")
        if any(c not in {'0', '1'} for c in divisor):
            errori.append("Il divisore contiene caratteri non binari")
            
        if errori:
            messagebox.showerror("Errore", "\n".join(errori))
            return
            
        # Calcolo CRC
        try:
            quoziente, resto, passaggi = crc_division(data, divisor)
        except Exception as e:
            messagebox.showerror("Errore durante il calcolo", str(e))
            return
            
        # Popolazione tabella
        for p in passaggi:
            self.tree.insert('', 'end', values=(
                p['step'],
                p['current_dividend'],
                p['divisor_used'],
                p['xor_result'],
                p['quotient_bit'],
                p['new_dividend'],
                p['appended_bit']
            ))
            
        # Aggiornamento risultati
        self.quotient_label.config(text=quoziente)
        self.crc_label.config(text=resto)

if __name__ == "__main__":
    app = CRCGUI()
    app.mainloop()