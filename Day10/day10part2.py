import itertools
from fractions import Fraction

# --- Gauß-Solver für rationale Zahlen ---
def solve_linear_system_subset(buttons, targets):
    """
    Löst Ax = b für eine Teilmenge von Knöpfen.
    Gibt die Summe der Drücke zurück, wenn eine gültige, 
    ganzzahlige, nicht-negative Lösung existiert.
    """
    num_vars = len(buttons)
    num_eqs = len(targets)
    
    # Matrix aufbauen: Zeilen = Gleichungen, Spalten = Knöpfe
    matrix = []
    for r in range(num_eqs):
        row = []
        for c in range(num_vars):
            if r in buttons[c]:
                row.append(Fraction(1, 1))
            else:
                row.append(Fraction(0, 1))
        row.append(Fraction(targets[r]))
        matrix.append(row)

    # Gauß-Elimination
    pivot_row = 0
    col = 0
    
    while pivot_row < num_eqs and col < num_vars:
        # Pivot suchen
        sel = -1
        for i in range(pivot_row, num_eqs):
            if matrix[i][col] != 0:
                sel = i
                break
        
        if sel == -1:
            col += 1
            continue

        # Tauschen
        matrix[pivot_row], matrix[sel] = matrix[sel], matrix[pivot_row]

        # Normieren
        pivot_val = matrix[pivot_row][col]
        for j in range(col, num_vars + 1):
            matrix[pivot_row][j] /= pivot_val

        # Eliminieren
        for i in range(num_eqs):
            if i != pivot_row:
                factor = matrix[i][col]
                for j in range(col, num_vars + 1):
                    matrix[i][j] -= factor * matrix[pivot_row][j]

        pivot_row += 1
        col += 1

    # Konsistenz prüfen (0 = nicht-0 ?)
    for i in range(num_eqs):
        row_is_zero = all(matrix[i][j] == 0 for j in range(num_vars))
        if row_is_zero and matrix[i][-1] != 0:
            return None # Unlösbar

    # Lösung auslesen (Rücksubstitution)
    solution = [Fraction(0, 1)] * num_vars
    for c in range(num_vars):
        found_row = -1
        for r in range(num_eqs):
            if matrix[r][c] == 1:
                # Prüfen ob Pivot
                is_pivot = True
                for r2 in range(num_eqs):
                    if r2 != r and matrix[r2][c] != 0:
                        is_pivot = False
                        break
                if is_pivot:
                    found_row = r
                    break
        
        if found_row != -1:
            solution[c] = matrix[found_row][-1]
        # Freie Variablen bleiben 0 (Basis-Lösung)

    # Validierung: Ganzzahlig und nicht-negativ?
    current_presses = 0
    for val in solution:
        if val.denominator != 1: # Muss Integer sein
            return None
        if val < 0: # Darf nicht negativ sein
            return None
        current_presses += int(val)

    # Probe: Stimmt die Summe wirklich?
    for r in range(num_eqs):
        check_sum = 0
        for c in range(num_vars):
            if r in buttons[c]:
                check_sum += solution[c]
        if check_sum != targets[r]:
            return None

    return current_presses

# --- Hauptlogik ---
def solve_machine_exhaustive(line, line_num):
    parts = line.strip().split(' ')
    target_part = ""
    all_buttons = []
    
    # Parsing
    for part in parts:
        if part.startswith('{'):
            target_part = part.replace('{', '').replace('}', '')
        elif part.startswith('('):
            btn_str = part.replace('(', '').replace(')', '')
            if btn_str:
                indices = [int(x) for x in btn_str.split(',')]
            else:
                indices = []
            all_buttons.append(indices)
            
    targets = [int(x) for x in target_part.split(',')]
    
    best_presses = float('inf')
    solution_found = False
    
    # WICHTIGE ÄNDERUNG: Wir probieren JEDE Menge an Knöpfen, von 1 bis ALLE.
    # Keine Limitierung mehr auf 'len(targets)'.
    max_k = len(all_buttons)
    
    for k in range(1, max_k + 1):
        # itertools.combinations geht alle möglichen Gruppen durch
        for btn_indices in itertools.combinations(range(len(all_buttons)), k):
            selected_buttons = [all_buttons[i] for i in btn_indices]
            
            result = solve_linear_system_subset(selected_buttons, targets)
            
            if result is not None:
                if result < best_presses:
                    best_presses = result
                    solution_found = True

    if not solution_found:
        # Warnung ausgeben, wenn für eine Maschine gar keine Lösung gefunden wird
        # (Das erklärt, warum dein Ergebnis zu niedrig war - hier wurde wohl 0 addiert)
        print(f"[WARNUNG] Zeile {line_num}: Keine Lösung gefunden! (Wird als 0 gezählt)")
        return 0

    return best_presses

def solve_factory_final(fname):
    if len(fname) < 1:
        fname = '/workspaces/AdventofCode/Day10/input.txt' 
        
    total_presses = 0
    try:
        with open(fname, 'r') as f:
            lines = f.readlines()
        
        print("Starte vollständige Berechnung (kann kurz dauern)...")
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line: continue
            
            presses = solve_machine_exhaustive(line, i + 1)
            total_presses += presses
            
            # Fortschrittsanzeige alle 100 Zeilen
            if (i + 1) % 100 == 0:
                print(f"... {i + 1} Maschinen verarbeitet.")
            
    except FileNotFoundError:
        print(f"Fehler: Datei '{fname}' nicht gefunden.")
        return

    print("-" * 30)
    print(f"NEUES ERGEBNIS: {total_presses}")
    print("-" * 30)

if __name__ == "__main__":
    fname = input('Dateinamen eingeben (Enter für Standard): ')
    solve_factory_final(fname)