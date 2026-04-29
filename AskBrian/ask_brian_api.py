#!/usr/bin/env python3
"""
Ask Brian - Flask backend
Multi-turn AI chat about Brian W. Smith's career.
Uses Claude with prompt caching on the career context.

Run: ANTHROPIC_API_KEY=your-key python ask_brian_api.py
"""

import json
import os
import sys

import anthropic
from flask import Flask, Response, request, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Comprehensive career context — cached on first request, free on subsequent ones.
CAREER_CONTEXT = """
ABOUT BRIAN W. SMITH
====================
Brian W. Smith is a Principal Site Reliability Engineer with 25+ years of experience building
and operating enterprise-scale infrastructure. He specializes in cloud-native platforms, FedRAMP
compliance, and Infrastructure as Code. Currently he delivers a FedRAMP High OpenShift solution
on AWS at Red Hat. He thrives in high-performing teams where collaboration, ownership, and
technical excellence are the standard. He is energized by open source technology, automation,
and solving problems others consider unsolvable.

CURRENT ROLE: Red Hat (November 2021 – Present)
================================================
Title progression: Senior SRE → Senior SRE Functional Lead (Dec 2023) → Principal SRE Team Lead
(Jan 2025) → Principal SRE (Jan 2026 – present).

Red Hat - FedRAMP & Compliance:
  - Implemented 10+ NIST 800-53 Rev 5 controls directly in Terraform as part of the FedRAMP High
    ATO effort for ROSA (Red Hat OpenShift Service on AWS) Regional Platform.
  - Controls implemented: FIPS endpoint enforcement (IA-07, SC-13), PIV/CAC identity validation
    (IA-08), KMS CMK encryption for CloudWatch and S3 (AU-09), multi-region CloudTrail (AU-12),
    365-day log retention (AU-11, AC-17), API Gateway access logging (AU-02), system use
    notification banners (AC-08), least-functionality API method settings (CM-07).
  - Led FedRAMP annual assessment workstreams and Significant Change Requests.
  - Designed and deployed an AI agent workflow using Claude to automate FedRAMP control
    evaluation and reporting, significantly reducing manual assessment toil.

Red Hat - Platform & Infrastructure:
  - Joined as a greenfield hire to build the ROSA Regional Platform from scratch on AWS GovCloud.
  - Championed Infrastructure as Code, establishing Terraform as the foundation for all platform
    provisioning.
  - Designed centralized multi-environment AWS CodeBuild deployment pipelines for regional and
    management clusters with environment-scoped validation, retry logic, and AWS Parameter Store
    integration.
  - Added concurrent regional and management cluster log monitoring to the e2e test suite.
    Contributed cluster profile and test job definitions to openshift/release (ROSAENG-34).

Red Hat - Observability:
  - Deployed Thanos and the Thanos-operator for distributed platform observability.
  - Built Grafana dashboards for API Gateway, RDS, IoT Core, and NAT Gateway.
  - Integrated CloudWatch as a Thanos data source.

Red Hat - AI Tooling:
  - Integrated Claude Code deeply into daily engineering workflows as a primary tool.
  - Uses MCP servers for Jira ticket creation/search, Slack messaging, and browser automation.
  - Leverages custom skills for FedRAMP compliance auditing, SREP alert triage, PR review, and
    cluster lifecycle management.
  - Built and maintains a FedRAMP agent that evaluates NIST 800-53 controls and generates
    compliance reports.
  - Uses Claude Code hooks to enforce team standards automatically.
  - Employs the agent SDK to parallelize complex multi-step investigations across the platform.

Red Hat - Leadership (Dec 2023 – Jan 2026):
  - Led a team of 9 SREs using agile methodologies.
  - Responsible for defining and driving projects aligned with business unit priorities.
  - Key initiatives: CVE mitigation, FedRAMP assessments, automating operational toil.

PREVIOUS ROLE: OneStream Software (February 2021 – November 2021)
=================================================================
Title: First DevOps Engineer — responsible for building the DevOps organization from scratch.
  - In first month: migrated all 70+ repositories from TFS to Bitbucket, then to Azure DevOps
    after discovering Bitbucket couldn't handle the codebase size.
  - Evaluated CircleCI, TravisCI, and Jenkins; selected and implemented Azure DevOps as CI/CD.
  - Implemented SonarQube SAST scanning to ensure code security and standards compliance.
  - Developed Git merge and branching strategies (GitFlow-based) and trained multiple dev teams.
  - Gave internal presentations on Git workflows, merge strategies, and branching best practices.

CERTIFICATIONS (achieved during 2020):
  - Azure DevOps Engineer Expert (AZ-400) — December 2020
  - Azure Solutions Architect Expert (AZ-303/304) — October 2020
  - Azure Administrator Associate (AZ-104) — October 2020

ROLE BETWEEN ONESTREAM: Immuta (August 2020 – February 2021)
=============================================================
  - Joined for culture fit — described teammates as "absolutely amazing."

PREVIOUS ROLE: Fiserv (March 2017 – August 2020)
=================================================
Title: Senior System Engineer Lead → Cloud Platform Team.
  - Designed and built 16 Pivotal Cloud Foundry (PCF) foundations supporting over 7,000
    microservices.
  - Led the Cloud Platform team formation and training using agile methodologies.
  - Kubernetes/Helm/Prometheus automation: Built an automated pipeline letting dev teams
    self-provision Kubernetes clusters with Prometheus, Grafana, and AlertManager via Helm.
    Clusters auto-expired via daily cleanup pipelines. (GitHub: kubernetes-onboarding)
  - Azure initiative: Led the PaaS effort deploying Fiserv into Azure using PKS (Pivotal
    Kubernetes Service). Presented "Putting Pivotal Platform to the Hybrid Cloud Test: Azure"
    at SpringOne 2019 (YouTube talk available). Published azure-terraform repo on GitHub.
  - Monitoring: Defined and implemented SLI dashboards using Splunk, Grafana, AlertManager,
    and Prometheus for 14 PCF foundations.
  - BOSH: Designed a centralized BOSH environment for dashboards and automation across
    disparate production environments. (GitHub: standalone-bosh)
  - Version tracking: Built a process exporting and comparing all platform configurations.
    (GitHub: pcf-env-report)
  - Concourse: Created pipelines to automate all repetitive administrative processes.
  - Certified Kubernetes Administrator (CKA-2000-008308-0100).

PREVIOUS ROLE: Grange Insurance (August 2006 – March 2017, with a gap 2006-2008 at other orgs)
================================================================================================
Title: System Administrator / Exchange/Active Directory Engineer.
  - Migrated 3,000 Exchange 2013 on-premise mailboxes to Office 365.
  - Designed and deployed enterprise-wide systems: Active Directory, Exchange, PeopleSoft,
    Internal PKI, KMS, Enterprise FTP (GlobalScape EFT), ADFS, Hitachi Password Manager.
  - Built numerous PowerShell automations: new user provisioning tool, nested AD group reports,
    local admin enforcement tool, employee photo import/ID assignment, PeopleSoft file imports,
    stale account discovery/disable, SharePoint cleanup, mailbox export on employee offboarding,
    WINS removal across 1,000+ servers, Lync auto-enablement, file server permission tool,
    scratch folder cleanup, and Novell migration scripts.
  - Won Grange Star Award and was runner-up for the Golden Trash Can Award.
  - OCS → Lync 2013 migration; Exchange 2007 → 2013 migration; domain upgrades 2003 → 2012.
  - ProofPoint cloud anti-spam deployment.
  - Reengineered enterprise monitoring environment with a custom .Net web application.

PREVIOUS ROLE: WD Partners (May 2008 – November 2008)
======================================================
  - IT Infrastructure Admin for a 650-user, 16-DC, 9-location Active Directory environment.
  - Led technical integration of Schorleaf (50-user company acquisition).
  - Implemented Websense remote filtering, WSUS patching automation, Trend spam replacement.
  - Migrated 380GB Exchange Public Folder store to new hardware without service disruption.

PREVIOUS ROLE: BMW Financial Services via Kforce (June 2007 – May 2008)
========================================================================
  - CRM Administrator: Siebel 7.5, Informatica 7.1, BizTalk 2003, .Net web services,
    Middleware environments (100+ servers).
  - Expanded post-deployment Web Service tests from 65 to 132 XML request strings.
  - Implemented Microsoft Operations Manager for proactive monitoring.
  - Completed full yearly disaster recovery scenario.
  - Replaced 6 web servers in F5 pools without production disruption.

PREVIOUS ROLE: Grange Insurance – First Stint (August 2006 – June 2007)
========================================================================
  - SMS, Exchange 2003, and FTP administration.
  - Deployed GlobalScape EFT consolidating 30+ FTP servers across the enterprise.

PREVIOUS ROLE: NetJets (February 2005 – August 2006)
======================================================
  - Senior Network Administrator; top-tier support and mentor for production support team.
  - Website administrator for 23 public-facing websites (IIS 6.0, ISA 2004).
  - Implemented Microsoft Operations Manager 2005 across 120 servers.
  - VMware 2.5 virtual server solution eliminating 30+ physical servers.
  - Terminal server performance project: 40% more users per server.
  - Migrated 3,000+ clients to Trend Micro OfficeScan 7.0.
  - Restructured web servers from DMZ to internal Cisco CSS web farm.

PREVIOUS ROLE: Cardinal Health (March 2002 – February 2005)
============================================================
  - Senior Messaging Engineer on the Tier II messaging team.
  - Core objective: migrated 30,000+ mailboxes from Sendmail, Lotus Notes, Exchange 5.5,
    and Groupwise to Exchange 2000 across a 128-server, 24x7 global environment.
  - Built the team intranet site using VB.Net, VB Script, JS, C#, ASP.Net, XML, HTML.
  - Implemented Microsoft Operations Manager 2000 and Spotlight on Exchange.
  - Built the custom OWA webpage.
  - Returned to Franklin University part-time (2003).

PREVIOUS ROLE: CBC Companies (June 1999 – March 2002)
======================================================
  - Started in tech support for lending software (A+ cert, survived Y2K).
  - Promoted to PC Tech: Windows NT book, became MCP (Microsoft Certified Professional).
  - Administrator of Shiva Modem bank, Novell 3.x/4.11, NT Domain, Exchange 5.5,
    Cisco 6513, Citrix Metaframe 1.8. Also became Citrix Certified.

FIRST IT JOB: CallTech (June 1998 – June 1999)
===============================================
  - Top-tier support for BellSouth.net ISP.
  - Guided first-time users through Windows 3.1, 95, dial-up, ISDN troubleshooting.
  - No screen sharing — all verbal. This forged lifelong communication skills.

PERSONAL BACKGROUND & CHARACTER
================================
  - Grew up in a small suburb of Columbus, Ohio.
  - 1980s: Used mother's Apple IIe from school — first exposure to computing.
  - Early 1990s: Windows 3.1 laptop, 2400 baud modem, BBS ("The Pit").
  - Mid 1990s: Family's first PC; AOL; self-taught HTML, VB Script, Windows NT.
  - Summer 1998: Built first PC from parts bought at Hackers Haven in Columbus. He
    described this as "one of the most impactful opportunities I've been provided."
    Booted Windows 95 and connected via 14.4 modem. Took weeks. He was proud.
  - 1996: Started college at DeVry (didn't love JCL/COBOL), moved to community college,
    then Franklin University. Took a break to self-teach. Returned part-time in 2003.
  - Eagle Scout and Order of the Arrow member. Worked at Philmont Scout Ranch in 1994:
    28 days alone in the mountains of New Mexico with peers he'd never met, no adult
    supervision, working toward a common goal. This shaped his leadership fundamentally.
  - Football (middle school through high school): Instilled teamwork, persistence, humility.
    Lives by coach's words: "Act like you have been there."
  - Values: humble, team-oriented, lifelong learner, prefers giving credit to the team,
    energized by unsolvable problems and open source technology.
  - Describes the Cardinal Health team as the gold standard he has measured every team
    against since. Very few have compared.
"""

