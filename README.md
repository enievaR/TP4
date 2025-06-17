# Questions Contexte

- **Dans un modèle TCP, chaque client conserve une connexion ouverte. HTTP, en revanche, est sans mémoire. Comment réconcilier cette absence de session avec un système comme l’IRC, fondé sur un état utilisateur persistant ?**

    Dans un modèle TCP, chaque client établit une connexion persistante avec le serveur, permettant une communication continue. En revanche, HTTP est un protocole sans état, ce qui signifie que chaque requête est indépendante et ne conserve pas d'informations sur les requêtes précédentes.
    Pour réconcilier cette absence de session avec un système comme l'IRC, qui repose sur un état utilisateur persistant, on peut utiliser des techniques telles que :
    1. **WebSockets** : Ils permettent d'établir une connexion bidirectionnelle persistante entre le client et le serveur, permettant ainsi de maintenir l'état de la session.
    2. **Cookies et sessions** : Bien que HTTP soit sans état, on peut utiliser des cookies pour stocker des informations sur l'utilisateur entre les requêtes. Le serveur peut alors identifier l'utilisateur et maintenir son état.
    3. **Stockage côté serveur** : Le serveur peut conserver des informations sur l'état de l'utilisateur dans une base de données ou en mémoire, et les récupérer à chaque requête pour maintenir la continuité de l'état.



- **Peut-on envisager un système où le pseudo est redonné à chaque requête ? Quelles alternatives (cookies, token, paramètre URL) sont envisageables ? Quelles implications en termes de sécurité et d’ergonomie ?**
    Oui, il est possible d'envisager un système où le pseudo est redonné à chaque requête. Cependant, cela peut poser des problèmes d'ergonomie et de sécurité. Voici quelques alternatives et leurs implications :
    
    1. **Cookies** : Les cookies peuvent stocker le pseudo de l'utilisateur entre les requêtes. Cela permet une expérience utilisateur fluide, mais pose des problèmes de sécurité si les cookies ne sont pas correctement sécurisés (par exemple, vulnérabilités XSS).
    
    2. **Token** : Utiliser un token d'authentification (comme JWT) permet de maintenir l'état de l'utilisateur sans avoir à redonner le pseudo à chaque requête. Cela améliore la sécurité, mais nécessite une gestion appropriée des tokens.
    
    3. **Paramètre URL** : Passer le pseudo en tant que paramètre dans l'URL est une option, mais cela peut exposer le pseudo dans les journaux du serveur et les historiques de navigation, ce qui pose des problèmes de confidentialité.
    
    En termes de sécurité, il est crucial de protéger les données sensibles et d'éviter les attaques telles que le vol de session ou l'usurpation d'identité. En termes d'ergonomie, il est important de garantir une expérience utilisateur fluide et intuitive.


- **Dans un serveur TCP, on peut “pousser” des messages. HTTP ne permet pas cela nativement. Quelles solutions techniques peut-on envisager pour permettre aux clients de recevoir de nouveaux messages ? (polling, long-polling, etc.)**
    Dans un serveur TCP, les messages peuvent être envoyés de manière proactive aux clients, mais HTTP ne permet pas cela nativement en raison de sa nature sans état. Voici quelques solutions techniques pour permettre aux clients de recevoir de nouveaux messages :
    
    1. **Polling** : Le client envoie régulièrement des requêtes au serveur pour vérifier s'il y a de nouveaux messages. Cela peut entraîner une charge importante sur le serveur et une latence dans la réception des messages.
    
    2. **Long-polling** : Le client envoie une requête au serveur et le serveur maintient la connexion ouverte jusqu'à ce qu'un nouveau message soit disponible. Une fois le message reçu, le serveur répond et le client peut envoyer une nouvelle requête. Cela réduit la charge par rapport au polling régulier.
    
    3. **WebSockets** : Ils permettent d'établir une connexion bidirectionnelle persistante entre le client et le serveur, permettant au serveur d'envoyer des messages au client dès qu'ils sont disponibles, sans nécessiter de requêtes répétées.
    
    4. **Server-Sent Events (SSE)** : C'est une technologie qui permet au serveur d'envoyer des mises à jour en temps réel au client via une connexion HTTP persistante.
    
    Chacune de ces solutions a ses avantages et inconvénients en termes de complexité, de charge du serveur et de latence.


- **Une commande comme /join #pause_cafe devient-elle une requête POST ? Sur quelle route ? Avec quel corps JSON ? Comment modéliser ces actions dans le paradigme REST ?**
    Dans le paradigme REST, une commande comme `/join #pause_cafe` pourrait être modélisée comme une requête POST. Voici comment cela pourrait être structuré :

    - **Méthode HTTP** : POST
    - **Route** : `/channels/join`
    - **Corps JSON** :
      ```json
      {
        "channel": "#pause_cafe"
      }
      ```

    Dans ce cas, la requête POST est utilisée pour indiquer que l'utilisateur souhaite rejoindre un canal spécifique. Le corps de la requête contient les informations nécessaires pour identifier le canal.

    En termes de modélisation REST, cette action peut être considérée comme la création d'une ressource (l'adhésion de l'utilisateur au canal). Le serveur peut alors répondre avec un statut 201 Created et éventuellement renvoyer des informations sur le canal rejoint ou l'utilisateur.

