# DevSecOps Project – SonarCloud Integration

## 📌 Project Overview
This project demonstrates the integration of **SonarCloud** with a GitHub repository as part of a DevSecOps workflow.  
The goal was to implement **Continuous Integration (CI)** and **Continuous Security (CS)** by scanning code quality, vulnerabilities, and maintainability issues.

We initially configured GitHub Actions workflows (`ci-cd.yml` and `sonar.yml`) to automate scans. However, during testing, the scans did **not successfully execute via GitHub Actions**. Instead, **SonarCloud performed the code analysis directly on its platform** after being connected to the GitHub repository.

---

## ⚙️ Workflow Summary
1. **Code pushed to GitHub**  
   Developers commit and push changes to the repository.

2. **SonarCloud Integration with GitHub**  
   The GitHub repository was linked directly with SonarCloud.  
   → This allowed SonarCloud to automatically fetch and scan code from the repo whenever changes were pushed.

3. **Analysis in SonarCloud UI**  
   Instead of scanning within GitHub Actions, the scans were executed **inside SonarCloud’s own environment**, and results were available on the SonarCloud dashboard.

---

## 🚀 Key Tools Used
- **GitHub** → Version control and code hosting.
- **GitHub Actions** → (Configured, but scans didn’t pass successfully).
- **SonarCloud** → Static Application Security Testing (SAST), code quality, and vulnerability scanning.

---

## 🔍 Observations
- The GitHub Actions workflows (`ci-cd.yml` and `sonar.yml`) were present but did not succeed in running scans.
- Despite this, **SonarCloud successfully scanned the repository** because of the direct GitHub → SonarCloud integration.
- This shows that even without GitHub Actions, SonarCloud can independently perform scans when linked with a repository.

# Getting the token of the Sonarcloud and keeping it in secrets in the github repo:

  ![image alt](https://github.com/Dpk808/Sonarcube/blob/main/screenshots/1.1_sonarcloud_token.png) 
  

# And when the project is connected to the Sonarcloud, we can analyze the project for ulnerabilities from the sonarcloud platform itself:

  ![image alt](https://github.com/Dpk808/Sonarcube/blob/main/screenshots/1.5_sonarcloud%20results.png) 
  

---

## ✅ Lessons Learned
- GitHub Actions can be configured to trigger SonarCloud scans, but direct repo integration provides a fallback scanning method.
- SonarCloud’s direct GitHub integration ensures scans run even if CI pipelines fail.
- In real-world DevSecOps pipelines, combining both (GitHub Actions + SonarCloud direct integration) provides better visibility and automation.

---

## 📊 Results
- Code was scanned for **bugs, vulnerabilities, security hotspots, and maintainability issues**.
- Results were available on the **SonarCloud dashboard** rather than in GitHub Actions logs.

---

## 🔗 References
- [SonarCloud Documentation](https://docs.sonarcloud.io/)
- [GitHub Actions with SonarCloud](https://docs.sonarcloud.io/ci-integration/github-actions/)
