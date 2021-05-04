# CO2 Ampel

Die CO2-Werte in den Räumen werden jeweils von einer Netatmo Wetterstation gemessen und können zentral über die Netatmo API abgefragt werden. Die LED-Strips werden über eine Philips Hue Bridge gesteuert, welche ebenfalls per API angesprochen werden kann um die Farbe der LED-Strips zu ändern. Ein Python Script fragt die Netatmo API im Minutentakt ab und ändert die Farbe des LED-Strips im entsprechenden Raum wenn ein CO2-Grenzwert überschritten wird. Bis 1000ppm leuchten die LEDs grün, ab 1000ppm gelb und ab 1400ppm rot.
