"""
Le sujet porte sur la surveillance d’un lieu stratégique tel qu’une salle serveur.
Pour se faire, on va réaliser la détection des grandeurs physiques à l’aide d’une carte Arduino Yun*
équipée de capteurs : Mouvement - Température et humidité.

Dans un premier temps, on va détecter les grandeurs physiques, puis on va les transmettre à la REST API via la communication HTTP.
L’API est hébergée dans un serveur local via la carte Raspberry Pi.
La gestion d’alerte sera gérée au niveau de la carte raspberry Pi ainsi que L’interface d’affichage graphique.


*Option facultative : Déclencher un climatiseur ou un ventilateur pour faire diminuer la température (commande à distance).

"""
import uvicorn
import Base_de_donnée

if __name__ == "__main__":
    # The next commande line is to acces the API  from any device in local network
    ## So to get in, you should enter the ip adress of the the host computer
    ###By entering commande >$ ipconfig in windows and ifconfig in Linux and MacOS
    uvicorn.run("app:app", port=8000,host='0.0.0.0',reload=True)
    #The next commande is to acces api only on localhost "Your computer only",
    ##Run the commande wish is good for you.
    #uvicorn.run("app:app", port=8000, host='127.0.0.3', reload=True)
    __test__()