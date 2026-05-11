#!/usr/bin/env python3
"""
theautoroboto.github.io — combined API backend
Handles both AI demos: Ask Brian and FedRAMP Control Explainer.

Local:  ANTHROPIC_API_KEY=your-key python app.py
Render: gunicorn app:app  (PORT and ANTHROPIC_API_KEY set in Render dashboard)
"""

import json
import os
import re
import sys

import anthropic
from flask import Flask, Response, request, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://theautoroboto.github.io", "http://localhost:5001", "http://127.0.0.1:5001"])

# ---------------------------------------------------------------------------
# Ask Brian — system prompt with full career context (prompt-cached)
# ---------------------------------------------------------------------------

_CAREER_CONTEXT = """
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

Red Hat - Security Validation & Cryptography (2026):
  - Orchestrated a cross-vendor FIPS validation effort for OCP on EKS, confirming the integrity
    of the dlopen dispatch path from UBI9-based Go binaries to host-level kernel flags
    (/proc/sys/crypto/fips_enabled). Repo: https://github.com/theautoroboto/fips-validation
  - Designed negative-control testing methodologies to distinguish infrastructure-level enforcement
    from binary-level compliance, mitigating false-positive validation risks.
  - Collaborated with Red Hat cryptographic maintainers to implement hardcoded known-answer tests
    (KAT), ensuring NIST SP 800-131A compliance for AES, RSA, and ECDSA algorithm sets.

Red Hat - FedRAMP & Compliance:
  - Drove FedRAMP Moderate compliance remediation for the ROSA Regional Platform, implementing
    13+ NIST 800-53 Rev 5 controls spanning AU, AC, SC, SI, RA, IA, CA, and CP families.
  - Performed control-by-control mapping of ROSA HCP Terraform modules against NIST 800-53 Rev 5,
    annotating resource definitions with control IDs and surfacing gaps for remediation prioritization.
  - Implemented 10+ NIST 800-53 Rev 5 controls directly in Terraform for the FedRAMP High ATO:
    FIPS endpoint enforcement (IA-07, SC-13), PIV/CAC identity validation (IA-08), KMS CMK
    encryption for CloudWatch and S3 (AU-09), multi-region CloudTrail (AU-12), 365-day log
    retention (AU-11, AC-17), API Gateway access logging (AU-02), system use notification banners
    (AC-08), least-functionality API method settings (CM-07).
  - Led FedRAMP annual assessment workstreams and Significant Change Requests.
  - Spearheaded CONMON remediation by architecting and deploying compliance-monkey across
    Management Clusters to automate security auditing and ensure persistent adherence to baselines.
  - Authored mission-critical FedRAMP architectural diagrams and ADRs for HCP, External DNS
    Operator, and Keycloak identity services.
  - Built a fully automated FedRAMP Compliance Agent (Claude Sonnet sub-agent) evaluating ~700
    Moderate and ~100 High-only NIST 800-53 Rev 5 controls across ROSA Regional Platform repos,
    producing 12 artifacts per run. Repo: https://github.com/theautoroboto/compliance-agent/tree/main

Red Hat - GitOps Pipeline Architecture & Platform Engineering:
  - Architected a 3-tier AWS CodePipeline GitOps hierarchy — a meta-pipeline provisioner that
    dynamically creates, updates, and destroys per-cluster pipelines from Git commits — scaling
    infrastructure delivery to hundreds of independent regional EKS clusters without operator
    intervention.
  - Designed ArgoCD ApplicationSet Matrix Generators for dynamic multi-cluster application
    discovery with hash-pinned sector-based progressive deployment (integration → staging →
    production) from a single config_revision change.
  - Engineered ECS Fargate bootstrap-then-handoff for fully private EKS cluster initialization
    and AWS IoT Core MQTT for zero-trust cross-cluster messaging — eliminating VPC peering and
    Transit Gateway coupling between Regional and Management Clusters.
  - Built a standardized Terraform execution framework enforcing remote S3 state with DynamoDB
    locking, provider version pinning via .terraform.lock.hcl, and a shared module registry.
  - Containerized Terraform execution in Docker images pinned to specific provider versions, run
    through CodeBuild with OIDC-based AWS credential federation — removing tfstate drift.
  - Designed and rolled out a Secret Management framework using AWS Secrets Manager and Vault
    sidecar injection — enforcing least-privilege IAM policies per service and eliminating
    plaintext secrets from all repositories.
  - Built an AWS Sandbox account leasing system in Python backed by DynamoDB state tracking —
    accounts provisioned with scoped IAM roles and SCPs, automatically reclaimed after test
    completion, cutting environment setup from hours to minutes.
  - Architected and implemented AWS PrivateLink for ROSA HCP across all GovCloud regions,
    establishing private connectivity that bypasses the public internet for federal workloads.
  - Deployed Dynatrace Managed Service across FedRAMP environments with OneAgent log forwarding.
  - Integrated backplane-cli and backplane-api with FedRAMP-compliant authentication protocols.
  - Streamlined Hive (https://github.com/openshift/hive) infrastructure by removing redundant
    API components, improving maintainability and leaning the service architecture.
  - Added concurrent regional and management cluster log monitoring to the e2e test suite.

Red Hat - Observability:
  - Deployed a unified Thanos, Prometheus, Alertmanager, and Grafana observability suite using
    parameterized Terraform modules — a single variable change drives a full regional deployment
    with no config duplication.
  - Built Grafana dashboards for API Gateway, RDS, IoT Core, and NAT Gateway.
  - Integrated CloudWatch as a Thanos data source.
  - Engineered a Keycloak log → Splunk pipeline for centralized audit trails and real-time
    security monitoring of the authentication layer.

Red Hat - AI Tooling:
  - Integrated Claude Code deeply into daily engineering workflows as a primary tool.
  - Uses MCP servers for Jira ticket creation/search, Slack messaging, and browser automation.
  - Leverages custom skills for FedRAMP compliance auditing, SREP alert triage, PR review, and
    cluster lifecycle management.
  - Built and maintains a FedRAMP Compliance Agent that evaluates ~700 Moderate and ~100
    High-only NIST 800-53 Rev 5 controls, implementing a 7-step orchestrated workflow: repo
    cloning → control classification → evidence analysis → report generation → PDF conversion →
    Google Drive upload → Jira ticket creation and GitHub PR opening.
  - Integrates Trivy CVE scanning to downgrade Met controls to Gap on CRITICAL/HIGH findings,
    mapping into SI-02, RA-05, and SA-11 assessments.
  - Produces 12 artifacts per run — per-repo and cross-repo executive summaries in Markdown and
    PDF, each with Mermaid control-family heatmaps and delta analysis against prior audits.
  - Uses Claude Code hooks to enforce team standards automatically.
  - Employs the agent SDK to parallelize complex multi-step investigations across the platform.

Red Hat - Leadership (Dec 2023 – Jan 2026):
  - Led a team of 9 SREs using agile methodologies.
  - Responsible for defining and driving projects aligned with business unit priorities.
  - Key initiatives: CVE mitigation, FedRAMP assessments, automating operational toil.
  - Directed 10+ HCP technical training sessions covering Fleet Manager architecture, Service/
    Management cluster dynamics, and automated AMI deployment pipelines.

PREVIOUS ROLE: OneStream Software (February 2021 – November 2021)
=================================================================
Title: First DevOps Engineer — responsible for building the DevOps organization from scratch.
  - In first month: migrated all 70+ repositories from TFS to Bitbucket, then to Azure DevOps
    after discovering Bitbucket couldn't handle the codebase size.
  - Evaluated CircleCI, TravisCI, and Jenkins; selected and implemented Azure DevOps as CI/CD.
  - Implemented SonarQube SAST scanning to ensure code security and standards compliance.
  - Developed Git merge and branching strategies (GitFlow-based) and trained multiple dev teams.

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
    at SpringOne 2019 (YouTube talk available).
  - Monitoring: Defined and implemented SLI dashboards using Splunk, Grafana, AlertManager,
    and Prometheus for 14 PCF foundations.
  - BOSH: Designed a centralized BOSH environment for dashboards and automation across
    disparate production environments.
  - Concourse: Created pipelines to automate all repetitive administrative processes.
  - Certified Kubernetes Administrator (CKA-2000-008308-0100).

PREVIOUS ROLE: Grange Insurance (August 2006 – March 2017, with a gap for other orgs 2007-2008)
================================================================================================
Title: System Administrator / Exchange/Active Directory Engineer.
  - Migrated 3,000 Exchange 2013 on-premise mailboxes to Office 365.
  - Designed and deployed enterprise-wide systems: Active Directory, Exchange, PeopleSoft,
    Internal PKI, KMS, Enterprise FTP (GlobalScape EFT), ADFS, Hitachi Password Manager.
  - Built numerous PowerShell automations: new user provisioning tool, nested AD group reports,
    local admin enforcement tool, employee photo import/ID assignment, PeopleSoft file imports,
    stale account discovery/disable, SharePoint cleanup, mailbox export on offboarding,
    WINS removal across 1,000+ servers, Lync auto-enablement, file server permission tool.
  - Won Grange Star Award and was runner-up for the Golden Trash Can Award.
  - OCS → Lync 2013 migration; Exchange 2007 → 2013 migration; domain upgrades 2003 → 2012.

PREVIOUS ROLE: WD Partners (May 2008 – November 2008)
======================================================
  - IT Infrastructure Admin for a 650-user, 16-DC, 9-location Active Directory environment.
  - Led technical integration of Schorleaf (50-user company acquisition).

PREVIOUS ROLE: BMW Financial Services via Kforce (June 2007 – May 2008)
========================================================================
  - CRM Administrator: Siebel 7.5, Informatica 7.1, BizTalk 2003, .Net web services,
    Middleware environments (100+ servers).

PREVIOUS ROLE: NetJets (February 2005 – August 2006)
======================================================
  - Senior Network Administrator; top-tier support and mentor for production support team.
  - Website administrator for 23 public-facing websites (IIS 6.0, ISA 2004).
  - VMware 2.5 virtual server solution eliminating 30+ physical servers.
  - Terminal server performance project: 40% more users per server.

PREVIOUS ROLE: Cardinal Health (March 2002 – February 2005)
============================================================
  - Senior Messaging Engineer; migrated 30,000+ mailboxes from Sendmail, Lotus Notes,
    Exchange 5.5, and Groupwise to Exchange 2000 across a 128-server, 24x7 global environment.
  - Built the team intranet site using VB.Net, VB Script, JS, C#, ASP.Net, XML, HTML.

PREVIOUS ROLE: CBC Companies (June 1999 – March 2002)
======================================================
  - Started in tech support, promoted to PC Tech, became MCP and Citrix Certified.
  - Administrator of Shiva Modem bank, Novell, NT Domain, Exchange 5.5, Cisco 6513.

FIRST IT JOB: CallTech (June 1998 – June 1999)
===============================================
  - Top-tier support for BellSouth.net ISP. No screen sharing — all verbal.
  - This forged lifelong communication and troubleshooting skills.

PERSONAL BACKGROUND & CHARACTER
================================
  - Grew up in a small suburb of Columbus, Ohio.
  - 1980s: Used mother's Apple IIe from school — first exposure to computing.
  - Summer 1998: Built first PC from parts at Hackers Haven in Columbus. Took weeks to boot.
  - Eagle Scout and Order of the Arrow member. Philmont Scout Ranch 1994: 28 days in the
    mountains of New Mexico with strangers, no adult supervision, working toward a common goal.
  - Football through high school: teamwork, persistence, humility.
    Lives by coach's words: "Act like you have been there."
  - Values: humble, team-oriented, lifelong learner, energized by unsolvable problems
    and open source technology.
"""

