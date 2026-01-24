# verbeterdekaart
QGIS-32BT-verbeterdekaart is een QGIS plugin voor ondersteuning in het beheer van terugmeldingen. Hiermee kun je gemakkelijk WFS-lagen aanmaken voor de verschillende terugmeldservices, en je kunt de bijbehorende terugmeldviewers eenvoudig oproepen.

## Installatie
Middels de pluginbeheer omgeving kan de plugin geïnstalleerd worden volgens de gebruikelijke methode. De plugin kan eventueel ook van zipfile geïnstalleerd worden. De zipfile is beschikbaar via de Code-button die te vinden is op de github pagina. Zie:  
https://docs.qgis.org/3.40/nl/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab

## Gebruik
Zorg dat de plugin op de juiste wijze is geïnstalleerd en op actief is gezet in de pluginbeheer omgeving. Als je de plugin succesvol hebt geïnstalleerd, zou er een toolbar moeten verschijnen met twee buttons:

<img width="99" height="41" alt="image" src="https://github.com/user-attachments/assets/a6e5733b-61c9-40a4-8f29-42837b4604a9" /></br>

De eerste knop gebruik je om een WFS laag aan te maken voor één van de bekende terugmeldservices. Er zijn WFS services voor de BAG, de BGT, de BRT, 3DB en AERO. 

De tweede knop gebruik je om een melding aan te maken via de webpagina van de bekende terugmeldviewers. Die viewers tonen een kaart. De schaal en locatie van de kaart zal overeenkomen met je QGIS werkblad van dat moment.


## Knop 1: De "WFS" knop
De WFS button is bedoeld om een WFS laag aan te maken waarin terugmeldingen getoond zullen worden van de gekozen registratie. In het kort:  
- Open een QGIS project met de kaart van Nederland. 
- Klik op de WFS button om een WFS laag toe te voegen,
- Kies de gewenste service en geef eventueel een bronhoudercode op,
- Klik OK om de keuze te bevestigen en de laag aan te maken. 
##
**De WFS laag**  
De laag zal bovenaan de legenda worden toegevoegd, en heeft een standaard opmaak die enigszins vergelijkbaar is met de bekende weergaves van de gekozen service. De opmaak kan uiteraard naar wens worden gewijzigd. Het is ook mogelijk om je eigen styling mee te geven aan elke nieuw aangemaakte laag, zie de styling voetnoot.[^1] 

<img width="1014" height="485" alt="image" src="https://github.com/user-attachments/assets/7816f20b-a9b0-47ba-8ed9-c01c5046572d" /><br/>

## 
**De WFS opties**  
Als je op de button klikt, zal er een dialoogboxje verschijnen met twee opties: servicetype en bronhoudercode. 

<img width="304" height="248" alt="image" src="https://github.com/user-attachments/assets/5fd68406-b79e-4328-94de-ab133419f09a" /><br/>

**Servicetype**  
Servicetype is een keuzemenu voor de gewenste registratie. Terugmeldingen zijn gekoppeld aan één van de bekende registraties, en voor elk type registratie is er een aparte WFS service endpoint beschikbaar. Afhankelijk van welk type terugmeldingen je wilt zien, moet je dus allereerst de gewenste service kiezen:

<img width="311" height="250" alt="image" src="https://github.com/user-attachments/assets/85c5694f-6f1c-4f59-8e14-ed0c61107f82" /><br/>

Sinds kort (Januari 2026) zijn er ook OGC-compatible endpoints beschikbaar. Indien je deze wilt gebruiken, kun je de checkbox "ogc" aanvinken. Dit heeft wel enige beperkingen, zie notitie bij Bronhoudercode.

**Bronhoudercode**  
Bronhoudercode is een optionele filtercode. Bij het aanmaken van de laag kan eventueel een bronhoudercode-filter toegevoegd worden. Hiermee zorg je ervoor dat uitsluitend de meldingen voor een specifieke bronhouder worden opgevraagd. Dat scheelt in werklast voor de laag (en voor jezelf). 

<img width="305" height="250" alt="image" src="https://github.com/user-attachments/assets/d9d7904b-2722-42d0-bd93-8c2d618e5652" /><br/>

>[!CAUTION]
>BELANGRIJK: De filtercode wordt per servicetype bepaald. Als je van servicetype wisselt, dan wisselt de code mee.  

Voor de normale WFS service endpoints, wordt het filter toegevoegd als QGIS expression. De plugin ondersteunt hierbij ook wildcard-karakters:  
- "%" of "*" betekent "één of meer willekeurige karakters"  
- "_" of "?" betekent "precies één willekeurig karakter"

Hiermee kun je bijvoorbeeld ook een WFS-laag maken met alleen de terugmeldingen voor alle provinciale bronhouders:  

<img width="305" height="250" alt="image" src="https://github.com/user-attachments/assets/d03fe23a-28ea-4c15-b7f9-e89b6b9c64d8" /><br/>

Het filter kan overigens, indien gewenst, naderhand nog in QGIS worden aangepast via de laageigenschappen:

