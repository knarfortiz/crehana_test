TERRAFORM_IMAGE=hashicorp/terraform:latest
WORKDIR=/workspace
DOCKER_SOCK=/var/run/docker.sock
COMMAND=docker run --rm -it \
		-v $(PWD):$(WORKDIR) \
		-v $(DOCKER_SOCK):$(DOCKER_SOCK) \
		-w $(WORKDIR) \
		$(TERRAFORM_IMAGE)

init:
	$(COMMAND) init

plan:
	$(COMMAND) plan

apply:
	$(COMMAND) apply

destroy:
	$(COMMAND) destroy