- **Si /msg devient une ressource, que renvoie un GET /msg ? Tous les messages ? Seulement ceux du canal courant ? Et dans quel ordre ? Où placer la logique métier dans la structure de l’API ?**

    Si `/msg` devient une ressource, la réponse à un `GET /msg` dépend du contexte de l'application et des spécifications de l'API. Voici quelques options :

    - **Tous les messages** : Si l'API est conçue pour renvoyer tous les messages, la requête pourrait renvoyer une liste de tous les messages disponibles dans le système. Cela pourrait être structuré comme suit :
      ```json
      [
        {
          "id": 1,
          "channel": "#general",
          "user": "alice",
          "content": "Hello everyone!",
          "timestamp": "2023-10-01T12:00:00Z"
        },
        {
          "id": 2,
          "channel": "#general",
          "user": "bob",
          "content": "Hi Alice!",
          "timestamp": "2023-10-01T12:01:00Z"
        }
      ]
      ```

    - **Messages du canal courant** : Si l'API est conçue pour renvoyer uniquement les messages du canal courant, la requête pourrait inclure un paramètre pour spécifier le canal, par exemple `GET /msg?channel=#general`. La réponse serait alors limitée aux messages de ce canal.

    - **Ordre des messages** : L'ordre des messages peut être déterminé par le timestamp ou un identifiant unique. Par exemple, on pourrait renvoyer les messages dans l'ordre chronologique ou inversement (du plus récent au plus ancien).

    En termes de logique métier, elle devrait être placée dans le serveur qui gère les requêtes. Le serveur peut appliquer des filtres, des autorisations et d'autres règles métier avant de renvoyer la réponse au client. Par exemple, il peut vérifier si l'utilisateur a accès au canal demandé avant de renvoyer les messages.

- **Comment structurer les URLs : /canaux, /canaux/general,  canaux/general/messages ? Quel niveau de hiérarchie est pertinent ? Quelles conventions de nommage adopter ?**
    La structuration des URLs dans une API RESTful est cruciale pour la clarté et la maintenabilité. Voici une proposition de structure pour les URLs, en tenant compte des conventions de nommage et de la hiérarchie pertinente :

    1. **Liste des canaux** : 
       - URL : `/channels`
       - Méthode : GET
       - Description : Récupère la liste de tous les canaux disponibles.

    2. **Détails d'un canal spécifique** :
       - URL : `/channels/{channelName}`
       - Méthode : GET
       - Description : Récupère les détails d'un canal spécifique, par exemple `/channels/general`.

    3. **Messages d'un canal spécifique** :
       - URL : `/channels/{channelName}/messages`
       - Méthode : GET
       - Description : Récupère tous les messages du canal spécifié, par exemple `/channels/general/messages`.

    4. **Envoyer un message dans un canal** :
       - URL : `/channels/{channelName}/messages`
       - Méthode : POST
       - Corps JSON :
         ```json
         {
           "user": "alice",
           "content": "Hello everyone!"
         }
         ```
       - Description : Envoie un message dans le canal spécifié.

    En termes de hiérarchie, il est pertinent de structurer les URLs de manière à refléter la relation entre les ressources. Les canaux sont des entités principales, et les messages sont des sous-ressources associées à chaque canal. Cela permet une navigation intuitive et une compréhension claire des relations entre les ressources.

    En ce qui concerne les conventions de nommage, il est recommandé d'utiliser des noms pluriels pour les collections (par exemple, `channels`, `messages`) et des noms singuliers pour les ressources individuelles (par exemple, `channel`, `message`). Utiliser des tirets ou des underscores pour séparer les mots peut améliorer la lisibilité (par exemple, `#general` ou `#general_messages`).


- **Si deux utilisateurs envoient un POST /msg en même temps, comment garantir que l’ordre d’arrivée est conservé ? Quelles protections contre les conditions de course ?**

    Pour garantir que l'ordre d'arrivée des messages est conservé lorsque deux utilisateurs envoient un `POST /msg` en même temps, plusieurs approches peuvent être mises en œuvre :

    1. **Utilisation de timestamps** : Chaque message envoyé peut inclure un timestamp indiquant le moment où il a été créé. Le serveur peut alors trier les messages en fonction de ces timestamps avant de les stocker ou de les renvoyer aux clients. Cela permet de conserver l'ordre chronologique des messages.

    2. **Identifiants uniques** : Chaque message peut recevoir un identifiant unique (par exemple, un UUID) généré par le serveur au moment de la réception du message. Les messages peuvent ensuite être triés par cet identifiant, qui peut être basé sur l'heure de création.

    3. **File d'attente des messages** : Implémenter une file d'attente pour les messages entrants peut aider à gérer les conditions de course. Lorsqu'un message est reçu, il est placé dans une file d'attente et traité dans l'ordre d'arrivée. Cela garantit que les messages sont traités séquentiellement.

    4. **Transactions atomiques** : Si le système utilise une base de données relationnelle, on peut utiliser des transactions pour garantir que l'insertion des messages est atomique. Cela signifie que si deux messages sont insérés simultanément, la base de données gérera la concurrence et garantira que l'ordre est respecté.

    5. **Verrouillage optimiste** : Lorsqu'un utilisateur envoie un message, le serveur peut vérifier si le message précédent a été traité avant d'accepter le nouveau message. Si deux messages sont envoyés en même temps, le serveur peut rejeter l'un des messages et demander à l'utilisateur de réessayer.

    En combinant ces techniques, on peut minimiser les risques de conditions de course et garantir que l'ordre des messages est préservé dans le système.

