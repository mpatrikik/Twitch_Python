It is a simple Python script, which is checking the selected channel streaming or not, if yes and when it's finished, the PC automatically shut down.

Futtatás előtt a terminálban látni kell a "(.venv)" feliratot, ha nincs: venv\Scripts\activate

Konzolon bekéri a csatorna nevét, ezt megvizsgálva kapunk egy üzenetet a konzolra, hogy streamel-e vagy sem. Ha igen akkor addig fut a program amíg a stream véget nem ér. Ha vége a streamnek, tehát offline a csatorna akkor bezárja a chrome-ot és kiírja a konzolra hogy vége a streamnek, majd feldob egy kis ablakot a rendszer, hogy ki szeretném-e kapcsolni a gépet, ha a nemre kattintok akkor bezáródik a kis ablak és a script leáll, ha az igenre kattintok akkor pár másodperc mulva leáll a script és be is zárja a pycharmot.