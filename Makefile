NAME = radar

# Commandes Docker
DOCKER_CMD	= docker compose
DOCKER_OPT	= -f
DOCKER_FILE	= docker-compose.yml
DOCKER_COMPOSE = $(DOCKER_CMD) $(DOCKER_OPT) $(DOCKER_FILE)

# Règle par défaut
$(NAME): all

# Règle pour "all" : construit, crée et démarre les services
all:
			$(MAKE) config
			$(MAKE) create

config:
			$(DOCKER_COMPOSE) config
# Création des conteneurs sans les démarrer
create:
			$(DOCKER_COMPOSE) up -d

# Arrêt et suppression des conteneurs, avec suppression des images
clean:
			$(DOCKER_COMPOSE) down --rmi all

# Nettoyage complet (conteneurs, images, volumes)
fclean:
			$(DOCKER_COMPOSE) down --rmi all --volumes --remove-orphans
# Pour relancer tout à zéro
re: fclean all
