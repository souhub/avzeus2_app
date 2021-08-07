PROFILE:=default
REGION:=us-east-1
PREFIX:=avzeus
ENV:=production
# SERVICE:=bldg
# AWS_COMMAND_PREFIX := docker build -f cloudformation/Dockerfile -t avzeus-cloudformation . && docker run avzeus-cloudformation
AWS_COMMAND_PREFIX := docker run -v /Users/sou/.aws:/root/.aws \
								 -v Makefile:/aws/Makefile \
								 -v cloudformation/templates:/aws/templates \
								 amazon/aws-cli:2.2.14
# DOMAIN := xn--w8jwdsc1a.jp

acm:
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--profile ${PROFILE} \
		--template-body file://templates/acm.yml && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--profile ${PROFILE} \
		--template-file ./templates/acm.yml \
		--stack-name $(PREFIX)-acm \
		--region $(REGION) \
		--parameter-overrides \
		Domain=$(DOMAIN); \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--profile ${PROFILE} \
		--template-file ./templates/acm.yml \
		--stack-name $(PREFIX)-acm \
		--region us-east-1 \
		--parameter-overrides \
		Domain=$(DOMAIN)

vpc:
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--profile ${PROFILE} \
		--template-body file://templates/vpc.yml && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--profile ${PROFILE} \
		--template-file ./templates/vpc.yml \
		--stack-name $(PREFIX)-$(ENV)-vpc \
		--region $(REGION) \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV)

sg:
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--profile ${PROFILE} \
		--template-body file://templates/sg.yml && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--profile ${PROFILE} \
		--template-file ./templates/sg.yml \
		--stack-name $(PREFIX)-$(ENV)-sg \
		--region $(REGION) \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV) \
		VPCStackName=$(PREFIX)-$(ENV)-vpc

rds:
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--profile ${PROFILE} \
		--template-body file://templates/rds.yml && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--profile ${PROFILE} \
		--template-file ./templates/rds.yml \
		--stack-name $(PREFIX)-$(ENV)-rds \
		--region $(REGION) \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV) \
		VPCStackName=$(PREFIX)-$(ENV)-vpc \
		SGStackName=$(PREFIX)-$(ENV)-sg

alb:
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--profile ${PROFILE} \
		--template-body file://templates/alb.yml && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--profile ${PROFILE} \
		--template-file ./templates/alb.yml \
		--stack-name $(PREFIX)-$(ENV)-alb \
		--region $(REGION) \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV) \
		VPCStackName=$(PREFIX)-$(ENV)-vpc \
		SGStackName=$(PREFIX)-$(ENV)-sg \
		ACMStackName=$(PREFIX)-acm

ecr:
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--profile ${PROFILE} \
		--template-body file://templates/ecr.yml && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--profile ${PROFILE} \
		--template-file ./templates/ecr.yml \
		--stack-name $(PREFIX)-$(ENV)-ecr \
		--region $(REGION) \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV)

cloudfront:
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--profile ${PROFILE} \
		--template-body file://templates/cloudfront.yml && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--profile ${PROFILE} \
		--template-file ./templates/cloudfront.yml \
		--stack-name $(PREFIX)-$(ENV)-cloudfront \
		--region us-east-1 \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV) \
		Domain=$(DOMAIN) \
		ACMStackName=$(PREFIX)-acm

ecs:
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--profile ${PROFILE} \
		--template-body file://templates/ecs.yml && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--profile ${PROFILE} \
		--template-file ./templates/ecs.yml \
		--stack-name $(PREFIX)-$(ENV)-ecs \
		--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
		--region $(REGION) \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV) \
		VPCStackName=$(PREFIX)-$(ENV)-vpc \
		SGStackName=$(PREFIX)-$(ENV)-sg \
		RDSStackName=$(PREFIX)-$(ENV)-rds \
		ALBStackName=$(PREFIX)-$(ENV)-alb

systems-manager:
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--template-body file://templates/systems-manager.yml && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--template-file ./templates/systems-manager.yml \
		--stack-name $(PREFIX)-$(ENV)-systems-manager \
		--capabilities CAPABILITY_NAMED_IAM \
		--region $(REGION) \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV) \
		VPCStackName=$(PREFIX)-$(ENV)-vpc \
		SGStackName=$(PREFIX)-$(ENV)-sg

application-pipeline:
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--profile ${PROFILE} \
		--template-body file://templates/code-pipeline/application.yml && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--profile ${PROFILE} \
		--template-file ./templates/code-pipeline/application.yml \
		--stack-name $(PREFIX)-$(ENV)-application-pipeline \
		--capabilities CAPABILITY_NAMED_IAM \
		--region $(REGION) \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV) \
		Owner=souhub \
		Repo=hryk_web

application-api-pipeline:
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--template-body file://templates/code-pipeline/application-api.yml && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--template-file ./templates/code-pipeline/application-api.yml \
		--stack-name $(PREFIX)-$(ENV)-application-api-pipeline \
		--capabilities CAPABILITY_NAMED_IAM \
		--region $(REGION) \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV) \
		ECRStackName=$(PREFIX)-$(ENV)-ecr \
		Owner=souhub \
		AppRepo=hryk_app \
		ChatbotStackName=${PREFIX}-${ENV}-chatbot

sync-db:
ifeq ($(ENV),staging)
ifeq ($(SERVICE), $(filter $(SERVICE), bldg uw))
ifeq ($(SERVICE), bldg)
	$(eval DB_CLUSTER_NAME=$(PREFIX)-production-rds-RDSCluster)
else
	$(eval DB_CLUSTER_NAME=$(PREFIX)-production-rds-UwRDSCluster)
endif
	$(eval DB_CLUSTER_SNAPSHOT_ID=${PREFIX}-$(SERVICE)-production-cluster-snapshot-$(shell date "+%s"))
	$(eval DB_CLUSTER_ID=$(shell $(AWS_COMMAND_PREFIX) cloudformation list-exports \
										--query 'Exports[?Name==`$(DB_CLUSTER_NAME)`].Value' \
										--output=text))
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--template-body file://templates/rds.yml && \
	$(AWS_COMMAND_PREFIX) rds create-db-cluster-snapshot
		--db-cluster-snapshot-identifier $(DB_CLUSTER_SNAPSHOT_ID) \
		--db-cluster-identifier $(DB_CLUSTER_ID) && \
	$(AWS_COMMAND_PREFIX) rds wait db-cluster-snapshot-available \
		--db-cluster-snapshot-identifier $(DB_CLUSTER_SNAPSHOT_ID) && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--template-file ./templates/rds.yml \
		--stack-name $(PREFIX)-$(ENV)-rds \
		--region $(REGION) \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV) \
		VPCStackName=$(PREFIX)-$(ENV)-vpc \
		SGStackName=$(PREFIX)-$(ENV)-sg \
		RDSClusterSnapshotID=$(DB_CLUSTER_SNAPSHOT_ID) \
		Service=$(SERVICE)
else
	@echo "SERVICE must be 'bldg' or 'uw'"
endif
else
	@echo "ENV must be 'staging'"
endif

chatbot:
	$(AWS_COMMAND_PREFIX) cloudformation validate-template \
		--profile ${PROFILE} \
		--template-body file://templates/chatbot.yml && \
	$(AWS_COMMAND_PREFIX) cloudformation deploy \
		--profile ${PROFILE} \
		--template-file ./templates/chatbot.yml \
		--stack-name $(PREFIX)-$(ENV)-chatbot \
		--capabilities CAPABILITY_NAMED_IAM \
		--region $(REGION) \
		--parameter-overrides \
		Prefix=$(PREFIX) \
		Environment=$(ENV)
