# -----------------------------
# Preflight (non-blocking, best effort)
# -----------------------------

PREFLIGHT_SLEEP ?= 10
PREFLIGHT_LOG_TAIL ?= 500

POC_PATH ?= Exploit
LOGS_POC_FILE := $(LOGS_DIR)/$(VULNERABILITY)-poc

GEMINI3_PRO_FIXED_PATH := Gemini3-Pro-Fixed
LOGS_GEMINI3_PRO_FIXED_FILE := $(LOGS_DIR)/$(VULNERABILITY)-gemini3-pro-fixed

build-gemini3-pro-fixed-package: prepare-logs-folder
	cd $(GEMINI3_PRO_FIXED_PATH)/Package && docker build -t $(VULNERABILITY)-gemini3-pro-fixed-package -f Dockerfile . 2>&1 | tee $(LOGS_GEMINI3_PRO_FIXED_FILE)-package-build.log

preflight-gemini3-pro-fixed-package: prepare-logs-folder
	@docker rm -f $(VULNERABILITY)-gemini3-pro-fixed-package >/dev/null 2>&1 || true
	@docker run -d --name $(VULNERABILITY)-gemini3-pro-fixed-package $(DOCKER_OPTS) $(VULNERABILITY)-gemini3-pro-fixed-package >/dev/null
	@sleep $(PREFLIGHT_SLEEP)
	@docker logs $(VULNERABILITY)-gemini3-pro-fixed-package 2>&1 | tail -n $(PREFLIGHT_LOG_TAIL) | tee $(LOGS_GEMINI3_PRO_FIXED_FILE)-package-run.log
	@docker stop $(VULNERABILITY)-gemini3-pro-fixed-package >/dev/null 2>&1 || true
	@docker rm $(VULNERABILITY)-gemini3-pro-fixed-package >/dev/null 2>&1 || true


build-gemini3-pro-fixed-source: prepare-logs-folder
	cd $(GEMINI3_PRO_FIXED_PATH)/Source && docker build -t $(VULNERABILITY)-gemini3-pro-fixed-source -f Dockerfile . 2>&1 | tee $(LOGS_GEMINI3_PRO_FIXED_FILE)-source-build.log

preflight-gemini3-pro-fixed-source: prepare-logs-folder
	@docker rm -f $(VULNERABILITY)-gemini3-pro-fixed-source >/dev/null 2>&1 || true
	@docker run -d --name $(VULNERABILITY)-gemini3-pro-fixed-source $(DOCKER_OPTS) $(VULNERABILITY)-gemini3-pro-fixed-source >/dev/null
	@sleep $(PREFLIGHT_SLEEP)
	@docker logs $(VULNERABILITY)-gemini3-pro-fixed-source 2>&1 | tail -n $(PREFLIGHT_LOG_TAIL) | tee $(LOGS_GEMINI3_PRO_FIXED_FILE)-source-run.log
	@docker stop $(VULNERABILITY)-gemini3-pro-fixed-source >/dev/null 2>&1 || true
	@docker rm $(VULNERABILITY)-gemini3-pro-fixed-source >/dev/null 2>&1 || true



# Helpers (do not use @ inside these; callers add @ if needed)
define _preflight_docker_run
docker rm -f $(1) >/dev/null 2>&1 || true
docker run -d --name $(1) $(DOCKER_OPTS) $(2) >/dev/null
sleep $(PREFLIGHT_SLEEP)
docker logs $(1) 2>&1 | tail -n $(PREFLIGHT_LOG_TAIL) | tee $(3)
docker stop $(1) >/dev/null 2>&1 || true
docker rm $(1) >/dev/null 2>&1 || true
endef