<img width="908" height="443" alt="image" src="https://github.com/user-attachments/assets/97988260-16a5-415d-aca9-af3c00dec630" /><br/>

  

## Knop 2: De "VDK" knop  
De VDK knop is bedoeld om de verbeterdekaart webpagina te openen. Er zijn drie verschillende verbeterdekaart-webpagina's afhankelijk van welke registratie je wilt verbeteren.  
- Voor BAG meldingen is er de BAGViewer: https://bagviewer.kadaster.nl
- Voor BGT, BRT, en 3DB meldingen is er de verbeterdekaart webpagina: https://www.verbeterdekaart.nl
- Voor AERO meldingen is er de verbeterdeluchtvaartkaart variant: https://www.verbeterdeluchtvaartkaart.nl
 
Al deze pagina's tonen een kaart. Deze kaart zal door de VDK plugin zodanig worden aangeroepen dat de weergaveschaal en locatie gelijk zou moeten zijn met je huidige QGIS weergave. Je kunt de VDK knop gemakkelijk instellen op één van de drie doelpagina's. Door de knop kortstondig ingedrukt te houden zul je zien dat er een menu verschijnt met de 3 opties voor de landingspagina. De geselecteerde doelpagina is zichtbaar in vet lettertype met een vinkje ervoor. 

**Opties submenu**  
<img width="275" height="143" alt="image" src="https://github.com/user-attachments/assets/efbd9bb0-036d-4586-a97d-4ea960db6011" />

>[!NOTE]
>Er kunnen eventueel schalingsverschillen zijn tussen je QGIS omgeving en je default webbrowser, met name Linux op een chromebook kan verschillen vertonen vanwege de Wayland graphicsdriver backend. De plugin heeft een setting om dit te compenseren. Zie de opties onder het volgende hoofdstukje.

## Knop 3: De rechter muisknop
Een alternatieve manier om de viewerpagina te openen is de verbeterdekaart-contextmenu optie. Klik met de rechtermuisknop op de kaart en selecteer een optie uit het verbeterdekaart menu. Het verbeterdekaart menu toont een lijst met drie acties:  
1. Voorkeuren...
2. Kopieer locatie
3. Open webpagina

**Voorkeuren...**  
Met deze optie kun je voorkeuren opgeven voor de plugin. Er is één optie: **schalingspercentage**.  
Bij het openen van de verbeterdekaart website zal de plugin de huidige locatie en schaal van QGIS overnemen. Het kan echter zijn dat de verbeterdekaart website dan alsnog een afwijkende weergave geeft van de betreffende locatie. Om dit te synchroniseren, kun je een schalingspercentage opgeven. Waardes hoger dan 100% zullen de verbeterdekaart representatie vergroten.

**Kopieer locatie**  
Deze optie kopieert de huidige locatie en schaal als URL naar de clipboard in het format voor de gekozen registratie. Dit kun je gebruiken om een locatie te versturen naar een andere gebruiker.

**Open webpagina**  
Bij deze optie wordt de default browser geactiveerd met de verbeterdekaart URL voor de huidige QGIS locatie en schaal. In je browser kun je vervolgens een melding aanmaken volgens de stappen van de betreffende verbeterdekaart website.

## Werkmethodiek  
Voor bronhouders is het van belang om regelmatig te controleren of er binnengekomen meldingen zijn. Meldingen moeten binnen 5 werkdagen in onderzoek worden genomen, dus ten minste éénmaal per week is sterk aan te raden. Met de verbeterdekaart toolbar kun je deze klus snel en efficient uitvoeren:

- Gebruik de "WFS" knop om een nieuwe laag aan te maken voor meldingen met de gewenste bronhoudercode.
- Met de rechtermuisknop klik je vervolgens op de subcategorie "Nieuw". 
- In het menu kies je dan de optie "Objecten selecteren".

<img width="549" height="254" alt="image" src="https://github.com/user-attachments/assets/3e35fa55-63dd-4914-a3c9-02340b40a6d3" /><br/>

Alle nieuw binnengekomen meldingen zijn nu geselecteerd. Met de **QGIS-32BT-Feature-Navigation-Toolbar** kun je vervolgens de selectie gemakkelijk één-voor-één langsgaan om de meldingen te beoordelen en te bepalen hoe ze verder verwerkt moeten worden.  

<img width="849" height="270" alt="image" src="https://github.com/user-attachments/assets/7e8764e7-3124-4e10-8b84-0c00cd3d2153" /><br/>


[^1]:De styling van de aangemaakte WFS laag wordt bepaald door een qml file. Als je de standaardstyling vanuit de plugin permanent wilt wijzigen, dan kun je de interne qml file vervangen door een eigen versie. Hiervoor moet je allereerst op zoek naar de plugin folder van QGIS. Hoe je die vindt, kun je in de QGIS handleiding lezen. Vervolgens ga je naar de verbeterdekaart-plugin folder. Hierin zoek je naar een mapje "controllers/subcontrollers/qml". De file "bgt.qml" moet je dan vervangen door een eigen versie. 
