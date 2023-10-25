"""
The "hello world" custom component.

This component implements the bare minimum that a component should implement.

Configuration:

To use the hello_world component you will need to add the following to your
configuration.yaml file.

hello_world:
"""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from socket import *
import sys

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "tild_custom_info_service"

def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up a skeleton component."""
    def handle_tild(call):
      
      sockUDP = socket(AF_INET, SOCK_DGRAM)
      sockUDP.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
      sockUDP.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
      sockUDP.settimeout(10)

      server_address = ('255.255.255.255', 30303)

      message = 'D'
      try:
          sent = sockUDP.sendto(message.encode(), server_address)
          data, server = sockUDP.recvfrom(256)
          name = data.decode('UTF-8')
          #print(data.decode('UTF-8'))
          #print('TILD IP: ' + str(server[0]))
          
      finally:	
          sockUDP.close()


      tild_address = (str(server[0]), 30302)

      sockTCP = socket(AF_INET, SOCK_STREAM)
      sockTCP.settimeout(10)
      message = 'Begin'
      try:
          sockTCP.connect(tild_address)
          n = sockTCP.send(message.encode('utf-8'))
          if (n == len(message)):
              datatcp = sockTCP.recv(256)
              #print(donnees)

      finally:
          sockTCP.close()
      donnees = datatcp.decode('UTF-8')

      jour = donnees[128:130]
      mois = donnees[130:132]
      annee = donnees[132:134]
      
      minutes = donnees[122:124]
      heures = donnees[124:126]

      Lumierestatus = donnees[34:35] # 0 desactivé 2 = lumiere 3= lumiere + pompe
      if Lumierestatus == '0':
        Lumiere = 0
      if Lumierestatus == '2':
        Lumiere = 1
      if Lumierestatus == '3':
        Lumiere = 1
      couleur = donnees[64:66]
      intensite = donnees[71:72]
      def intensitepercent(intensite):  
        #'0','4','8','C
        switcher = {
        '0': "25",
        '4': "50",
        '8': "75",
        'C': "100",
        }
      
      temperature = int(donnees[66:68],16)

      pompeavecfiltration = donnees[75:76]  # avec = 8  sans =0
      traitementprograme = donnees[69:70]   # 3=desactivé 7= traitement programe

      OffsetTemp = donnees[155:156]
        # 0 = 0
        # 6 = -3°
      temperaturereel = 0
      if OffsetTemp == "0":
          temperaturereel = temperature

      if OffsetTemp == "6":
          temperaturereel = temperature + 3


     #expression_par_defaut
    #  ParseTemp1 = donnees[1:30]
    #  ParseTemp2 = donnees[31:37]
    #  ParseTemp3 = donnees[38:64]
    #  ParseTemp4 = donnees[97:120]
     

      # States are in the format DOMAIN.OBJECT_ID.
      hass.states.set('tild_custom_info.Hello', temperature)

      hass.states.set('tild_custom_info.systeme', name)
      hass.states.set('tild_custom_info.adresse', str(server[0]))
      hass.states.set('tild_custom_info.valeurs', donnees)

      hass.states.set('tild_custom_info.date', jour + '/' + mois + '/' + annee)
      
      hass.states.set('tild_custom_info.heure', heures + ':' + minutes )
      hass.states.set('tild_custom_info.Lumiere', Lumiere)
      hass.states.set('tild_custom_info.couleur', couleur)
      hass.states.set('tild_custom_info.intensite', intensite)

      hass.states.set('tild_custom_info.pompeavecfiltration', pompeavecfiltration)
      hass.states.set('tild_custom_info.traitementprograme', traitementprograme)

      hass.states.set('tild_custom_info.temperature', temperature)
      hass.states.set('tild_custom_info.OffsetTemp', OffsetTemp)


    #  hass.states.set('tild_custom_info.ParseTemp1', ParseTemp1)
    #  hass.states.set('tild_custom_info.ParseTemp2', ParseTemp2)
    #  hass.states.set('tild_custom_info.ParseTemp3', ParseTemp3)
    #  hass.states.set('tild_custom_info.ParseTemp4', ParseTemp4)


      hass.states.set('sensor.tild_custom_info_temp', temperature, {'unit_of_measurement': '°C' , 'friendly_name': 'Piscine temperature'})
      hass.states.set('sensor.tild_custom_info_tempreel', temperaturereel, {'unit_of_measurement': '°C' , 'friendly_name': 'Piscine temperature reel'})
      
      hass.states.set('binary_sensor.tild_custom_info_Lumiere', Lumiere,{  'friendly_name': 'Piscine Lumiere','icon': 'mdi:lightbulb'})
      hass.states.set('select.tild_custom_info_intensite', intensite,{ 'friendly_name': 'puissance lumiere','options': {'0','4','8','C'} }) # 0 = Faible , C = Fort
      # couleurs 
      #01 Froid
      #02 Bleeu
      #03 Lagon
      #04 Cyan
      #05 Violet
      #06 Magenta
      #07 Rose
      #08 Rouge
      #09 Orange
      #0A Vert
      #0B couleur favorite
      #10 Sequence Dégradé
      #11 Arc en ciel
      #12 Défilé
      #13 Techno
      hass.states.set('light.tild_custom_info_Lumiere_full', Lumiere,{  'friendly_name': 'Piscine Lumiere full','icon': 'mdi:lightbulb', 'rgbw_color': '[255,0,0,255]' ,'brightness_pct': '50' })

    hass.services.register(DOMAIN, "tild_custom_info", handle_tild)

    # Return boolean to indicate that initialization was successfully.

    return True

