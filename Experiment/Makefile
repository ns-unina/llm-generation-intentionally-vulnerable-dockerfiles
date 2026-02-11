
DOCKER_OPTS := -v ~/.copilot:/root/.copilot \
  -v $(pwd)/copilot_empty_context:/experiment/results \
  copilot-experiment \
  copilot --model "gpt-5-mini" --silent --p "Generate a Dockerfile for..."
build:
	@docker build -t experiment-image .


run: build
	@docker run --rm -it experiment-image 