define _preflight_compose_up
cd "$(1)" && docker compose -p "$(VULNERABILITY)-$(2)" down >/dev/null 2>&1 || true
cd "$(1)" && docker compose -p "$(VULNERABILITY)-$(2)" up -d >/dev/null
sleep $(PREFLIGHT_SLEEP)
cd "$(1)" && docker compose -p "$(VULNERABILITY)-$(2)" logs --no-color 2>&1 | tail -n $(PREFLIGHT_LOG_TAIL) | tee "$(3)"
cd "$(1)" && docker compose -p "$(VULNERABILITY)-$(2)" down >/dev/null 2>&1 || true
endef

# -----------------------------
# Baseline preflight
# -----------------------------

preflight-human-single: prepare-logs-folder
	@[ -d "$(HUMAN_PATH)" ] || { echo "[SKIP] Human folder not found: $(HUMAN_PATH)"; exit 0; }
	@$(MAKE) build-human-single
	@$(call _preflight_docker_run,$(VULNERABILITY)-human,$(VULNERABILITY)-human,$(LOGS_HUMAN_FILE)-run.log)

preflight-human-compose: prepare-logs-folder
	@[ -d "$(HUMAN_PATH)" ] || { echo "[SKIP] Human folder not found: $(HUMAN_PATH)"; exit 0; }
	@cd "$(HUMAN_PATH)" && ( [ -f "compose.yaml" ] || [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ] ) \
		|| { echo "[SKIP] Human compose file not found in $(HUMAN_PATH)"; exit 0; }
	@$(MAKE) build-human-compose
	@$(call _preflight_compose_up,$(HUMAN_PATH),human-compose,$(LOGS_HUMAN_FILE)-compose-run.log)

preflight-poc: prepare-logs-folder
	@[ -d "$(POC_PATH)" ] || { echo "[SKIP] PoC folder not found: $(POC_PATH)"; exit 0; }
	@cd "$(POC_PATH)" && $(DOCKER_BUILD) -t "$(VULNERABILITY)-poc" . 2>&1 | tee "$(LOGS_POC_FILE)-build.log"
	@$(call _preflight_docker_run,$(VULNERABILITY)-poc,$(VULNERABILITY)-poc,$(LOGS_POC_FILE)-run.log)

preflight-baseline: preflight-human-single preflight-human-compose preflight-poc
	@echo "[OK] Baseline preflight completed."

# -----------------------------
# Gemini preflight (single + compose)
# -----------------------------

preflight-gemini-single: prepare-logs-folder
	@[ -d "$(GEMINI_PATH)" ] || { echo "[SKIP] Gemini folder not found: $(GEMINI_PATH)"; exit 0; }
	@$(MAKE) build-gemini-single
	@$(call _preflight_docker_run,$(VULNERABILITY)-gemini,$(VULNERABILITY)-gemini,$(LOGS_GEMINI_FILE)-run.log)

preflight-gemini-compose: prepare-logs-folder
	@[ -d "$(GEMINI_PATH)" ] || { echo "[SKIP] Gemini folder not found: $(GEMINI_PATH)"; exit 0; }
	@cd "$(GEMINI_PATH)" && ( [ -f "compose.yaml" ] || [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ] ) \
		|| { echo "[SKIP] Gemini compose file not found in $(GEMINI_PATH)"; exit 0; }
	@$(MAKE) build-gemini-compose
	@$(call _preflight_compose_up,$(GEMINI_PATH),gemini-compose,$(LOGS_GEMINI_FILE)-compose-run.log)

# -----------------------------
# Gemini3-Pro preflight (bundle/package/source/single + compose root + compose dir)
# -----------------------------

preflight-gemini3-pro-single: prepare-logs-folder
	@[ -d "$(GEMINI3_PRO_PATH)" ] || { echo "[SKIP] Gemini3-Pro folder not found: $(GEMINI3_PRO_PATH)"; exit 0; }
	@$(MAKE) build-gemini3-pro-single
	@$(call _preflight_docker_run,$(VULNERABILITY)-gemini3-pro,$(VULNERABILITY)-gemini3-pro,$(LOGS_GEMINI3_PRO_FILE)-run.log)

