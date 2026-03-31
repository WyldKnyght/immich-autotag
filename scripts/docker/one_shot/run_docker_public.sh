#!/bin/bash
# Run immich-autotag using the public Docker image from Docker Hub
# Usage: bash scripts/docker/run_docker_public.sh [config_path] [docker_options]

set -euo pipefail

SCRIPT_DIR="$(
	cd -- "$(dirname "$0")" >/dev/null 2>&1
	pwd -P
)"

DEFAULT_PUBLIC_IMAGE="txemi/immich-autotag:latest"
PUBLIC_IMAGE_NAME="${IMAGE_NAME_OVERRIDE:-$DEFAULT_PUBLIC_IMAGE}"

if [ "${SKIP_DOCKER_PULL:-0}" != "1" ]; then
	echo "Pulling latest image: $PUBLIC_IMAGE_NAME"
	docker pull "$PUBLIC_IMAGE_NAME"
fi

"$SCRIPT_DIR/run_docker_with_config.sh" --image "$PUBLIC_IMAGE_NAME" "$@"
