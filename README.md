# Fonetica

**Un carattere tipografico per distinguere le vocali accentate a colpo d’occhio.**

**Nome della famiglia:** Fonetica  
**Autore delle modifiche:** Davide Perillo  
**Versione:** 1.0.0 — 21 novembre 2026  
**Licenza:** SIL Open Font License 1.1

Fonetica è una personalizzazione di **Atkinson Hyperlegible** (versione 1.02), il carattere originariamente realizzato per il Braille Institute of America. La versione Fonetica è stata adattata e pubblicata con un nuovo nome per evidenziare la grafia delle vocali italiane accentate.

## Cosa cambia

| Carattere | Disegno nel font |
| --- | --- |
| **è** / **ò** | Corpo della lettera rimpicciolito a circa il 67,5% dell’originale; accento grave ridotto e riposizionato |
| **é** / **ó** | Corpo della lettera ingrandito a circa il 126,5% dell’originale; accento acuto ingrandito e riposizionato |
| Lettere non modificate, maiuscole, cifre | Mantengono il disegno del carattere di partenza |

**Importante:** nella terminologia fonetica italiana, **è/ò** sono normalmente **aperte** e **é/ó** sono **chiuse**. Le modifiche visive di Fonetica riguardano la forma dei caratteri e non la pronuncia automaticamente. Il font **non trascrive né corregge** un testo: per visualizzare le distinzioni il testo deve contenere i caratteri accentati corretti.

## Scaricare e installare

### Windows
1. Estrai lo ZIP.
2. Apri la cartella `Fonts/OTF`.
3. Seleziona i quattro file `.otf` e scegli **Installa** dal menu del tasto destro.
4. Riavvia l’applicazione di scrittura e scegli **Fonetica** nella lista dei font.

### macOS
Apri ciascun file `.otf` in `Fonts/OTF` con **Libro Font** e scegli **Installa**.

### Linux
Copia i `.otf` in `~/.local/share/fonts/` e aggiorna la cache con `fc-cache -f`.

### Siti web
Nella cartella `Fonts/WOFF2` trovi i quattro font compressi per il web; il file `Web/esempio.html` fornisce un esempio di integrazione CSS.

## File inclusi

- `Fonts/OTF/`: Regular, Bold, Italic, Bold Italic, pronti per l’installazione
- `Fonts/WOFF2/`: gli stessi stili per siti web e web app
- `Preview/Fonetica_Preview.png`: anteprima grafica del font
- `Web/esempio.html`: dimostrazione HTML/CSS funzionante anche offline
- `Source/build_fonetica.py`: sorgente delle modifiche dei glifi e dei metadati
- `OFL.txt`: licenza completa SIL OFL 1.1
- `AUTHORS.md`: attribuzioni e riconoscimenti
- `CHANGELOG.md`: cronologia delle versioni

## Per gli sviluppatori

Tutti i file `.otf` contengono internamente il nome della famiglia **Fonetica**, lo stile specifico, il nome dell’autore **Davide Perillo**, l'indicazione della licenza e il copyright originale. È raccomandata la normalizzazione **Unicode NFC** del testo per visualizzare i quattro caratteri precomposti `è`, `ò`, `é`, `ó` con i glifi personalizzati. Le sequenze Unicode con accenti combinanti non sono automaticamente sostituite dai medesimi glifi in tutte le applicazioni.

Per ricompilare da Atkinson Hyperlegible 1.02, installa `fonttools` e `brotli`, scarica i quattro `.otf` originali, poi esegui:

```bash
python Source/build_fonetica.py --sources /percorso/atkinson-1.02 --output ./Fonetica
```

Fonte del carattere originario: https://github.com/googlefonts/atkinson-hyperlegible

## Licenza e attribuzioni

**Fonetica — modifiche e personalizzazione: Davide Perillo (2026).**  
**Disegno originale Atkinson Hyperlegible:** Copyright 2020 Braille Institute of America, Inc.; sviluppato con Applied Design Works.

Fonetica è un’opera derivata di Atkinson Hyperlegible distribuita con il nuovo nome **Fonetica** sotto la **SIL Open Font License 1.1**, come la base originale. La licenza permette utilizzo, modifica e redistribuzione secondo le condizioni esplicitate in `OFL.txt`. La distribuzione non implica alcun sostegno o affiliazione da parte del Braille Institute o dei designer originali.

---

**English:** Fonetica is an Atkinson Hyperlegible-based typeface adaptation by Davide Perillo. Lowercase `è` and `ò` are compact, while `é` and `ó` are enlarged. Four OTF and four WOFF2 styles are included. Released under the SIL Open Font License 1.1, with original-design attribution preserved. See `OFL.txt` and `AUTHORS.md`.
