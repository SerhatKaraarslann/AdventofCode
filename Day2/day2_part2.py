def solve_problem(arr):
    total_sum = 0  # Besser nicht 'sum' nennen, da sum() eine Python-Funktion ist
    
    for i in arr:
        # strip() entfernt Leerzeichen/Zeilenumbrüche, falls vorhanden
        nums = i.strip().split('-') 
        start = int(nums[0])
        end = int(nums[1])

        for num in range(start, end + 1):
            number_text = str(num)  # Variable umbenannt
            length = len(number_text)
            
            is_invalid = False

            # Wir testen Musterlängen (n)
            for n in range(1, length // 2 + 1):
                
                # Wenn die Länge nicht glatt teilbar ist, überspringen
                if length % n != 0:
                    continue
                
                muster = number_text[:n]
                anzahl = length // n
                
                # Hier 'test_string' statt 'str' benutzen
                test_string = muster * anzahl
                
                # WICHTIG: Diese Prüfung muss IN der Schleife sein (eingerückt!)
                if test_string == number_text:
                    is_invalid = True
                    break  # Sobald wir ein Muster finden, aufhören zu suchen

            if is_invalid:
                total_sum += num
        
    return total_sum

# Datei einlesen
# Pfad ggf. anpassen
with open('/workspaces/AdventofCode/Day2/input.txt') as f:
    content = f.read()
    # strip() ist wichtig, falls am Ende der Datei eine leere Zeile ist
    numbers = content.strip().split(',')
    
    total = solve_problem(numbers)
    print('Total:', total)