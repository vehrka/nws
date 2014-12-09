=======================
Naval Warfare Simulator
=======================

Intro
=====

The idea is to assist in the playing of the Command at Sea wargame from Clash
of Arms.

Probably it won't grow over a lot of rants about how to make an online
multiplayer game for naval warfare based on World War II naval warfare, but you
never can tell.

Some ideas:

* Is it possible to develop the game in Flask
  and making it platform agnostic.

* Is it possible to store the data on SQLite3.

What do I want:

* A multiplayer app

* An app that shows a map with the ships data

* An app where a player can send orders to his ships

* I can set several multiplayer games:

  * The player will have one of three possible roles:

    * Player
    
    * Referee
    
    * Expectator

  * A player can be assigned to a side or to one or several ships and have
    limited information

Install
=======

Clone the repository::

    $ git clone https://github.com/vehrka/nws.git
    $ cd nws

Create the virtual environment::

    $ mkvirtualenv -r requirements.txt nws

Create the configuration file::

    $ cp config/example.cfg config prod.cfg

Modify the contents to match your system.

Install *javascript* dependencies::

    $ bower install

Fire the server::

    $ fab runprod
