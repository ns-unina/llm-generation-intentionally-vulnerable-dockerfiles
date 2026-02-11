HUMAN_PATH := Human
GEMINI_PATH := Gemini
GEMINI3_PRO_PATH := Gemini3-Pro
BING_PATH := Bing
GPT3_5_PATH := Gpt3.5
GPT5_2_THINKING_PATH := Gpt5.2-Thinking
GPT5_2_THINKING_WEB_PATH := Gpt5.2-Thinking-Web

DOCKER_RUN := docker run --rm -it --name
DOCKER_BUILD := docker build
CURRENT_DIR := $(shell pwd)
LOGS_DIR := $(CURRENT_DIR)/Logs

LOGS_HUMAN_FILE := $(LOGS_DIR)/$(VULNERABILITY)-human
LOGS_GEMINI_FILE := $(LOGS_DIR)/$(VULNERABILITY)-gemini
LOGS_GEMINI3_PRO_FILE := $(LOGS_DIR)/$(VULNERABILITY)-gemini3-pro
LOGS_BING_FILE := $(LOGS_DIR)/$(VULNERABILITY)-bing
LOGS_GPT3_5_FILE := $(LOGS_DIR)/$(VULNERABILITY)-gpt3.5
LOGS_GPT5_2_FILE := $(LOGS_DIR)/$(VULNERABILITY)-gpt5.2
LOGS_GPT5_2_THINKING_FILE := $(LOGS_DIR)/$(VULNERABILITY)-gpt5.2-thinking
LOGS_GPT5_2_THINKING_WEB_FILE := $(LOGS_DIR)/$(VULNERABILITY)-gpt5.2-thinking-web

HUMAN_POSTFIX := human
GPT3_5_POSTFIX := gpt3.5
GEMINI_POSTFIX := gemini
GEMINI3_PRO_POSTFIX := gemini3-pro
BING_POSTFIX := bing
GPT5_2_POSTFIX := gpt5.2
GPT5_2_THINKING_POSTFIX := gpt5.2-thinking
GPT5_2_THINKING_WEB_POSTFIX := gpt5.2-thinking-web

prepare-logs-folder:
	mkdir -p $(LOGS_DIR)

build-human-single: prepare-logs-folder
	cd $(HUMAN_PATH) && docker build -t $(VULNERABILITY)-human . 2>&1 | tee $(LOGS_HUMAN_FILE)-build.log


down-human-single:
	docker rm -f $(VULNERABILITY)-human || true

run-human-single: build-human-single down-human-single
	echo $(LOGS_HUMAN_FILE)-run.log
	docker run --rm --name $(VULNERABILITY)-human $(DOCKER_OPTS) $(VULNERABILITY)-human 2>&1 | tee $(LOGS_HUMAN_FILE)-run.log

# Gemini targets
build-gemini-single: prepare-logs-folder
	cd $(GEMINI_PATH) && docker build -t $(VULNERABILITY)-gemini . 2>&1 | tee $(LOGS_GEMINI_FILE)-build.log

down-gemini-single:
	docker rm -f $(VULNERABILITY)-gemini || true

run-gemini-single: build-gemini-single down-gemini-single
	echo $(LOGS_GEMINI_FILE)-run.log
	docker run --rm --name $(VULNERABILITY)-gemini $(DOCKER_OPTS) $(VULNERABILITY)-gemini 2>&1 | tee $(LOGS_GEMINI_FILE)-run.log

# Gemini3-Pro targets
build-gemini3-pro-single: prepare-logs-folder
	cd $(GEMINI3_PRO_PATH) && docker build -t $(VULNERABILITY)-gemini3-pro . 2>&1 | tee $(LOGS_GEMINI3_PRO_FILE)-build.log

build-gemini3-pro-bundle: prepare-logs-folder
	cd $(GEMINI3_PRO_PATH)/Bundle && docker build -t $(VULNERABILITY)-gemini3-pro . 2>&1 | tee $(LOGS_GEMINI3_PRO_FILE)-build.log


build-gemini3-pro-package: prepare-logs-folder
	cd $(GEMINI3_PRO_PATH)/Package && docker build -t $(VULNERABILITY)-gemini3-pro-package -f Dockerfile . 2>&1 | tee $(LOGS_GEMINI3_PRO_FILE)-package-build.log

run-gemini3-pro-package: build-gemini3-pro-package down-gemini3-pro-single
	docker run --rm --name $(VULNERABILITY)-gemini3-pro-package $(DOCKER_OPTS) $(VULNERABILITY)-gemini3-pro-package 2>&1 | tee $(LOGS_GEMINI3_PRO_FILE)-package-run.log


