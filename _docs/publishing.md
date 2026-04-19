# Publishing `fastapi-pundra` to PyPI

This guide covers the full workflow for building and publishing the package using **uv** and **Hatch** (hatchling build backend).

---

## Prerequisites

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- A [PyPI account](https://pypi.org/account/register/)
- A PyPI API token (see [Generate a PyPI API Token](#1-generate-a-pypi-api-token))

---

## Project Structure

```
fastapi-pundra/
├── src/
│   └── fastapi_pundra/      # package source
├── docs/
├── pyproject.toml            # build config (hatchling backend)
├── publish.sh                # publish helper script
├── LICENSE
├── README.md
└── .python-version
```

Key sections in `pyproject.toml`:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/fastapi_pundra"]
```

---

## Step-by-Step Publishing Flow

### 1. Generate a PyPI API Token

1. Log in to [pypi.org](https://pypi.org/manage/account/).
2. Go to **Account Settings → API tokens**.
3. Click **Add API token**.
   - **Token name**: anything descriptive (e.g. `fastapi-pundra-deploy`)
   - **Scope**: limit to the `fastapi-pundra` project (or "Entire account" for a first-time upload)
4. Copy the token — it starts with `pypi-` and is shown only once.

### 2. Store the Token

Create a `.env` file in the project root (already gitignored):

```bash
# .env
PYPI_API_TOKEN=pypi-xxxxxxxxxxxxxxxxxxxx
```

> **Never commit this file.** Make sure `.env` is listed in `.gitignore`.

### 3. Bump the Version

Edit the version in `pyproject.toml`:

```toml
[project]
version = "0.0.24"   # increment appropriately
```

Follow [semantic versioning](https://semver.org/):

| Change type | Example | Version bump |
|---|---|---|
| Breaking / incompatible API change | Removed a public function | `0.0.x` → `0.1.0` |
| New feature, backward compatible | Added a new helper module | `0.0.x` → `0.0.x+1` (pre-1.0) |
| Bug fix | Fixed a typo in output | `0.0.23` → `0.0.24` |

### 4. Clean Previous Builds

```bash
rm -rf dist/ build/ *.egg-info src/*.egg-info
```

### 5. Build the Package

```bash
uv build
```

This uses the `hatchling` backend defined in `pyproject.toml` and produces two files inside `dist/`:

```
dist/
├── fastapi_pundra-0.0.24-py3-none-any.whl   # wheel (binary)
└── fastapi_pundra-0.0.24.tar.gz              # sdist (source)
```

You can verify the build contents:

```bash
# List what's inside the wheel
unzip -l dist/fastapi_pundra-*.whl

# List what's inside the sdist
tar tzf dist/fastapi_pundra-*.tar.gz
```

### 6. Publish to PyPI

#### Option A — Using `publish.sh` (recommended)

```bash
chmod +x publish.sh
./publish.sh
```

The script loads the token from `.env` and runs:

```bash
uv publish --username __token__ --password $PYPI_API_TOKEN
```

#### Option B — Manual one-liner

```bash
uv publish --username __token__ --password pypi-xxxxxxxxxxxxxxxxxxxx
```

#### Option C — Build + Publish in one go

```bash
uv build && uv publish --username __token__ --password $PYPI_API_TOKEN
```

### 7. Verify the Release

```bash
# Check on PyPI
open https://pypi.org/project/fastapi-pundra/

# Install in a fresh environment to test
uv venv /tmp/test-pundra && source /tmp/test-pundra/bin/activate
pip install fastapi-pundra==0.0.24
python -c "import fastapi_pundra; print('OK')"
```

---

## Publishing to TestPyPI (Dry Run)

Always test with [TestPyPI](https://test.pypi.org/) before a real release.

### 1. Get a TestPyPI token

Register at [test.pypi.org](https://test.pypi.org/account/register/) and create an API token the same way.

### 2. Publish to TestPyPI

```bash
uv publish --publish-url https://test.pypi.org/legacy/ \
  --username __token__ \
  --password pypi-xxxxxxxxxxxxxxxxxxxx
```

### 3. Install from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  fastapi-pundra==0.0.24
```

The `--extra-index-url` flag allows dependencies (e.g. `requests`, `bcrypt`) to resolve from the real PyPI.

---

## Quick Reference — Full Release Checklist

```bash
# 1. Make sure you're on a clean main branch
git checkout main && git pull

# 2. Bump version in pyproject.toml

# 3. Clean old artifacts
rm -rf dist/ build/ *.egg-info src/*.egg-info

# 4. Build
uv build

# 5. (Optional) Test publish
uv publish --publish-url https://test.pypi.org/legacy/ \
  --username __token__ --password $TEST_PYPI_TOKEN

# 6. Publish to PyPI
./publish.sh            # or: uv publish --username __token__ --password $PYPI_API_TOKEN

# 7. Tag the release
git add pyproject.toml
git commit -m "release: v0.0.24"
git tag v0.0.24
git push origin main --tags
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `HTTPError: 400 ... file already exists` | You're re-uploading the same version. Bump the version in `pyproject.toml` and rebuild. |
| `HTTPError: 403 Forbidden` | Token is invalid or scoped to a different project. Regenerate it. |
| `uv: command not found` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Build includes unwanted files | Check `[tool.hatch.build.targets.sdist] exclude` in `pyproject.toml`. |
| `ModuleNotFoundError` after install | Verify `[tool.hatch.build.targets.wheel] packages` points to the right directory. |

---

## Useful Links

- [uv docs — Publishing](https://docs.astral.sh/uv/guides/publish/)
- [Hatch — Build configuration](https://hatch.pypa.io/latest/config/build/)
- [PyPI — Managing projects](https://pypi.org/help/#project-release-notifications)
- [Semantic Versioning](https://semver.org/)
