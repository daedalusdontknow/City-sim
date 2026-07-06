<h1 align="center"> City Simulation </h1>

Eine dynamische, agentenbasierte Lebenssimulation in Python. Die Bewohner haben eigene Bedürfnisse, gehen Berufen nach, gründen Familien, vererben Vermögen und nutzen intelligentes A*-Pathfinding, um sich in der prozedural generierten Welt zu bewegen.

---

## Features

* **Smarte Wegfindung:** A*-Pathfinding zur kollisionsfreien Navigation um Gebäude herum (Häuser, Shops, Büros).
* **Komplexes Bedürfnis-System:** Dynamischer Stoffwechsel und Energieverbrauch – Agenten müssen arbeiten, essen und schlafen.
* **Wirtschaftskreislauf:** Ein funktionierendes System aus Gehalt, Ersparnissen, Einkäufen und dynamischem Taschengeld für die Kinder.
* **Lebenszyklus:** Altern, Heirat, Fortpflanzung (inklusive Cooldowns), Tod durch Altersschwäche oder Hunger sowie ein voll funktionierendes Vererbungssystem.
* **Live-Rendering:** Echtzeit-Visualisierung der Stadt und der berechneten Laufwege mit OpenCV und Pillow.

---

## Installation & Start

1. Klone dieses Repository.
2. Installiere die benötigten Abhängigkeiten:

   ```bash
   pip install opencv-python Pillow numpy
    ```
    ```bash
    python main.py
    ```
---

## Credits

### Namens-Datenbank

Die zufälligen Namen der Einwohner (`male.txt` & `female.txt`) basieren auf dem NLP-Namen-Corpus der Carnegie Mellon University. 

**Originaler Copyright-Hinweis:**

> You may use the lists of names for any purpose, so long as credit is given
> in any published work. You may also redistribute the list if you
> provide the recipients with a copy of this README file. The lists are
> not in the public domain (I retain the copyright on the lists) but are
> freely redistributable.
> If you have any additions to the lists of names, I would appreciate
> receiving them.
> My email address is mkant+@cs.cmu.edu.
> Mark Kantrowitz
> **Quelle:** [CMU AI NLP Corpora - Names](https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/)

### Verwendete Bibliotheken

* **OpenCV & NumPy:** Für das schnelle Echtzeit-Rendering der Simulation.
* **Pillow (PIL):** Für die Erstellung und das Zeichnen der grafischen Assets im Hintergrund.