build-gemini3-pro-source: prepare-logs-folder
	cd $(GEMINI3_PRO_PATH)/Source && docker build -t $(VULNERABILITY)-gemini3-pro-source -f Dockerfile . 2>&1 | tee $(LOGS_GEMINI3_PRO_FILE)-source-build.log

run-gemini3-pro-source: build-gemini3-pro-source down-gemini3-pro-single
	docker run --rm --name $(VULNERABILITY)-gemini3-pro-source $(DOCKER_OPTS) $(VULNERABILITY)-gemini3-pro-source 2>&1 | tee $(LOGS_GEMINI3_PRO_FILE)-source-run.log

run-gemini3-pro-bundle: build-gemini3-pro-bundle down-gemini3-pro-single
	docker run --rm --name $(VULNERABILITY)-gemini3-pro-bundle $(DOCKER_OPTS) $(VULNERABILITY)-gemini3-pro 2>&1 | tee $(LOGS_GEMINI3_PRO_FILE)-bundle-run.log

down-gemini3-pro-bundle:
	docker rm -f $(VULNERABILITY)-gemini3-pro-bundle || true

down-gemini3-pro-single:
	docker rm -f $(VULNERABILITY)-gemini3-pro || true

down-gemini3-pro-package:
	docker rm -f $(VULNERABILITY)-gemini3-pro-package || true

down-gemini3-pro-source:
	docker rm -f $(VULNERABILITY)-gemini3-pro-source || true

run-gemini3-pro-single: build-gemini3-pro-single down-gemini3-pro-single
	docker run --rm --name $(VULNERABILITY)-gemini3-pro $(DOCKER_OPTS) $(VULNERABILITY)-gemini3-pro 2>&1 | tee $(LOGS_GEMINI3_PRO_FILE)-run.log

# Bing targets
build-bing-single: prepare-logs-folder
	cd $(BING_PATH) && docker build -t $(VULNERABILITY)-bing . 2>&1 | tee $(LOGS_BING_FILE)-build.log

down-bing-single:
	docker rm -f $(VULNERABILITY)-bing || true

run-bing-single: build-bing-single down-bing-single
	echo $(LOGS_BING_FILE)-run.log
	docker run --rm --name $(VULNERABILITY)-bing $(DOCKER_OPTS) $(VULNERABILITY)-bing 2>&1 | tee $(LOGS_BING_FILE)-run.log

# GPT3.5 targets
build-gpt3.5-single: prepare-logs-folder
	cd $(GPT3_5_PATH) && docker build -t $(VULNERABILITY)-gpt3.5 . 2>&1 | tee $(LOGS_GPT3_5_FILE)-build.log

down-gpt3.5-single:
	docker rm -f $(VULNERABILITY)-gpt3.5 || true

run-gpt3.5-single: build-gpt3.5-single down-gpt3.5-single
	echo $(LOGS_GPT3_5_FILE)-run.log
	docker run --rm --name $(VULNERABILITY)-gpt3.5 $(DOCKER_OPTS) $(VULNERABILITY)-gpt3.5 2>&1 | tee $(LOGS_GPT3_5_FILE)-run.log

# GPT5.2-Thinking targets
build-gpt5.2-thinking-single: prepare-logs-folder
	cd $(GPT5_2_THINKING_PATH) && docker build -t $(VULNERABILITY)-gpt5.2-thinking . 2>&1 | tee $(LOGS_GPT5_2_THINKING_FILE)-build.log

down-gpt5.2-thinking-single:
	docker rm -f $(VULNERABILITY)-gpt5.2-thinking || true

run-gpt5.2-thinking-single: build-gpt5.2-thinking-single down-gpt5.2-thinking-single
	echo $(LOGS_GPT5_2_THINKING_FILE)-run.log
	docker run --rm --name $(VULNERABILITY)-gpt5.2-thinking $(DOCKER_OPTS) $(VULNERABILITY)-gpt5.2-thinking 2>&1 | tee $(LOGS_GPT5_2_THINKING_FILE)-run.log

# GPT5.2-Thinking-Web targets
build-gpt5.2-thinking-web-single: prepare-logs-folder
	cd $(GPT5_2_THINKING_WEB_PATH) && docker build -t $(VULNERABILITY)-gpt5.2-thinking-web . 2>&1 | tee $(LOGS_GPT5_2_THINKING_WEB_FILE)-build.log

down-gpt5.2-thinking-web-single:
	docker rm -f $(VULNERABILITY)-gpt5.2-thinking-web || true

