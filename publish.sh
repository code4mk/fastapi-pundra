if [ -f .env.deployment ]; then
  set -o allexport
  source .env
  set +o allexport
fi

export PYPI_API_TOKEN=$PYPI_API_TOKEN
uv publish --username __token__ --password $PYPI_API_TOKEN