preflight-gemini3-pro-bundle: prepare-logs-folder
	@[ -d "$(GEMINI3_PRO_PATH)/Bundle" ] || { echo "[SKIP] Gemini3-Pro Bundle not found: $(GEMINI3_PRO_PATH)/Bundle"; exit 0; }
	@$(MAKE) build-gemini3-pro-bundle
	@$(call _preflight_docker_run,$(VULNERABILITY)-gemini3-pro-bundle,$(VULNERABILITY)-gemini3-pro,$(LOGS_GEMINI3_PRO_FILE)-bundle-run.log)

preflight-gemini3-pro-package: prepare-logs-folder
	@[ -d "$(GEMINI3_PRO_PATH)/Package" ] || { echo "[SKIP] Gemini3-Pro Package not found: $(GEMINI3_PRO_PATH)/Package"; exit 0; }
	@$(MAKE) build-gemini3-pro-package
	@$(call _preflight_docker_run,$(VULNERABILITY)-gemini3-pro-package,$(VULNERABILITY)-gemini3-pro-package,$(LOGS_GEMINI3_PRO_FILE)-package-run.log)

preflight-gemini3-pro-source: prepare-logs-folder
	@[ -d "$(GEMINI3_PRO_PATH)/Source" ] || { echo "[SKIP] Gemini3-Pro Source not found: $(GEMINI3_PRO_PATH)/Source"; exit 0; }
	@$(MAKE) build-gemini3-pro-source
	@$(call _preflight_docker_run,$(VULNERABILITY)-gemini3-pro-source,$(VULNERABILITY)-gemini3-pro-source,$(LOGS_GEMINI3_PRO_FILE)-source-run.log)

preflight-gemini3-pro-compose: prepare-logs-folder
	@[ -d "$(GEMINI3_PRO_PATH)" ] || { echo "[SKIP] Gemini3-Pro folder not found: $(GEMINI3_PRO_PATH)"; exit 0; }
	@cd "$(GEMINI3_PRO_PATH)" && ( [ -f "compose.yaml" ] || [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ] ) \
		|| { echo "[SKIP] Gemini3-Pro root compose file not found in $(GEMINI3_PRO_PATH)"; exit 0; }
	@$(MAKE) build-gemini3-pro-compose
	@$(call _preflight_compose_up,$(GEMINI3_PRO_PATH),gemini3-pro-compose,$(LOGS_GEMINI3_PRO_FILE)-compose-run.log)

preflight-gemini3-pro-compose-dir: prepare-logs-folder
	@[ -d "$(GEMINI3_PRO_PATH)/Compose" ] || { echo "[SKIP] Gemini3-Pro Compose dir not found: $(GEMINI3_PRO_PATH)/Compose"; exit 0; }
	@cd "$(GEMINI3_PRO_PATH)/Compose" && ( [ -f "compose.yaml" ] || [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ] ) \
		|| { echo "[SKIP] Gemini3-Pro Compose compose file not found in $(GEMINI3_PRO_PATH)/Compose"; exit 0; }
	@$(MAKE) build-gemini3-pro-compose-dir
	@$(call _preflight_compose_up,$(GEMINI3_PRO_PATH)/Compose,gemini3-pro-compose-dir,$(LOGS_GEMINI3_PRO_FILE)-compose-dir-run.log)

preflight-gemini3-pro: \
	preflight-gemini3-pro-single \
	preflight-gemini3-pro-bundle \
	preflight-gemini3-pro-package \
	preflight-gemini3-pro-source \
	preflight-gemini3-pro-compose \
	preflight-gemini3-pro-compose-dir
	@echo "[OK] Gemini3-Pro preflight completed."

# -----------------------------
# Aggregate: everything preflight
# -----------------------------

preflight-all: preflight-baseline preflight-gemini-single preflight-gemini-compose preflight-gemini3-pro
	@echo "[OK] All preflight completed."
