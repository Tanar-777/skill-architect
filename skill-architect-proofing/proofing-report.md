<!-- skill-proofing -->
![skill-proofing](https://img.shields.io/badge/skill--proofing-%E2%9D%8C+failed-red)
**Last checked:** 2026-03-16 | **Score:** 4/7 categories passed
<!-- end skill-proofing -->

## skill-proofing report — skill-architect-proofing

> This skill is **not ready to share on Git**.

### ❌ Hard Failures (must fix before sharing)

- [CREDENTIALS] Private key block detected in `proofing.py`
- [SENSITIVE_PATH] ~/.ssh (SSH keys directory) reference found in `proofing-report.md`
- [SENSITIVE_PATH] ~/.aws (AWS credentials) reference found in `proofing-report.md`
- [SENSITIVE_PATH] /etc/passwd (system users) reference found in `proofing-report.md`
- [SENSITIVE_PATH] /etc/shadow (system passwords) reference found in `proofing-report.md`
- [SENSITIVE_PATH] ~/.env (environment variables file) reference found in `proofing-report.md`
- [SENSITIVE_PATH] ~/.ssh (SSH keys directory) reference found in `README.md`
- [SENSITIVE_PATH] ~/.aws (AWS credentials) reference found in `README.md`
- [SENSITIVE_PATH] /etc/passwd (system users) reference found in `README.md`
- [SENSITIVE_PATH] ~/.env (environment variables file) reference found in `README.md`
- [SENSITIVE_PATH] ~/.ssh (SSH keys directory) reference found in `proofing.py`
- [SENSITIVE_PATH] ~/.aws (AWS credentials) reference found in `proofing.py`
- [SENSITIVE_PATH] /etc/passwd (system users) reference found in `proofing.py`
- [SENSITIVE_PATH] /etc/shadow (system passwords) reference found in `proofing.py`
- [SENSITIVE_PATH] ~/.env (environment variables file) reference found in `proofing.py`
- [UNSAFE_BASH] `rm -rf (destructive delete)` found in `proofing.py`
- [UNSAFE_BASH] `curl | bash (arbitrary code execution)` found in `proofing.py`
- [UNSAFE_BASH] `eval() (arbitrary code execution)` found in `proofing.py`
- [UNSAFE_BASH] `sudo (privilege escalation)` found in `proofing.py`
- [UNSAFE_BASH] `os.system() (unsafe shell execution)` found in `proofing.py`
