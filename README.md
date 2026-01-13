# verbeterdekaart
QGIS-32BT-verbeterdekaart is een QGIS plugin voor ondersteuning in het beheer van terugmeldingen. Hiermee kun je gemakkelijk WFS-lagen aanmaken voor de verschillende terugmeldservices, en je kunt de bijbehorende terugmeldviewers eenvoudig oproepen.

## Installatie
Middels de pluginbeheer omgeving kan de plugin geïnstalleerd worden volgens de gebruikelijke methode. De plugin kan eventueel als zipfile geïnstalleerd worden. De zipfile is beschikbaar via de Code-button die te vinden is op de github pagina. Vervolgens kun je de zipfile decomprimeren en het mapje verplaatsen naar je QGIS plugins directory. De plugins beheerdialoog kan dit voor je doen via de optie "Install from ZIP". Zie:  
https://docs.qgis.org/3.40/nl/docs/user_manual/plugins/plugins.html#the-install-from-zip-tab

## Gebruik
Zorg dat de plugin op de juiste wijze is geïnstalleerd en op actief is gezet in de pluginbeheer omgeving. Als je de plugin succesvol geïnstalleerd en actief gemaakt hebt, zou er een toolbar moeten verschijnen met twee buttons:

<img width="99" height="41" alt="image" src="https://github.com/user-attachments/assets/a6e5733b-61c9-40a4-8f29-42837b4604a9" /></br>

De eerste knop gebruik je om een WFS laag aan te maken voor één van de bekende terugmeldservices. Er zijn WFS services voor de BAG, de BGT, de BRT, 3DB en AERO. 

De tweede knop gebruik je om een melding aan te maken via de webpagina van de bekende terugmeldviewers. Die viewers tonen een kaart. De schaal en locatie van de kaart zal overeenkomen met je QGIS werkblad van dat moment.


## Knop 1: De "WFS" knop
De WFS button gebruik je om een WFS laag aan te maken waarin terugmeldingen getoond zullen worden van de gekozen registratie. In het kort:  
- Open een QGIS project met de kaart van Nederland. 
- Klik op de WFS button om een WFS laag toe te voegen,
- Kies de gewenste service en geef eventueel een bronhoudercode op,
- Klik OK om de keuze te bevestigen en de laag aan te maken. 
##
**De WFS laag**  
De laag zal bovenaan de legenda worden toegevoegd, en heeft een standaard opmaak die enigszins vergelijkbaar is met de bekende weergaves van de gekozen service. De opmaak kan uiteraard naar wens worden gewijzigd. Het is ook mogelijk om je eigen styling mee te geven aan elke nieuw aangemaakte laag, zie verderop onder Customisation. 

<img width="958" height="377" alt="image" src="https://github.com/user-attachments/assets/324a78aa-1f44-4972-b268-90299adf495d" />

## 
**De WFS opties**  
Als je op de button klikt, zal er een dialoogboxje verschijnen met twee opties: servicetype en bronhoudercode. 

<img width="299" height="251" alt="image" src="https://github.com/user-attachments/assets/44a702a2-b79f-40dc-9dc7-1864888dbeb7" /><br/>

**Servicetype**  
Servicetype is een keuzemenu voor de gewenste registratie. Terugmeldingen zijn gekoppeld aan één van de bekende registraties, en voor elk type registratie is er een aparte WFS service endpoint beschikbaar. Afhankelijk van welk type terugmeldingen je wilt zien, moet je dus allereerst de gewenste service kiezen:

<img width="309" height="254" alt="image" src="https://github.com/user-attachments/assets/eb8f3343-2815-4e96-a7fe-5c3077b9777b" /><br/>

**Bronhoudercode**  
Bronhoudercode is een optionele filtercode. Bij het aanmaken van de laag kan eventueel een bronhoudercode-filter toegevoegd worden. Hiermee zorg je ervoor dat uitsluitend de meldingen voor een specifieke bronhouder worden opgevraagd. Dat scheelt in werklast voor de laag (en voor jezelf). 

<img width="306" height="265" alt="image" src="https://github.com/user-attachments/assets/b10db9de-292a-4540-92aa-5315ed97df14" /><br/>

>[!CAUTION]
>BELANGRIJK: De filtercode wordt per servicetype bepaald. Als je van servicetype wisselt, dan wisselt de code mee.  

Het filter gebruikt de PropertyIsLike methode met de volgende kenmerken:  
```<PropertyIsLike wildCard="*" singleChar="?" escapeChar="%">```  
Hiermee kun je bijvoorbeeld ook een WFS-laag maken met alleen de terugmeldingen voor alle provinciale bronhouders:  

<img width="303" height="255" alt="image" src="https://github.com/user-attachments/assets/8693c1c0-95d8-424b-b6da-6c14f3083dd1" /><br/>

Het filter kan overigens, indien gewenst, naderhand nog in QGIS worden aangepast via de laageigenschappen:

<img width="848" height="525" alt="image" src="https://github.com/user-attachments/assets/b1307165-a50c-47ce-92d9-7144e22585c8" /><br/>

  

## Knop 2: De "VDK" knop  

**Opties submenu**  
<img width="275" height="143" alt="image" src="https://github.com/user-attachments/assets/efbd9bb0-036d-4586-a97d-4ea960db6011" />

## Alternatief: "verbeterdekaart" contextmenu
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

<img width="832" height="286" alt="image" src="https://github.com/user-attachments/assets/6ca9b228-e0bb-4861-83e7-b3a693617c13" /><br/>
