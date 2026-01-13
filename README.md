# Azure DevOps PR Scan Pipeline
This pipeline installs Python dependencies via your Azure Artifacts feed and runs `pip-audit` for vulnerability scanning. It does **not** promote packages to any view; packages will remain cached in the feed's `@Local` view.

## Setup Steps

1. **Azure Artifacts Feed**
   - Project: `CTDP-SLT`
   - Feed: `CDP-TST`
   - Ensure PyPI is configured as an upstream source so installs through the feed cache into `@Local`.

2. **Pipeline Configuration**
   - Add this `azure-pipelines.yml` to your repo.
   - Enable **Allow scripts to access the OAuth token** in pipeline settings.

3. **Permissions**
   - The pipeline needs read access to the feed. Typically, the project Build Service identity already has this.

4. **Usage**
   - On PR, the pipeline will:
     - Install dependencies from your feed.
     - Run `pip-audit` to check for vulnerabilities.

## Variables
- `FEED_SIMPLE_URL` is set to the project-scoped feed's PyPI simple endpoint:
  `https://pkgs.dev.azure.com/<ORG>/CTDP-SLT/_packaging/CDP-TST/pypi/simple/`