run-gpt5.2-thinking-web-single: build-gpt5.2-thinking-web-single down-gpt5.2-thinking-web-single
	echo $(LOGS_GPT5_2_THINKING_WEB_FILE)-run.log
	docker run --rm --name $(VULNERABILITY)-gpt5.2-thinking-web $(DOCKER_OPTS) $(VULNERABILITY)-gpt5.2-thinking-web 2>&1 | tee $(LOGS_GPT5_2_THINKING_WEB_FILE)-run.log

# Docker Compose targets
# Human compose
build-human-compose: prepare-logs-folder
	cd $(HUMAN_PATH) && docker compose -p $(VULNERABILITY) build 2>&1 | tee $(LOGS_HUMAN_FILE)-compose-build.log

run-human-compose: build-human-compose down-human-compose
	echo $(LOGS_HUMAN_FILE)-compose-run.log
	cd $(HUMAN_PATH) && docker compose -p $(VULNERABILITY) up 2>&1 | tee $(LOGS_HUMAN_FILE)-compose-run.log

down-human-compose:
	cd $(HUMAN_PATH) && docker compose -p $(VULNERABILITY) down 2>&1 || true

# Gemini compose
build-gemini-compose: prepare-logs-folder
	cd $(GEMINI_PATH) && docker compose -p $(VULNERABILITY) build 2>&1 | tee $(LOGS_GEMINI_FILE)-compose-build.log

run-gemini-compose: build-gemini-compose down-gemini-compose
	echo $(LOGS_GEMINI_FILE)-compose-run.log
	cd $(GEMINI_PATH) && docker compose -p $(VULNERABILITY) up 2>&1 | tee $(LOGS_GEMINI_FILE)-compose-run.log

down-gemini-compose:
	cd $(GEMINI_PATH) && docker compose -p $(VULNERABILITY) down 2>&1 || true

# Gemini3-Pro compose
build-gemini3-pro-compose: prepare-logs-folder
	cd $(GEMINI3_PRO_PATH) && docker compose -p $(VULNERABILITY) build 2>&1 | tee $(LOGS_GEMINI3_PRO_FILE)-compose-build.log
run-gemini3-pro-compose: build-gemini3-pro-compose down-gemini3-pro-compose
	echo $(LOGS_GEMINI3_PRO_FILE)-compose-run.log
	cd $(GEMINI3_PRO_PATH) && docker compose -p $(VULNERABILITY) up 2>&1 | tee $(LOGS_GEMINI3_PRO_FILE)-compose-run.log

down-gemini3-pro-compose:
	cd $(GEMINI3_PRO_PATH) && docker compose -p $(VULNERABILITY) down 2>&1 || true

build-gemini3-pro-compose-dir: prepare-logs-folder
	cd $(GEMINI3_PRO_PATH)/Compose && docker compose -p $(VULNERABILITY) build 2>&1 | tee $(LOGS_GEMINI3_PRO_FILE)-compose-build.log
run-gemini3-pro-compose-dir: build-gemini3-pro-compose-dir down-gemini3-pro-compose-dir
	echo $(LOGS_GEMINI3_PRO_FILE)-compose-run.log
	cd $(GEMINI3_PRO_PATH)/Compose && docker compose -p $(VULNERABILITY) up 2>&1 | tee $(LOGS_GEMINI3_PRO_FILE)-compose-run.log

down-gemini3-pro-compose-dir:
	cd $(GEMINI3_PRO_PATH)/Compose && docker compose -p $(VULNERABILITY) down 2>&1 || true

# Bing compose
build-bing-compose: prepare-logs-folder
	cd $(BING_PATH) && docker compose -p $(VULNERABILITY) build 2>&1 | tee $(LOGS_BING_FILE)-compose-build.log
run-bing-compose: build-bing-compose down-bing-compose
	echo $(LOGS_BING_FILE)-compose-run.log
	cd $(BING_PATH) && docker compose -p $(VULNERABILITY) up 2>&1 | tee $(LOGS_BING_FILE)-compose-run.log

down-bing-compose:
	cd $(BING_PATH) && docker compose -p $(VULNERABILITY) down 2>&1 || true

# GPT3.5 compose
build-gpt3.5-compose: prepare-logs-folder
	cd $(GPT3_5_PATH) && docker compose -p $(VULNERABILITY) build 2>&1 | tee $(LOGS_GPT3_5_FILE)-compose-build.log
run-gpt3.5-compose: build-gpt3.5-compose down-gpt3.5-compose
	echo $(LOGS_GPT3_5_FILE)-compose-run.log
	cd $(GPT3_5_PATH) && docker compose -p $(VULNERABILITY) up 2>&1 | tee $(LOGS_GPT3_5_FILE)-compose-run.log

down-gpt3.5-compose:
	cd $(GPT3_5_PATH) && docker compose -p $(VULNERABILITY) down 2>&1 || true

