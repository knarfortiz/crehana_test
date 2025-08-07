TERRAFORM_IMAGE=hashicorp/terraform:latest
WORKDIR=/workspace
DOCKER_SOCK=/var/run/docker.sock
PLAN_FILE=plan.tfplan

COMMAND=docker run --rm -it \
	-v $(PWD):$(WORKDIR) \
	-v $(DOCKER_SOCK):$(DOCKER_SOCK) \
	-w $(WORKDIR) \
	$(TERRAFORM_IMAGE)

init:
	$(COMMAND) init

validate:
	$(COMMAND) validate

plan:
	$(COMMAND) plan -out=$(PLAN_FILE)

apply:
	$(COMMAND) apply $(PLAN_FILE)

destroy:
	$(COMMAND) destroy $(ARGS)

clean:
	@echo "🧹 Limpiando archivos temporales..."
	@rm -f $(PLAN_FILE)

help:
	@echo "init       Inicializa Terraform"
	@echo "validate   Valida los archivos .tf"
	@echo "plan       Genera el plan y lo guarda en $(PLAN_FILE)"
	@echo "apply      Aplica el plan guardado"
	@echo "destroy    Elimina la infraestructura (usa ARGS=-auto-approve opcional)"
	@echo "clean      Elimina archivos temporales (como el plan)"