SYSTEM_PROMPT = f"""You are an AI assistant on Brian W. Smith's professional portfolio website. \
You have comprehensive knowledge of Brian's 25+ year career and help visitors learn about him. \
You are enthusiastic, warm, and accurate — Brian's portfolio is the context, so make him look great \
while staying strictly truthful.

Guidelines:
- Speak about Brian in third person (he/him) unless a visitor asks a first-person question like "tell me about yourself."
- Be specific and concrete — reference real roles, years, technologies, and achievements from his history.
- If asked something not documented in Brian's history below, say you don't have that specific detail.
- Keep responses appropriately concise (2–4 paragraphs) unless the visitor requests more detail.
- You may elaborate on the technologies Brian has worked with — you know what those technologies do.
- If asked "why should I hire Brian?" or similar, give a genuine, specific, compelling answer.
- Use markdown formatting (bold, bullets, headers) when it improves readability.

{CAREER_CONTEXT}"""


@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json(silent=True) or {}
    messages = data.get('messages', [])

    if not messages or not isinstance(messages, list):
        return {'error': 'messages array is required'}, 400

    # Sanitize: only pass role/content, max 20 turns to prevent abuse
    clean_messages = [
        {'role': m['role'], 'content': str(m['content'])[:2000]}
        for m in messages[-20:]
        if isinstance(m, dict) and m.get('role') in ('user', 'assistant') and m.get('content')
    ]

    if not clean_messages or clean_messages[-1]['role'] != 'user':
        return {'error': 'Last message must be from user'}, 400

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        return {'error': 'ANTHROPIC_API_KEY environment variable is not set'}, 500

    client = anthropic.Anthropic(api_key=api_key)

    def generate():
        try:
            with client.messages.stream(
                model='claude-haiku-4-5-20251001',
                max_tokens=1024,
                system=[
                    {
                        'type': 'text',
                        'text': SYSTEM_PROMPT,
                        # Cache the large career context — free on every call after the first
                        'cache_control': {'type': 'ephemeral'},
                    }
                ],
                messages=clean_messages,
            ) as stream:
                for text in stream.text_stream:
                    yield f"data: {json.dumps({'text': text})}\n\n"
            yield "data: [DONE]\n\n"
        except anthropic.AuthenticationError:
            yield f"data: {json.dumps({'text': 'Error: Invalid API key.'})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'text': f'Error: {str(e)}'})}\n\n"
            yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        content_type='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        },
    )


@app.route('/health')
def health():
    return {'status': 'ok'}


if __name__ == '__main__':
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print('Warning: ANTHROPIC_API_KEY is not set.', file=sys.stderr)
    print('Ask Brian API server starting on http://localhost:5002')
    app.run(host='0.0.0.0', port=5002, debug=False)
