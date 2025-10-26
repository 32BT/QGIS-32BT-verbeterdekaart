# verbeterdekaart
QGIS plugin voor het eenvoudig openen van verbeterdekaart.nl vanuit de QGIS applicatie

## Installatie
Via de Code-button die beschikbaar is op de github pagina kun je de code als zipfile downloaden.  
Vervolgens kun je de zipfile decomprimeren en het mapje verplaatsen naar je QGIS plugins directory.  
De plugins beheerdialoog kan dit voor je doen via de optie "Install from ZIP". Zie:  
https://docs.qgis.org/3.40/nl/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab

## Gebruik
Zorg dat de plugin op de juiste wijze is geïnstalleerd en op actief is gezet in de pluginbeheer omgeving. 

Open een QGIS project met de kaart van Nederland. Klik met de rechtermuisknop op de kaart en selecteer een optie uit het verbeterdekaart menu. Het verbeterdekaart menu toont een lijst met drie opties:  
1. Voorkeuren...
2. Kopieer locatie
3. Melding aanmaken...

**Voorkeuren...**  
Met deze optie kun je voorkeuren opgeven voor de plugin. Er is één optie: **schalingspercentage**.  
Bij het openen van de verbeterdekaart website zal de plugin de huidige locatie en schaal van QGIS overnemen. Het kan echter zijn dat de verbeterdekaart website dan een kleinere weergave geeft van de betreffende locatie. Om dit te synchroniseren, kun je een schalingspercentage opgeven. Waardes hoger dan 100% zullen de verbeterdekaart representatie vergroten.

**Kopieer locatie**  
Deze optie kopieert de huidige locatie en schaal als verbeterdekaart URL naar de clipboard. Dit kun je gebruiken om een locatie te versturen naar een andere gebruiker.

**Melding aanmaken...**  
Bij deze optie wordt de default browser geactiveerd met de verbeterdekaart URL voor de huidige QGIS locatie en schaal. In je browser kun je vervolgens een melding aanmaken volgens de stappen van de verbeterdekaart website.

