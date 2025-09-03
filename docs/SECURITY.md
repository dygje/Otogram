# Security Policy

## Supported Versions

We actively support the following versions of Otogram:

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.x.x   | :x:                |

## Reporting a Vulnerability

The Otogram team takes security bugs seriously. We appreciate your efforts to responsibly disclose your findings, and will make every effort to acknowledge your contributions.

### How to Report a Security Vulnerability?

If you believe you have found a security vulnerability in Otogram, please report it to us through coordinated disclosure.

**Please do not report security vulnerabilities through public GitHub issues, discussions, or pull requests.**

Instead, please send an email to: **security@otogram.project** (or create a private security advisory on GitHub)

Please include as much of the information listed below as you can to help us better understand and resolve the issue:

* Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
* Full paths of source file(s) related to the manifestation of the issue
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit the issue

This information will help us triage your report more quickly.

### What to Expect

After you submit a report, we will:

1. **Acknowledge** receipt of your vulnerability report within 48 hours
2. **Confirm** the problem and determine the affected versions within 5 business days  
3. **Audit** code to find any potential similar problems
4. **Prepare** fixes for all supported releases
5. **Release** new versions and publish security advisories

## Security Best Practices

When using Otogram, please follow these security best practices:

### Environment Security
* **Never commit credentials** to version control
* **Use strong passwords** for Telegram accounts
* **Enable 2FA** on your Telegram account
* **Keep dependencies updated** using dependabot alerts
* **Run in isolated environments** (Docker/containers)

### Telegram Security
* **Use Bot tokens securely** - never share or expose them
* **Validate all inputs** from Telegram messages
* **Implement rate limiting** to prevent abuse
* **Monitor for suspicious activity** in logs
* **Use webhook URLs with SSL** if using webhooks

### Database Security
* **Secure MongoDB instance** with authentication
* **Use connection strings** with credentials in environment variables
* **Keep MongoDB updated** to latest stable version
* **Enable MongoDB logging** for audit trails
* **Backup data regularly** and test restore procedures

### Deployment Security
* **Use HTTPS/TLS** for all communications
* **Keep system updated** with security patches
* **Use firewall rules** to restrict network access
* **Monitor system logs** for security events
* **Use secrets management** for production deployments

## Security Features

Otogram includes several built-in security features:

* **Input validation** using Pydantic models
* **Error handling** to prevent information disclosure  
* **Rate limiting** and blacklist management
* **Secure credential handling** through environment variables
* **Logging and monitoring** capabilities
* **Database connection security** with MongoDB authentication

## Vulnerability Disclosure Timeline

* **Day 0**: Security report received
* **Day 1-2**: Initial response and acknowledgment
* **Day 3-7**: Vulnerability confirmed and assessed
* **Day 8-21**: Fix developed and tested
* **Day 22-30**: Coordinated release and disclosure

We aim to resolve critical vulnerabilities within 30 days of initial report.

## Security Hall of Fame

We recognize security researchers who help improve Otogram's security:

<!-- Contributors who responsibly disclosed security issues will be listed here -->

*No security issues have been reported yet.*

## Contact

For questions about this security policy, please contact:
* **GitHub Issues**: For general security discussions (non-sensitive)
* **Email**: security@otogram.project (for sensitive security matters)
* **GitHub Security Advisories**: For private vulnerability reporting

---

Thank you for helping keep Otogram and our users safe! 🔒