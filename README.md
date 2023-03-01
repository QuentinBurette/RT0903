# TP Kubernetes

# Info Pratique:
adresse email intervenant: amnay.m@gmail.com

# Preparation

- Disposer d'un compte [Google](https://accounts.google.com/signup) (Si vous avez une boite mail GMail, c'est tout bon!)
- Disposer d'un compte [Github](https://github.com/signup)
- Disposer d'un compte [Docker Hub](https://hub.docker.com/signup)
- **important** renseigner vos informations sur ce [google sheet](https://docs.google.com/spreadsheets/d/13IHlEyLHt_dNwGujlVxwRdqYJ65BRv-kGvx5GZJJ7qY/edit?usp=sharing)

# 🎉🎉  Dockerfile + Code python du microservice [ici](https://gist.github.com/amnay-mo/decf9807eec917b2c677f8c88c256ea8)  🎉🎉

# TP 1

Ecrire un microservice http "motd-api" (MOTD == Message of the Day)
- Le microservice retourne toujours un objet json `{"message": MESSAGE}`
- le MESSAGE doit être configurable
- Le service prend deux variables d'environnement pour sa configuration:
  - `MESSAGE` est le message retourné par l'API
  - `APP_PORT` est le port d'écoute de l'API


```
➜  motd-api git:(master) ✗ APP_PORT=5555 MESSAGE="Hello World!" ./motd-api
2021/03/22 10:17:21 starting app
2021/03/22 10:17:41 127.0.0.1:42306 GET /
```

```
➜  ~ http GET ':5555/'
HTTP/1.1 200 OK
Content-Length: 27
Content-Type: application/json
Date: Mon, 22 Mar 2021 09:17:41 GMT

{
    "message": "Hello World!"
}
```

- pousser votre code dans votre dépot git
- invitez-moi dans votre depot git; mon pseudo github : "amnay-mo"


# TP 2 

- Dockeriser "motd-api"
- Fournir le Dockerfile dans le dépot git

# TP 3

- Pousser l'image Docker dans votre docker hub


```sh
$ docker login # il faudra vous authentifier au moins une fois
$ docker build -t <COMPTE_DOCKER_HUB>/<NOM_IMAGE_DOCKER>:<VERSION> .
$ docker push  <COMPTE_DOCKER_HUB>/<NOM_IMAGE_DOCKER>:<VERSION>
```

- Documenter le nom de l'image dans le README du dépot GIT


# TP 4 : installation de gcloud et kubectl

⚠️ **Utiliser l'adresse gmail que vous m'avez donné pour l'authentification GCloud**

- installer l'outil CLI GCLOUD: https://cloud.google.com/sdk/docs/install
- téléchargez le client kubernetes `kubectl` et ajoutez-le dans votre path:

```sh
https://dl.k8s.io/release/v1.24.9/bin/windows/amd64/kubectl.exe
```

- Vérifiez que kubectl est bien installé:

```sh
kubectl version
```

- Bonus: activez l'auto-complétion bash pour kubectl:

```sh
echo 'source <(kubectl completion bash)' >>~/.bashrc
```

ℹ️ **Kubectl** est votre compagnon pour toute interaction avec un cluster K8S. Voici un Cheat Sheet qui peut vous être utile: https://kubernetes.io/docs/reference/kubectl/cheatsheet/

# TP 5 : setup de gcloud et kubectl

## Configuration de GCloud

- authentification:

```sh
gcloud auth login
```

- notre project google cloud s'appelle "amnay-k8s-337617"

```sh
gcloud config set project amnay-k8s-337617
```

- Lister le cluster kubernetes

```sh
gcloud container clusters list
```

- Récupérer les credentials de connexion au Cluster Kubernetes

```sh
export USE_GKE_GCLOUD_AUTH_PLUGIN=True
gcloud container clusters get-credentials --zone=europe-west9-b tp-k8s
```

## Kubectl

- Vérifez que vous avez bien un nouveau context k8s:

```sh
kubectl config get-contexts
```

- Vérifier qu'on arrive à requeter  l'API du cluster kubernetes, en listant les `nodes` par exemple:

```sh
kubectl get nodes
```

# TP 6 : création et configuration de votre namespace

- créer son propre <namespace> sous forme de <prenom.nom>

```sh
kubectl create ns <prenom-nom>
```

- configurer le Namespace par défaut

```sh
kubectl config set-context --current --namespace=<prenom-nom>
```

⚠️ Veillez à bien rester dans votre **namespace personnel** tout le long du TP

- Vérifiez que votre `context` est correctement configuré, avec le bon nom de `namespace`
- Vous verrez s'afficher pas mal d'informations utiles concernant votre cluster k8s, notamment l'URL publique du kube-apiserver

```sh
kubectl config view --minify
```

- Vérifiez que le client `kubectl` arrive bien à communiquer avec le serveur API du cluster Kubernetes:
- On arrive bien à récupérer la version du serveur API:

```sh
kubectl version
```

- On arrive bien à lister les `nodes` du cluster:

```sh
kubectl get nodes
```

# TP 8 : premier pod

- Creer un fichier `pod.yml`:

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: <nom_de_votre_pod>
  labels:
    app: motd
spec:
  containers:
  - name: motd
    image: <nom_de_votre_image_docker>
```

- Faites écouter le pod sur le port `80`

```sh
kubectl apply -f pod.yml
```

⚠️ **votre_image** doit être accessible via un `docker pull` pour que Kubernetes puisse la récupérer!

- Essayez d'appeler votre webservice après l'avoir rendu accessible à l'aide de la commande

```sh
kubectl port-forward <nom_du_pod> <port_dans_votre_machine>:<port_du_pod>
```

- Vérifiez que votre webservice écrit bien des logs :
 
```sh
kubectl logs -f <nom_de_votre_pod>`
```

- Listez vos pods et observez les différents champs (le Status, le Node où il est déployé):

```sh
kubectl get pods -o wide
```

- Vous pouvez aussi obtenir plus ample information sur votre pod avec la commande:

```sh
kubectl get pods -o yaml
```

- Editez votre pod ajouter un label supplémentaire `env: prod` au pod

```sh
kubectl edit pod <nom_du_pod>
```

- supprimez ce pod

```sh
kubectl delete pod <nom_du_pod>
```

- vérifiez que votre pod a bien disparu

```sh
kubectl get pods
```

- recréez-le

```sh
kubectl apply -f pod.yml
```

# TP 9 : Premier service

- Créer un fichier `service.yml` qui définit un service de type ClusterIP qui pointe sur le pod que vous avez créé dans l'étape précedente. utilisez cette doc pour vous guider (doc: https://kubernetes.io/docs/concepts/services-networking/service/)

- Appliquer le service sur le cluster:

```sh
kubectl apply -f service.yml
```

- Vérifier que votre service a bien été créé:

```sh
kubectl get service
```

- Verifier que votre service pointe bien sur votre pod en listant les endpoints:

```sh
kubectl get endpoints
```

- Comme c'est un service de type `ClusterIP`, il n'est accessible que depuis l'intérieur du cluster
- Essayez de vous y connecter en lançant en lançant un curl depuis un pod de debug:

```sh
kubectl run -i --tty --rm debug --image=ubuntu --restart=Never -- bash
apt update && apt install -y httpie
http GET  'http://<nom-du-service>.<nom-du-namespace>.svc.cluster.local/'
```

- Faites  un nslookup sur le nom du service `<nom-du-service>.<nom-du-namespace>.svc.cluster.local`





```sh
apt update && apt install dnsutils
nslookup <nom-du-service>
```

- Essayez de requeter votre service en utilisant la version longue de son nom DNS

Tip: Si votre service n'est pas correctement connecté à votre pod, éditez le selecteur du Service et le Label du pod afin qu'ils correspondent:

```sh
kubectl edit svc <nom_du_service>
kubectl edit pod <nom_du_pod>
```

# TP 10 : Going Public!

- Une fois assurés que votre Service ClusterIP est fonctionnel, créez un service de type LoadBalancer et essayez d'y accéder en utilisant son adresse IP publique
💡Il suffit d'ajouter le champ `type: LoadBalancer` à la partie `spec` de la définition de votre `Service`

# TP 11 : Deploiements multi-instances
- Supprimez votre pod
- Vérifiez que votre service n'est plus disponible (via l'IP publique du service LoadBalancer)
- Créer un "Deployment" qui déploie 3 instances de votre conteneur motd
- Observez la création de votre "Deployment" `kubectl get deploy -o wide`
- Gardez le même Label que celui configuré dans votre Service LoadBalancer (TP 10)
- Vérifiez que votre service est toujours joignable
- Vérifiez que vous avez bien pods en exécution avec `kubectl get pods`
- Essayez de supprimer à la main un des pods du déploiement et observez que le pods manquant est aussitôt recréé  `kubectl delete pod <nom_d_un_des_pods>`

