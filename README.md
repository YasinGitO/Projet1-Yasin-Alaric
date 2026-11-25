# Projet1-Yasin-Alaric

Un jeu d'arcade de type *Space Invader* développé en Python avec **Pygame**, issu de la refonte orientée objet d'un prototype procédural initial.

---

## Table des matières
- [Présentation du projet](#présentation-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Architecture & Diagramme de classes](#architecture--diagramme-de-classes)
- [Structure du dépôt](#structure-du-dépôt)
- [Installation et lancement](#installation-et-lancement)
- [Contrôles](#contrôles)
- [Auteurs](#auteurs)

---

## Présentation du projet

L'objectif de ce projet est de transformer un script procédural monolithique (`main.py` d'origine, reposant sur des variables globales et des tableaux parallèles) en une architecture **orientée objet modulaire, maintenable et extensible**, en appliquant les principes fondamentaux de la POO (encapsulation, héritage, polymorphisme, séparation des responsabilités).

---

## Fonctionnalités

- **Système d'entités hiérarchisé :** classe mère `Entity` factorisant les points de vie, la vitesse, les coordonnées (`Coordinate`), le rendu et la gestion des dégâts.
- **Types d'ennemis variés :**
  - `Ennemy` : ennemi standard se déplaçant horizontalement et descendant par paliers au contact des bords de l'écran.
  - `EnnemiTank` : sous-classe d'`Ennemy` plus lente mais dotée de 3 PV, infligeant davantage de dégâts et rapportant plus de points.
- **Difficulté progressive :** réduction dynamique du délai d'apparition des ennemis (`get_spawn_delay()`) au fur et à mesure que le score augmente.
- **Système d'armement évolutif :**
  - **Pistolet** : munitions illimitées, cadence standard (`400 ms`), 1 dégât.
  - **Mitraillette** : 40 munitions, cadence rapide (`150 ms`), 1 dégât.
  - **Canon** : 10 munitions, cadence lente (`800 ms`), 3 dégâts (capable de détruire un `EnnemiTank` en un tir).
  - Retour automatique au *Pistolet* lorsque les munitions d'une arme spéciale sont épuisées.
- **Power-ups dynamiques :** apparition probabiliste de bonus à la mort d'un ennemi permettant de changer d'arme en vol.
- **Interface HUD & Game Over :** affichage en temps réel du score, des points de vie restants, de l'arme équipée et de ses munitions.

---

## Architecture & Diagramme de classes

Le diagramme ci-dessous est rendu directement par GitHub via **Mermaid** :

```mermaid
classDiagram
    direction TB

    namespace Moteur {
        class Main {
            +game: Game
            +joueur: Player
            +clock: Clock
            +run()
        }
        class Game {
            +players: list~Player~
            +ennemies: list~Ennemy~
            +powerups: list~PowerUp~
            +level: int
            +last_spawn: int
            +running: bool
            +game_over: bool
            +screen: Surface
            +background: Surface
            -_init_pygame()
            +get_screen_size() tuple
            +set_background(background)
            +handle_collisions(player)
            +spawn_ennemy()
            +get_spawn_delay() int
            +update_spawn()
            +drop_powerup(ennemi)
            +handle_powerups(player)
            +handle_player_collisions(player)
            +draw_hud(player)
            +draw_game_over()
        }
    }

    namespace Entites {
        class Entity {
            +hp: int
            +speed: int
            +coordinate: Coordinate
            +is_alive() bool
            +draw(screen)
            +take_damage(damage)
        }
        class Player {
            +name: str
            +score: int
            +weapon: Arme
            +update()
            +change_weapon(nouvelle_arme)
            +shoot()
            +handle_input()
        }
        class Ennemy {
            +damage: int
            +points: int
            +update()
            +is_hit_by(bullet) bool
            +touch_ennemy(player)
        }
        class EnnemiTank {
            +__init__(x, y, game)
        }
    }

    namespace Combat_et_Bonus {
        class Arme {
            +type: str
            +damage: int
            +cooldown: int
            +ammo: int
            +shooted_bullets: list~Bullet~
            +shoot(center_x, start_y) bool
            +update()
            +draw(screen)
        }
        class Bullet {
            +coordinate: Coordinate
            +speed: int
            +damage: int
            +update()
            +draw(screen)
        }
        class PowerUp {
            +weapon_name: str
            +coordinate: Coordinate
            +speed: int
            +update()
            +draw(screen)
        }
    }

    namespace Utilitaire {
        class Coordinate {
            +x: int
            +y: int
            +clamp_x(min_x, max_x)
            +move(dx, dy)
            +get_tuple() tuple
        }
    }

    Main *-- "1" Game
    Main ..> Player : crée et ajoute
    Entity <|-- Player
    Entity <|-- Ennemy
    Ennemy <|-- EnnemiTank
    Game "1" o-- "1..*" Player
    Game *-- "0..*" Ennemy
    Game *-- "0..*" PowerUp
    Player o-- "1" Arme
    Arme *-- "0..*" Bullet
    Entity *-- "1" Coordinate
    Bullet *-- "1" Coordinate
    PowerUp *-- "1" Coordinate
