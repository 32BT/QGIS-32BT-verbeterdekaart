# verbeterdekaart
QGIS-32BT-verbeterdekaart is een QGIS plugin voor ondersteuning in het beheer van terugmeldingen. Hiermee kun je gemakkelijk WFS-lagen aanmaken voor de verschillende terugmeldservices, en je kunt de bijbehorende terugmeldviewers eenvoudig oproepen.

## Installatie
Middels de pluginbeheer omgeving kan de plugin geïnstalleerd worden volgens de gebruikelijke methode. De plugin kan eventueel als zipfile geïnstalleerd worden. De zipfile is beschikbaar via de Code-button die te vinden is op de github pagina. Vervolgens kun je de zipfile decomprimeren en het mapje verplaatsen naar je QGIS plugins directory. De plugins beheerdialoog kan dit voor je doen via de optie "Install from ZIP". Zie:  
https://docs.qgis.org/3.40/nl/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab

## Gebruik
Zorg dat de plugin op de juiste wijze is geïnstalleerd en op actief is gezet in de pluginbeheer omgeving. Als je de plugin succesvol geïnstalleerd en actief gemaakt hebt, zou er een toolbar moeten verschijnen met twee buttons:

ophalen, aanmaken?

De eerste button gebruik je om een WFS laag aan te maken voor één van de bekende terugmeldservices. Er zijn WFS services voor de BAG, de BGT, de BRT, 3DB en AERO. 

De tweede button gebruik je om een melding aan te maken via de webpagina van de bekende terugmeldviewers. Die viewers tonen een kaart. De schaal en locatie van de kaart zal overeenkomen met je QGIS werkblad van dat moment.


## De "Ophalen" button
De ... button gebruik je om een WFS laag aan te maken. Als je op de button klikt, zal er een dialoogboxje verschijnen met twee opties. Allereerst kun je de gewenste service kiezen:

En bij het aanmaken van de laag kan eventueel een bronhoudercode-filter toegevoegd worden. Hiermee zorg je ervoor dat uitsluitend de meldingen voor een specifieke bronhouder worden opgevraagd. Dat scheelt in werklast voor de laag. Het filter kan, indien gewenst, naderhand nog worden aangepast in QGIS.



Open een QGIS project met de kaart van Nederland. 
Klik op de ... button om een WFS laag aan te maken,
Kies de gewenste service en geef eventueel een bronhoudercode op,
Klik OK om de keuze te bevestigen en de laag aan te maken. 

De laag zal bovenaan de legenda worden toegevoegd, en heeft een standaard opmaak die enigszins vergelijkbaar is met de bekende weergaves van de gekozen service. De opmaak kan uiteraard naar wens worden gewijzigd. Het is ook mogelijk om je eigen styling mee te geven aan elke nieuw aangemaakte laag, zie verderop onder Customisation. 




Klik met de rechtermuisknop op de kaart en selecteer een optie uit het verbeterdekaart menu. Het verbeterdekaart menu toont een lijst met drie opties:  
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