ASK_BRIAN_SYSTEM = f"""You are an AI assistant on Brian W. Smith's professional portfolio website. \
You have comprehensive knowledge of Brian's 25+ year career and help visitors learn about him. \
You are enthusiastic, warm, and accurate — Brian's portfolio is the context, so make him look great \
while staying strictly truthful.

Guidelines:
- Speak about Brian in third person (he/him) unless a visitor asks a first-person style question.
- Be specific and concrete — reference real roles, years, technologies, and achievements.
- If asked something not documented below, say you don't have that specific detail.
- Keep responses concise (2–4 paragraphs) unless the visitor requests more detail.
- If asked "why should I hire Brian?" give a genuine, specific, compelling answer.
- Use markdown formatting (bold, bullets) when it improves readability.

{_CAREER_CONTEXT}"""

# ---------------------------------------------------------------------------
# FedRAMP Explainer — system prompt (prompt-cached)
# ---------------------------------------------------------------------------

FEDRAMP_SYSTEM = """You are a FedRAMP and NIST 800-53 Rev 5 compliance expert with extensive \
hands-on experience implementing controls in cloud-native infrastructure — specifically OpenShift, \
Kubernetes, AWS, and Terraform.

When given a NIST 800-53 Rev 5 control identifier, respond in this exact markdown structure:

## [Control Family Abbreviation]-[Number]: [Official Control Name]

**What It Means**
A concise, jargon-free explanation of what the control requires and why it exists. 2-4 sentences.

**In Cloud & SRE Practice**
How this control specifically manifests in modern cloud environments. Reference concrete \
technologies: Kubernetes RBAC, OpenShift SCCs, AWS IAM, CloudTrail, S3, KMS, Terraform, \
CI/CD pipelines, etc. Be specific and practical.

**Implementation Example**
A concrete implementation example with code. Use Terraform HCL, Kubernetes YAML, AWS CLI, \
or shell commands where appropriate. Show real-world patterns, not pseudocode.

**What Assessors Look For**
3-5 bullet points covering: key evidence artifacts required, common compliance gaps, and \
gotchas that trip up engineers during FedRAMP assessments.

---
Keep it focused and technical. Target audience: senior SREs and platform engineers who are \
technically expert but may be new to FedRAMP assessment processes."""


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _get_client():
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        return None, {'error': 'ANTHROPIC_API_KEY is not set'}, 500
    return anthropic.Anthropic(api_key=api_key), None, None


