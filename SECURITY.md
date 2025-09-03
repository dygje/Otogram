# Security Policy

## Supported Versions

We support security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via:

1. **GitHub Security Advisories** (preferred)
   - Go to the repository's Security tab
   - Click "Report a vulnerability"
   - Fill out the form with details

2. **Private Communication**
   - Create a private issue if Security Advisories are not available
   - Contact maintainers directly if needed

## What to Report

Please report any security concerns including:

### High Priority
- **Credential exposure**: API keys, tokens, passwords in logs or code
- **Authentication bypass**: Ways to bypass bot authentication
- **Privilege escalation**: Unauthorized access to admin functions  
- **Data injection**: SQL injection, command injection, etc.
- **Unauthorized access**: Access to restricted Telegram groups/data

### Medium Priority
- **Information disclosure**: Exposure of sensitive system information
- **Denial of service**: Ways to crash or overwhelm the system
- **Configuration issues**: Insecure default settings
- **Dependency vulnerabilities**: Known CVEs in dependencies

### What We Handle
- Security issues in the core application
- Configuration and deployment guidance
- Dependency security updates
- Authentication and authorization flaws

### What We Don't Handle
- Issues in third-party dependencies (report to upstream)
- Telegram platform security (report to Telegram)
- MongoDB security (report to MongoDB)
- Infrastructure security (AWS, VPS, etc.)

## Security Best Practices

### For Users
- **Credentials**: Store API keys and tokens securely in `.env` file
- **Permissions**: Use dedicated Telegram account with minimal permissions
- **Network**: Run behind firewall, restrict database access
- **Updates**: Keep dependencies updated for security patches
- **Monitoring**: Monitor logs for suspicious activity

### For Developers
- **Environment**: Never commit secrets to version control
- **Input validation**: Validate all user inputs
- **Error handling**: Don't expose sensitive data in error messages
- **Logging**: Don't log credentials or sensitive data
- **Dependencies**: Use exact versions, audit regularly

## Response Process

1. **Acknowledgment**: We'll acknowledge receipt within 24 hours
2. **Assessment**: Initial assessment within 72 hours
3. **Investigation**: Detailed investigation and impact analysis
4. **Fix Development**: Develop and test security fixes
5. **Disclosure**: Coordinate disclosure timeline with reporter
6. **Release**: Release security update with advisory

## Security Updates

Security updates will be:
- Released as patch versions (e.g., 2.0.1 → 2.0.2)
- Documented in `CHANGELOG.md` with security note
- Announced in repository releases
- Tagged with security advisory if applicable

## Recognition

We appreciate security researchers who:
- Follow responsible disclosure
- Provide clear reproduction steps
- Work with us on fix timeline
- Allow us to properly test fixes

We may recognize contributors in:
- Security advisory acknowledgments
- Repository contributors list
- Project documentation (with permission)

## Dependencies Security

We regularly audit dependencies using:
- Automated security scanning
- Dependency update monitoring
- CVE tracking for critical components

Critical dependencies monitored:
- `pyrofork`: Telegram MTProto client
- `python-telegram-bot`: Bot API client
- `motor`/`pymongo`: Database drivers
- `pydantic`: Data validation
- `aiofiles`: File operations

## Contact

For urgent security matters, use GitHub Security Advisories or create a private issue.

For general security questions, use GitHub Discussions with `security` label.

---

**Remember**: Security is everyone's responsibility. Thank you for helping keep this project secure!