# verbeterdekaart
QGIS-32BT-verbeterdekaart is een QGIS plugin voor ondersteuning in het beheer van terugmeldingen. Hiermee kun je gemakkelijk WFS-lagen aanmaken voor de verschillende terugmeldservices, en je kunt de bijbehorende terugmeldviewers eenvoudig oproepen.  

1. [Installatie](#installatie)
2. [Gebruik](#gebruik)
3. [Knop 1: De "WFS" knop](#knop-1-de-wfs-knop)
4. [Knop 2: De "VDK" knop](#knop-2-de-vdk-knop)
5. [Knop 3: De rechter muis knop](#knop-3-de-rechter-muisknop)

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
### De WFS laag  
De laag zal bovenaan de legenda worden toegevoegd, en heeft een standaard opmaak die enigszins vergelijkbaar is met de bekende weergaves van de gekozen service. De opmaak kan uiteraard naar wens worden gewijzigd. Het is ook mogelijk om je eigen styling mee te geven aan elke nieuw aangemaakte laag, zie de styling voetnoot.[^1] 

<img width="1014" height="485" alt="image" src="https://github.com/user-attachments/assets/7816f20b-a9b0-47ba-8ed9-c01c5046572d" /><br/>

## 
### De WFS opties  
Als je op de button klikt, zal er een dialoogboxje verschijnen met aantal opties, onderverdeelt in WFS Endpoint en Styling. 

<img width="328" height="406" alt="vdk23_styling_nl" src="https://github.com/user-attachments/assets/3916c652-8ecd-4795-898c-03fc11dcd7aa" /><br/>

**Servicetype**  
Servicetype is een keuzemenu voor de gewenste registratie. Terugmeldingen zijn gekoppeld aan één van de bekende registraties, en voor elk type registratie is er een aparte WFS service endpoint beschikbaar. Afhankelijk van welk type terugmeldingen je wilt zien, moet je dus allereerst de gewenste service kiezen:

<img width="344" height="409" alt="vdk23_wfs_servicetypes" src="https://github.com/user-attachments/assets/a7c1c031-7bd5-43d3-91fa-d4b8057c18c0" /><br/>

Sinds kort (Januari 2026) zijn er ook OGC-compatible endpoints beschikbaar. Indien je deze wilt gebruiken, kun je de checkbox "ogc" aanvinken. Dit heeft wel enige beperkingen, zie de [waarschuwing](#FILTER_WARNING) bij Bronhoudercode.

**Bronhoudercode**  
Bronhoudercode is een optionele filtercode. Bij het aanmaken van de laag kan eventueel een bronhoudercode-filter toegevoegd worden. Hiermee zorg je ervoor dat uitsluitend de meldingen voor een specifieke bronhouder worden opgevraagd. Dat scheelt in werklast voor de laag (en voor jezelf).  
>[!NOTE]
>LET OP: De filtercode wordt per servicetype bepaald. Als je van servicetype wisselt, dan wisselt de code mee.  

<img width="347" height="413" alt="vdk23_wfs_bhc" src="https://github.com/user-attachments/assets/42785988-52d1-44bd-84d8-63dddd809375" /><br/>

Voor de normale WFS service endpoints, wordt het filter toegevoegd als QGIS expression. De plugin ondersteunt ook wildcard-karakters. Hiermee kun je bijvoorbeeld een WFS-laag maken met alleen de terugmeldingen voor alle provinciale bronhouders. 
- "%" of "*" betekent "één of meer willekeurige karakters"  
- "_" of "?" betekent "precies één willekeurig karakter"

<img width="352" height="420" alt="vdk23_wfs_bhc2" src="https://github.com/user-attachments/assets/d5876602-8636-40d9-a169-612f0d42f573" /><br/>

Het filter kan overigens, indien gewenst, naderhand nog in QGIS worden aangepast via de laageigenschappen:

<img width="908" height="443" alt="image" src="https://github.com/user-attachments/assets/97988260-16a5-415d-aca9-af3c00dec630" /><br/>

<a name="FILTER_WARNING"></a>
>[!WARNING]
>**WAARSCHUWING**: De OGC-compatible endpoints staan op dit moment (januari 2026) nog geen ogc-filters toe. Als alternatief voor server-side filtering, zijn door PDOK "gesloten" parameters in de url bedacht. Dit betekent dat er voor OGC-endpoints **geen** QGIS expression aangemaakt wordt. De plugin past in plaats daarvan de url aan voor service-side filtering. Wildcard-filters worden door PDOK niet ondersteund. Deze worden door de plugin wel gewoon als QGIS expression beschikbaar gemaakt, maar deze worden door QGIS alleen client-side toegepast, dus op je eigen computer nadat eerst **alle** terugmeldingen zijn opgehaald.  

**Styling**  
De WFS laag wordt aangemaakt met een toepasselijke styling van symbolen en labels. De symbolen zijn gegroepeerd naar de status van de terugmelding. De groepen zijn terug te vinden in de legenda van de laag. De statusindicaties zijn beschikbaar in 3 smaakjes. De "Standaard"-styling optie is voor de bekende namen zoals gebruikt op de websites en andere externe uitingen. "Kort" is voor de weergave van de interne statusCode, en "Aangepast" is een beheerdersweergave om eventueel te synchroniseren met andere plugins.  


## Knop 2: De "VDK" knop  
De VDK knop is bedoeld om de verbeterdekaart webpagina te openen. Er zijn drie verschillende verbeterdekaart-webpagina's afhankelijk van welke registratie je wilt verbeteren.  
- Voor BAG meldingen is er de BAGViewer: https://bagviewer.kadaster.nl
- Voor BGT, BRT, en 3DB meldingen is er de verbeterdekaart webpagina: https://www.verbeterdekaart.nl
- Voor AERO meldingen is er de verbeterdeluchtvaartkaart variant: https://www.verbeterdeluchtvaartkaart.nl  

<img width="310" height="152" alt="vdk23_menu" src="https://github.com/user-attachments/assets/08a9f40a-f5ac-4faf-af95-64e809769041" /><br/>

**Ad hoc modus vs Focus modus**  
De knop kan op twee manieren gebruikt worden. Allereerst in de Ad hoc modus, waarbij je altijd een keuzemenu krijgt om de gewenste registratie te kiezen voordat de betreffende webpagina wordt geopend in je browser. Daarnaast is er de focus modus, waarbij de knop direct de voorgeselecteerde webpagina zal openen in je browser. Deze laatste modus is handig als je strikt binnen één registratie werkt. Bij de voorkeuren kun je instellen in welke modus je wilt werken. 

## Knop 3: De rechter muisknop  
Een alternatieve manier om de viewerpagina te openen is de verbeterdekaart-contextmenu optie. Klik met de rechtermuisknop op de kaart en selecteer een optie uit het verbeterdekaart menu.  

<img width="381" height="116" alt="image" src="https://github.com/user-attachments/assets/3715a742-e9ed-4202-a384-59956acd6435" /><br/>  

Het verbeterdekaart menu toont een lijst met drie acties:  
1. [Voorkeuren...](#1-voorkeuren)
2. [Kopieer locatie](#2-kopieer-locatie)
3. [Open webpagina](#3-open-webpagina)

### 1. Voorkeuren...    
Met deze optie kun je voorkeuren opgeven voor de plugin. Er zal een dialoogbox verschijnen met twee opties.  

<img width="467" height="441" alt="vdk23_settings" src="https://github.com/user-attachments/assets/1ef03de9-1264-42ff-99b8-997481b52067" /><br />  

Optie 1: ***Werkbalk knop***  
De instelling voor de werkbalk knop bepaalt hoe je de gewenste langingspagina opent. Dit is afhankelijk van je werkmodus. Je kunt in -*Ad hoc* modus werken. In dat geval krijg je het keuzemenu altijd eerst te zien als je op de werkbalk knop drukt. Je kunt ook in *Focus* modus werken. Dan kies je hier alvast een registratie, en zal de werkbalk knop direct de betreffende landingspagina openen. Door de knop kortstondig ingedrukt te houden, kun je alsnog makkelijk wisselen tussen langingspagina's.  

Optie 2: ***schalingspercentage***.  
Bij het openen van de verbeterdekaart website zal de plugin de huidige locatie en schaal van QGIS overnemen. Het kan echter zijn dat de verbeterdekaart website dan alsnog een afwijkende weergave geeft van de betreffende locatie. Om dit te synchroniseren, kun je een schalingspercentage opgeven. Waardes hoger dan 100% zullen de verbeterdekaart weergave vergroten.

### 2. Kopieer locatie  
Deze optie kopieert de huidige locatie en schaal als URL naar de clipboard in het format voor de gekozen registratie. Dit kun je gebruiken om een locatie te versturen naar een andere gebruiker.

### 3. Open webpagina  
Bij deze optie wordt de default browser geactiveerd met de verbeterdekaart URL voor de huidige QGIS locatie en schaal. In je browser kun je vervolgens een melding aanmaken volgens de stappen van de betreffende verbeterdekaart website.

## Werkmethodiek  
Voor bronhouders is het van belang om regelmatig te controleren of er binnengekomen meldingen zijn. Meldingen moeten binnen 5 werkdagen in onderzoek worden genomen, dus ten minste éénmaal per week is sterk aan te raden. Met de verbeterdekaart toolbar kun je deze klus snel en efficient uitvoeren:

- Gebruik de "WFS" knop om een nieuwe laag aan te maken voor meldingen met de gewenste bronhoudercode.
- Met de rechtermuisknop klik je vervolgens op de subcategorie "Nieuw". 
- In het menu kies je dan de optie "Objecten selecteren".

<img width="549" height="254" alt="image" src="https://github.com/user-attachments/assets/3e35fa55-63dd-4914-a3c9-02340b40a6d3" /><br/>

Alle nieuw binnengekomen meldingen zijn nu geselecteerd. Met de **QGIS-32BT-Feature-Navigation-Toolbar** kun je vervolgens de selectie gemakkelijk één-voor-één langsgaan om de meldingen te beoordelen en te bepalen hoe ze verder verwerkt moeten worden.  

<img width="849" height="270" alt="image" src="https://github.com/user-attachments/assets/7e8764e7-3124-4e10-8b84-0c00cd3d2153" /><br/>


[^1]: De styling van de aangemaakte WFS laag wordt bepaald door een qml file. Als je de standaardstyling vanuit de plugin permanent wilt wijzigen, dan kun je de interne qml files vervangen door een eigen versie. Hiervoor moet je allereerst op zoek naar de plugin folder van QGIS. Hoe je die vindt, kun je in de QGIS handleiding lezen. Vervolgens ga je naar de verbeterdekaart-plugin folder. Hierin zoek je naar een mapje "controllers/subcontrollers/qml". Vervang vervolgens de gewenste styling-optie door je eigen file.
