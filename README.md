# verbeterdekaart
QGIS-32BT-verbeterdekaart is een QGIS plugin voor ondersteuning in het beheer van terugmeldingen. Hiermee kun je gemakkelijk WFS-lagen aanmaken voor de verschillende terugmeldservices, en je kunt de bijbehorende terugmeldviewers eenvoudig oproepen.

## Installatie
Middels de pluginbeheer omgeving kan de plugin geïnstalleerd worden volgens de gebruikelijke methode. De plugin kan eventueel als zipfile geïnstalleerd worden. De zipfile is beschikbaar via de Code-button die te vinden is op de github pagina. Vervolgens kun je de zipfile decomprimeren en het mapje verplaatsen naar je QGIS plugins directory. De plugins beheerdialoog kan dit voor je doen via de optie "Install from ZIP". Zie:  
https://docs.qgis.org/3.40/nl/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab

## Gebruik
Zorg dat de plugin op de juiste wijze is geïnstalleerd en op actief is gezet in de pluginbeheer omgeving. Als je de plugin succesvol geïnstalleerd en actief gemaakt hebt, zou er een toolbar moeten verschijnen met twee buttons:

<img width="99" height="41" alt="image" src="https://github.com/user-attachments/assets/a6e5733b-61c9-40a4-8f29-42837b4604a9" /></br>

De eerste button gebruik je om een WFS laag aan te maken voor één van de bekende terugmeldservices. Er zijn WFS services voor de BAG, de BGT, de BRT, 3DB en AERO. 

De tweede button gebruik je om een melding aan te maken via de webpagina van de bekende terugmeldviewers. Die viewers tonen een kaart. De schaal en locatie van de kaart zal overeenkomen met je QGIS werkblad van dat moment.


## De "WFS" button
De WFS button gebruik je om een WFS laag aan te maken waarin terugmeldingen getoond zullen worden van de gekozen registratie. In het kort:  
- Open een QGIS project met de kaart van Nederland. 
- Klik op de WFS button om een WFS laag toe te voegen,
- Kies de gewenste service en geef eventueel een bronhoudercode op,
- Klik OK om de keuze te bevestigen en de laag aan te maken. 

De laag zal bovenaan de legenda worden toegevoegd, en heeft een standaard opmaak die enigszins vergelijkbaar is met de bekende weergaves van de gekozen service. De opmaak kan uiteraard naar wens worden gewijzigd. Het is ook mogelijk om je eigen styling mee te geven aan elke nieuw aangemaakte laag, zie verderop onder Customisation. 


Als je op de button klikt, zal er een dialoogboxje verschijnen met twee opties. 

<img width="299" height="251" alt="image" src="https://github.com/user-attachments/assets/44a702a2-b79f-40dc-9dc7-1864888dbeb7" /><br/>

Optie 1 is een keuzemenu voor de gewenste registratie. Terugmeldingen zijn gekoppeld aan één van de bekende registraties, en voor elk type registratie is er een aparte WFS endpoint beschikbaar. Afhankelijk van welk type terugmeldingen je wilt zien, moet je dus allereerst de gewenste service kiezen:

<img width="309" height="254" alt="image" src="https://github.com/user-attachments/assets/eb8f3343-2815-4e96-a7fe-5c3077b9777b" /><br/>

Optie 2 is een optionele bronhoudercode. Bij het aanmaken van de laag kan eventueel een bronhoudercode-filter toegevoegd worden. Hiermee zorg je ervoor dat uitsluitend de meldingen voor een specifieke bronhouder worden opgevraagd. Dat scheelt in werklast voor de laag (en voor jezelf). 

<img width="306" height="265" alt="image" src="https://github.com/user-attachments/assets/b10db9de-292a-4540-92aa-5315ed97df14" /><br/>

>[!CAUTION]
>BELANGRIJK: De filtercode wordt per servicetype bepaald. Als je van servicetype wisselt, dan wisselt de code mee.  

Het filter gebruikt de PropertyIsLike methode met de volgende kenmerken:  
```<PropertyIsLike wildCard="*" singleChar="?" escapeChar="%">```  
Hiermee kun je bijvoorbeeld ook een WFS-laag maken met alleen de terugmeldingen voor alle provinciale bronhouders:  

<img width="303" height="255" alt="image" src="https://github.com/user-attachments/assets/8693c1c0-95d8-424b-b6da-6c14f3083dd1" /><br/>

Het filter kan overigens, indien gewenst, naderhand nog in QGIS worden aangepast via de laageigenschappen:

<img width="848" height="525" alt="image" src="https://github.com/user-attachments/assets/b1307165-a50c-47ce-92d9-7144e22585c8" /><br/>

  

## 
Open een QGIS project met de kaart van Nederland. 
Klik op de WFS button om een WFS laag toe te voegen,
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