Doc : https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Tip: Créer un fichier yaml similaire à celui de la doc, éditer la config, puis appliquer le fichier avec `kubectl apply -f <fichier.yaml>`

## Config Map & Canary Deployment

- Créer un fichier `configmap.yml` qui contient une configmap avec les clé/valeurs ( doc: https://kubernetes.io/docs/concepts/configuration/configmap ) 
  -  message: "Do not eat the yellow snow!"
-  Créer un fichier `deployment_canary.yml` qui:
  -  utiliser la configmap créée ci-dessus pour renseigner la variable d'env "MESSAGE" du container motd de ce deployment
  -  ce deployment à aussi un label `app=motd` afin qu'il soit routé par le service LoadBalancer créé précédemment
-  Accédez à votre service en faisant plusieurs requetes, et remarquez le round-robin effectué entre les deux deployments

# TP 12 : Ingress


- Un `NGINX-INGRESS-CONTROLLER` vient d'être installé dans le cluster Kubernetes. Son IP publique est consultable en jetant un oeil sur le service de type `LoadBalancer` dans namespace `nginx-ingress`
	- Plus besoin d'avoir chacun son propre service de type LoadBalancer pour exposer son service à internet
- Supprimez donc tous les services de **votre namespace**
- Créez un service de type ClusterIP pour votre "Deployment"
- NB: si vous disposez de votre propre nom de domaine personnel , vous pouvez sauter cette étape
  - Demandez un nom de domaine à votre instructeur (elle sera de la forme "prenom-nom.amnay.fr"
- Créez un `ingress` pour permettre l'accès à votre Service, en vous aidant de cette [doc](https://kubernetes.io/docs/concepts/services-networking/ingress/) ou [celle-ci](https://docs.nginx.com/nginx-ingress-controller/configuration/ingress-resources/basic-configuration/)
- Astuce: Le nom de domaine qui vous sera fourni sera renseigné dans le champ `host` de votre ingress
- Astuce: assurez-vous d'ajouter la ligne `ingressClassName: nginx` dans la spec de votre `Ingress`
- Vérifiez que vous arrivez à acceder à votre service via l'url `http://<prenom-nom>.amnay.fr/`

# TP 13: Grand nettoyage

- Crééz un répertoire s'appelle `k8s` dans la racine de votre dépôt git
- Dans ce répertoire, vous devez avoir les manifests k8s nécessaires au déploiement de votre microservice:
  - le `Deployment` dans deployment.yml
  - le `Service` dans `service.yml`
  - la config du microservice dans un `ConfigMap` dans configmap.ym (les variables d'environnement de votre microservice doivent être initialisées grace à ce configmap)
  - le `Ingress` de votre service dans `ingress.yml`
- Commitez et poussez
- Supprimez votre namespace k8s `kubectl delete namespace <votre namespace>`
- Vous avez à présent perdu toutes vos ressources sur k8s.
- Recréez votre namespace `kubectl create namespace <votre namespace>`
- Redéployez votre microservice à l'aide des manifests que vous avez créé dans `/k8s`
- Vérifiez que votre microservice fonctionne correctement et est bien accessible depuis internet


# InitContainer

- Nous voulons à présent ajouter un [InitContainer](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) au pod de notre application `motd`
- Le role de cet InitContainer est de créer un fichier dans un volume du pod, et d'écrire le "message" de `motd` dans ce fichier. doc concernant le type de volume à utiliser pour cette exercice [ici](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/)
- Le plus simple serait de créer une image docker d'un petit programme qui fait ça. Vous le poussez sur votre dockerhub et vous l'utilisez en tant que InitContainer dans votre pod
- Vous mettrez à jour le code de l'application `motd`pour qu'il aille chercher le "message" dans ce fichier
- Si la lecture de ce fichier échoue, `motd` doit écrire une ligne de log pour signaler cet echec et utiliser la variable d'environnement "MESSAGE"
- Le message écrit par le InitContainer doit provenir d'un [Secret](https://kubernetes.io/docs/concepts/configuration/secret/)

# StatefulSet

- Changer le code source de votre microservice `motd` de la manière suivante:
  - il peut maintenant récupérer le "message" depuis une base de donnée de votre choix
  - l'URL de la base de donnée est fournie par variable d'environnement
- Créer un StatefulSet (avec une seule instance) et un service de type ClusterIP pour votre base de donnée. exemple de définition de statefulset: https://gist.github.com/amnay-mo/ec02c6e6bbf4c6f41eaa8b233fa342d2 doc: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
- Remarquez qu'un PersistentVolumeClaim et un PersistentVolume ont été créés

```sh
kubectl get pvc
kubectl get pv
```

- Remarquez aussi que Google Cloud a provisionné des disques qui correspondent à votre PersistentVolume:

```sh
gcloud compute disks list
```

- Peuplez manuellement votre base de donnée avec au moins un message afin que votre application puisse l'utiliser
- Tester votre application
- Supprimez le pod (et non pas le statefulset) de votre base de donnée
- Remarquez qu'un nouveau pod est aussitôt créé par le StatefulSet, et que les données n'ont pas été perdues


# CI/CD : 

- Créer un script "build-and-deploy.sh" qui permet de:
	- Build & Push l'image docker sur votre docker hub. La version du tag de l'image docker doit correspondre  aux 6 premiers caractères du hash du commit afin de générer un id de version unique pour chaque 
	- Mettre à jour le **Deployment** avec l'image docker nouvellement créé dans votre cluster kubernetes (dans votre namespace bien-sur)
	
