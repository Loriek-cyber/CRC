def xor(a, b):
    """Esegue l'operazione XOR tra due stringhe binarie della stessa lunghezza."""
    return ''.join('0' if bit_a == bit_b else '1' for bit_a, bit_b in zip(a, b))

def crc_division(dividend, divisor):
    """Esegue la divisione binaria XOR per calcolare il quoziente e il resto (CRC)."""
    # Lunghezze
    dividend_len = len(dividend)
    divisor_len = len(divisor)
    
    # Aggiunta di zeri per l'operazione
    temp_dividend = dividend[:divisor_len]
    quotient = ''
    
    for i in range(divisor_len, dividend_len + 1):
        if temp_dividend[0] == '1':
            quotient += '1'
            temp_dividend = xor(temp_dividend, divisor)[1:]  # XOR e shift
        else:
            quotient += '0'
            temp_dividend = xor(temp_dividend, '0' * divisor_len)[1:]
        
        if i < dividend_len:
            temp_dividend += dividend[i]
    
    return quotient, temp_dividend  # Quoziente e resto (CRC)

# Esempio di utilizzo
data = input("Inserire il messaggio: ")  # Messaggio con zeri aggiunti
polynomial = input("inserire il divisore: ")  # Polinomio generatore
quotient, crc_remainder = crc_division(data, polynomial)

print(f"Quoziente: {quotient}")
print(f"CRC (Resto): {crc_remainder}")