# GPT5.2 compose
build-gpt5.2-compose: prepare-logs-folder
	cd $(GPT5_2_PATH) && docker compose -p $(VULNERABILITY) build 2>&1 | tee $(LOGS_GPT5_2_FILE)-compose-build.log
run-gpt5.2-compose: build-gpt5.2-compose down-gpt5.2-compose
	echo $(LOGS_GPT5_2_FILE)-compose-run.log
	cd $(GPT5_2_PATH) && docker compose -p $(VULNERABILITY) up 2>&1 | tee $(LOGS_GPT5_2_FILE)-compose-run.log

down-gpt5.2-compose:
	cd $(GPT5_2_PATH) && docker compose -p $(VULNERABILITY) down 2>&1 || true

# GPT5.2-Thinking compose
build-gpt5.2-thinking-compose: prepare-logs-folder
	cd $(GPT5_2_THINKING_PATH) && docker compose -p $(VULNERABILITY) build 2>&1 | tee $(LOGS_GPT5_2_THINKING_FILE)-compose-build.log
run-gpt5.2-thinking-compose: build-gpt5.2-thinking-compose down-gpt5.2-thinking-compose
	echo $(LOGS_GPT5_2_THINKING_FILE)-compose-run.log
	cd $(GPT5_2_THINKING_PATH) && docker compose -p $(VULNERABILITY) up 2>&1 | tee $(LOGS_GPT5_2_THINKING_FILE)-compose-run.log

down-gpt5.2-thinking-compose:
	cd $(GPT5_2_THINKING_PATH) && docker compose -p $(VULNERABILITY) down 2>&1 || true

# GPT5.2-Thinking-Web compose
build-gpt5.2-thinking-web-compose: prepare-logs-folder
	cd $(GPT5_2_THINKING_WEB_PATH) && docker compose -p $(VULNERABILITY) build 2>&1 | tee $(LOGS_GPT5_2_THINKING_WEB_FILE)-compose-build.log
run-gpt5.2-thinking-web-compose: build-gpt5.2-thinking-web-compose down-gpt5.2-thinking-web-compose
	echo $(LOGS_GPT5_2_THINKING_WEB_FILE)-compose-run.log
	cd $(GPT5_2_THINKING_WEB_PATH) && docker compose -p $(VULNERABILITY) up 2>&1 | tee $(LOGS_GPT5_2_THINKING_WEB_FILE)-compose-run.log

down-gpt5.2-thinking-web-compose:
	cd $(GPT5_2_THINKING_WEB_PATH) && docker compose -p $(VULNERABILITY) down 2>&1 || true

build-gpt3-single: prepare-logs-folder
	cd $(GPT3_PATH) && docker build -t $(VULNERABILITY)-$(GPT3_POSTFIX) . 2>&1 | tee $(LOGS_DIR)/$(VULNERABILITY)-$(GPT3_POSTFIX)-build.log

run-gpt3-single: build-gpt3-single
	cd $(GPT3_PATH) && docker build -t $(VULNERABILITY)-$(GPT3_POSTFIX) . && \
	docker run -d --name $(VULNERABILITY)-$(GPT3_POSTFIX) $(VULNERABILITY)-$(GPT3_POSTFIX)

down-gpt3-single:
	docker rm -f $(VULNERABILITY)-$(GPT3_POSTFIX) || true

rm-gpt3-single: down-gpt3-single
	docker rmi -f $(VULNERABILITY)-$(GPT3_POSTFIX) || true



diff-all:
	mkdir -p Diffs
	diff -r $(HUMAN_PATH) $(GEMINI_PATH) > Diffs/$(VULNERABILITY)-human-vs-gemini.diff || true
	diff -r $(HUMAN_PATH) $(GEMINI3_PRO_PATH) > Diffs/$(VULNERABILITY)-human-vs-gemini3-pro.diff || true
	diff -r $(HUMAN_PATH) $(BING_PATH) > Diffs/$(VULNERABILITY)-human-vs-bing.diff || true
	diff -r $(HUMAN_PATH) $(GPT3_5_PATH) > Diffs/$(VULNERABILITY)-human-vs-gpt3.5.diff || true
	diff -r $(HUMAN_PATH) $(GPT5_2_THINKING_PATH) > Diffs/$(VULNERABILITY)-human-vs-gpt5.2-thinking.diff || true
	diff -r $(HUMAN_PATH) $(GPT5_2_THINKING_WEB_PATH) > Diffs/$(VULNERABILITY)-human-vs-gpt5.2-thinking-web.diff || true


# Take the folder name as an argumnt to avoid hardcoding the vulnerability name in this shared Makefile
SHARED_MK_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
include $(SHARED_MK_DIR)/Preflight.mk