def _sse_stream(gen_fn):
    return Response(
        stream_with_context(gen_fn()),
        content_type='text/event-stream',
        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'},
    )


def _sse_generate(client, model, system_blocks, messages, max_tokens=1024):
    try:
        with client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            system=system_blocks,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"
    except anthropic.AuthenticationError:
        yield f"data: {json.dumps({'text': 'Error: Invalid API key.'})}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'text': f'Error: {e}'})}\n\n"
        yield "data: [DONE]\n\n"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route('/api/ask', methods=['POST'])
def ask_brian():
    client, err, status = _get_client()
    if err:
        return err, status

    data = request.get_json(silent=True) or {}
    messages = data.get('messages', [])

    clean = [
        {'role': m['role'], 'content': str(m['content'])[:2000]}
        for m in messages[-20:]
        if isinstance(m, dict) and m.get('role') in ('user', 'assistant') and m.get('content')
    ]
    if not clean or clean[-1]['role'] != 'user':
        return {'error': 'Last message must be from user'}, 400

    system_blocks = [{'type': 'text', 'text': ASK_BRIAN_SYSTEM,
                      'cache_control': {'type': 'ephemeral'}}]

    return _sse_stream(lambda: _sse_generate(
        client, 'claude-haiku-4-5-20251001', system_blocks, clean, max_tokens=1024
    ))


@app.route('/api/fedramp', methods=['POST'])
def fedramp_explain():
    client, err, status = _get_client()
    if err:
        return err, status

    data = request.get_json(silent=True) or {}
    control_id = data.get('control_id', '').strip().upper()

    if not control_id:
        return {'error': 'control_id is required'}, 400
    if not re.match(r'^[A-Z]{2,3}-\d{1,2}(\(\d+\))?$', control_id):
        return {'error': f'"{control_id}" does not look like a valid NIST 800-53 control ID'}, 400

    system_blocks = [{'type': 'text', 'text': FEDRAMP_SYSTEM,
                      'cache_control': {'type': 'ephemeral'}}]
    messages = [{'role': 'user', 'content': f'Explain NIST 800-53 Rev 5 control: {control_id}'}]

    return _sse_stream(lambda: _sse_generate(
        client, 'claude-sonnet-4-6', system_blocks, messages, max_tokens=1200
    ))


@app.route('/health')
def health():
    return {'status': 'ok'}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print('Warning: ANTHROPIC_API_KEY is not set.', file=sys.stderr)
    port = int(os.environ.get('PORT', 5001))
    print(f'API server starting on http://localhost:{port}')
    app.run(host='0.0.0.0', port=port, debug=False)
