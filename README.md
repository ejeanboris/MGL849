#### MGL849 – Hiver 2020  
**Modélisation, analyse et programmation des systèmes temps réel**  
**Laboratoire #2**  
**Panneau de contrôle des gaz**

---

### Objectif

Dans le laboratoire #2, on veut que vous consolidiez vos connaissances, acquises lors du laboratoire précédent, afin de réaliser d’une façon plus autonome les fonctionnalités décrites ci-dessous.

---

### Description du travail demandé

Dans ce laboratoire, vous allez concevoir et implémenter un logiciel embarqué sur le Raspberry Pi 3. Ce logiciel a pour objectif principal de réagir à la détection des fuites de gaz simulées d’un programme fourni pour ce laboratoire. Ce logiciel de simulation joue aussi le rôle d’un outil de test de la fiabilité et l’efficacité du logiciel embarqué avant son installation dans une zone industrielle (au niveau des réservoirs ou des tuyauteries).

![Figure 1 - Interface du programme de simulation](https://camo.githubusercontent.com/27c174d5526113ae1c8b63b694a38edf1e96db511741b0f7825cdb1ecd296072/68747470733a2f2f726566732e7265686f756e6f752e63612f75706c6f6164732f696d616765732f67616c6c6572792f323032352d30312f7363616c65642d313638302d2f73326353345777754d685256757336782d696d6167652e706e67)

**Figure 1** présente l’interface du programme de simulation de fuites des gaz.

Elle comporte :  
- **Des composants graphiques** de variations (progress bar) des valeurs de trois types de gaz (qui peuvent être CO2, CO, O3, CH4, etc.). Ces valeurs affichées sont capturées par des capteurs dédiés à mesurer les concentrations des gaz et par conséquent détecter des fuites éventuelles.  
- **Des actions (commandes)** qui peuvent être appliquées en cas de fuites :  
  - Aération à trois niveaux  
  - Ventilation à deux niveaux  
  - Injection de gaz : cette action se manifeste par l’injection d’un gaz qui peut neutraliser le gaz ciblé (celui de la fuite).

L’utilisateur peut réagir aux fuites de gaz manuellement via l’interface graphique ou automatiquement via les réactions appropriées du logiciel embarqué. 

Le logiciel embarqué à développer et le programme de simulation (test) doivent communiquer les valeurs, alarmes, et commandes via le réseau en utilisant les sockets. Le protocole de communication (description des messages) est défini dans le tableau ci-dessous.

---

### Protocole de communication

| Information                                        | Format                      | Expéditeur → Récepteur          |
|----------------------------------------------------|-----------------------------|---------------------------------|
| La concentration de gaz Gas1                      | `LG1Val` tq. Val=0..100     | Prog. Simulation → Prog. Embarqué |
| La concentration de gaz Gas2                      | `LG2Val` tq. Val=0..100     | Prog. Simulation → Prog. Embarqué |
| La concentration de gaz Gas3                      | `LG3Val` tq. Val=0..100     | Prog. Simulation → Prog. Embarqué |
| La commande Aération niveau 1                     | `AL1`                       | Prog. Embarqué → Prog. Simulation |
| La commande Aération niveau 2                     | `AL2`                       | Prog. Embarqué → Prog. Simulation |
| La commande Aération niveau 3                     | `AL3`                       | Prog. Embarqué → Prog. Simulation |
| Désactivation de la réaction de l’aération         | `AN`                        | Prog. Embarqué → Prog. Simulation |
| La commande Ventilation niveau 1                  | `VL1`                       | Prog. Embarqué → Prog. Simulation |
| La commande Ventilation niveau 2                  | `VL2`                       | Prog. Embarqué → Prog. Simulation |
| Désactivation de la réaction de la ventilation     | `VN`                        | Prog. Embarqué → Prog. Simulation |
| Injection de gaz annulant l’effet de Gas1         | `IG1`                       | Prog. Embarqué → Prog. Simulation |
| Injection de gaz annulant l’effet de Gas2         | `IG2`                       | Prog. Embarqué → Prog. Simulation |
| Injection de gaz annulant l’effet de Gas3         | `IG3`                       | Prog. Embarqué → Prog. Simulation |
| Désactivation de l’injection de Gas1              | `AIG1`                      | Prog. Embarqué → Prog. Simulation |
| Désactivation de l’injection de Gas2              | `AIG2`                      | Prog. Embarqué → Prog. Simulation |
| Désactivation de l’injection de Gas3              | `AIG3`                      | Prog. Embarqué → Prog. Simulation |
| Commande d’alerte pour Gas1                       | `AG1X` X = ``, `L`, `M`, `H`| Prog. Embarqué → Prog. Simulation |
| Commande d’alerte pour Gas2                       | `AG2X` X = ``, `L`, `M`, `H`| Prog. Embarqué → Prog. Simulation |
| Commande d’alerte pour Gas3                       | `AG3X` X = ``, `L`, `M`, `H`| Prog. Embarqué → Prog. Simulation |

---

### Description des actions

| Graduation (croissante) | Action                 | Effet                                     | Coût                                  |
|--------------------------|-----------------------|-------------------------------------------|---------------------------------------|
| 1                        | Aération niveau 1     | Effet faible sur une faible fuite         | Presque rien à perdre                 |
| 2                        | Aération niveau 2     | Effet modéré sur une faible fuite         | Nécessite un peu plus d’énergie       |
| 3                        | Aération niveau 3     | Effet important sur une faible fuite      | Parfois n’est pas possible            |
| 4                        | Ventilation niveau 1  | Effet modéré sur une fuite moyenne        | Consommation d’énergie considérable   |
| 5                        | Ventilation niveau 2  | Effet important sur une fuite moyenne     | Plus de consommation                  |
| 6                        | Injection de gaz      | Neutralité totale du gaz                  | Le gaz à injecter coûte cher et est une ressource épuisable |

---

### Remarques

Pour raison de simplification, les valeurs des concentrations des gaz sont en pourcentage. Par exemple, le 100% du gaz CO2 peut correspondre à la valeur 1000 ppm.

- Pas d’alarme (`''`) si la valeur est entre 0-5.  
- Alarme niveau 1 (`L` pour Low) si la valeur est entre 6-20.  
- Alarme niveau 2 (`M` pour Medium) si la valeur est entre 21-50.  
- Alarme niveau 3 (`H` pour High) si la valeur est entre 51-100.  

En notant que le temps de réaction du logiciel embarqué est critique, la décision de l’action à appliquer devrait être appropriée en termes de :  
- **Efficacité** : Neutraliser l’effet de la fuite et informer les surveillants par des alarmes.  
- **Coût** : Minimiser les ressources consommées pour éviter des réactions excessives.

Finalement, vous avez la liberté de décider comment organiser les tâches. Il est très recommandé d’utiliser autant que possible les techniques de modélisation acquises dans le cours.