- **Le serveur TCP conserve tout l’état en mémoire. Un service Web doit-il faire pareil ? Ou doit-il persister les données entre deux requêtes ? Si oui,comment ?**

    Un service Web n'est pas obligé de conserver tout l'état en mémoire, mais il est souvent nécessaire de persister certaines données entre les requêtes pour garantir la continuité de l'expérience utilisateur et la fiabilité du système. Voici quelques considérations sur la persistance des données :

    1. **Persistance des données** : Il est recommandé de persister les données critiques (comme les utilisateurs, les canaux, les messages) dans une base de données. Cela permet de conserver l'état entre les requêtes et de récupérer les informations même après un redémarrage du serveur.

    2. **Types de stockage** :
       - **Bases de données relationnelles** : Utiliser des bases de données comme PostgreSQL ou MySQL pour stocker des données structurées avec des relations complexes.
       - **Bases de données NoSQL** : Utiliser des bases de données comme MongoDB ou Redis pour des données non structurées ou semi-structurées, offrant une flexibilité et une scalabilité accrues.
       - **Fichiers** : Pour des données moins critiques ou temporaires, on peut utiliser des fichiers sur le système de fichiers du serveur.

    3. **Gestion de l'état utilisateur** : Pour maintenir l'état utilisateur (comme les sessions), on peut utiliser :
       - **Cookies** : Pour stocker des identifiants de session ou d'autres informations pertinentes.
       - **Tokens JWT** : Pour authentifier les utilisateurs et maintenir leur état sans avoir à stocker des sessions côté serveur.
       - **Sessions côté serveur** : Stocker les sessions dans une base de données ou en mémoire (par exemple, avec Redis) pour une gestion efficace.

    4. **Scalabilité et performance** : En persistant les données, il est important de prendre en compte la scalabilité et la performance du système. Utiliser des caches (comme Redis ou Memcached) peut aider à réduire la charge sur la base de données et améliorer les temps de réponse.

    En résumé, bien que le serveur TCP puisse conserver tout l'état en mémoire, un service Web doit généralement persister certaines données entre les requêtes pour assurer la continuité et la fiabilité du service. La méthode choisie dépendra des besoins spécifiques de l'application et des contraintes techniques.


- **Chaque appel HTTP crée une connexion, lit, écrit, ferme. Quel impact sur la charge réseau et CPU ? À partir de combien d’utilisateurs cela devient-il problématique ?**

    Chaque appel HTTP crée une nouvelle connexion, ce qui peut avoir un impact significatif sur la charge réseau et le CPU du serveur. Voici quelques points à considérer :

    1. **Impact sur la charge réseau** : 
       - Chaque connexion HTTP nécessite un échange de paquets pour établir la connexion (handshake TCP), envoyer la requête, recevoir la réponse et fermer la connexion. Cela entraîne une surcharge en termes de bande passante et de latence.
       - Si de nombreux utilisateurs effectuent des requêtes simultanément, cela peut entraîner une congestion du réseau, surtout si les requêtes sont fréquentes.

    2. **Impact sur le CPU** :
       - La création et la gestion de connexions HTTP consomment des ressources CPU. Chaque connexion nécessite des ressources pour traiter les requêtes, gérer les sessions et envoyer les réponses.
       - Si le nombre d'utilisateurs augmente, le serveur peut devenir surchargé, entraînant des temps de réponse plus longs et une dégradation des performances.

    3. **À partir de combien d'utilisateurs cela devient-il problématique ?**
       - Le seuil à partir duquel cela devient problématique dépend de plusieurs facteurs, notamment la capacité du serveur (CPU, mémoire, bande passante), l'optimisation du code, et l'architecture du système.
       - En général, pour un serveur standard, on peut commencer à observer des problèmes de performance avec quelques centaines à quelques milliers d'utilisateurs simultanés, selon la nature des requêtes (par exemple, des requêtes lourdes en données ou en traitement).
       - Pour des applications à fort trafic, il est courant d'utiliser des techniques comme le **caching**, les **WebSockets** ou le **long-polling** pour réduire le nombre de connexions HTTP nécessaires et améliorer l'efficacité.

    En conclusion, bien que chaque appel HTTP soit indépendant, il est crucial de concevoir l'architecture du système pour gérer efficacement les connexions afin d'éviter une surcharge réseau et CPU lorsque le nombre d'utilisateurs augmente.