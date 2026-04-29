#!/usr/bin/env python3
"""
Ask Brian - Flask backend (local dev)
Multi-turn AI chat about Brian W. Smith's career, powered by Gemini.

Run: GEMINI_API_KEY=your-key python ask_brian_api.py
"""

import json
import os
import sys
import time

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from flask import Flask, Response, request, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

Red Hat - FedRAMP & Compliance:
  - Implemented 10+ NIST 800-53 Rev 5 controls directly in Terraform as part of the FedRAMP High
    ATO effort for ROSA (Red Hat OpenShift Service on AWS) Regional Platform.
  - Controls: FIPS endpoint enforcement (IA-07, SC-13), PIV/CAC identity validation (IA-08),
    KMS CMK encryption for CloudWatch and S3 (AU-09), multi-region CloudTrail (AU-12), 365-day
    log retention (AU-11, AC-17), API Gateway access logging (AU-02), system use notification
    banners (AC-08), least-functionality API method settings (CM-07).
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
  - Contributed cluster profile and test job definitions to openshift/release (ROSAENG-34).

Red Hat - Observability:
  - Deployed Thanos and the Thanos-operator for distributed platform observability.
  - Built Grafana dashboards for API Gateway, RDS, IoT Core, and NAT Gateway.
  - Integrated CloudWatch as a Thanos data source.

Red Hat - AI Tooling:
  - Integrated Claude Code deeply into daily engineering workflows as a primary tool.
  - Uses MCP servers for Jira, Slack, and browser automation.
  - Leverages custom skills for FedRAMP auditing, SREP alert triage, PR review, and cluster
    lifecycle management.
  - Uses Claude Code hooks to enforce team standards automatically.
  - Employs the agent SDK to parallelize complex multi-step investigations.

Red Hat - Leadership (Dec 2023 – Jan 2026):
  - Led a team of 9 SREs using agile methodologies.
  - Key initiatives: CVE mitigation, FedRAMP assessments, automating operational toil.

PREVIOUS ROLE: OneStream Software (February 2021 – November 2021)
=================================================================
  - First DevOps Engineer; built the DevOps organization from scratch.
  - Migrated 70+ repositories from TFS → Bitbucket → Azure DevOps.
  - Implemented Azure DevOps CI/CD, SonarQube SAST, and GitFlow-based branching strategies.

CERTIFICATIONS (2020): AZ-400, AZ-303/304, AZ-104.

PREVIOUS ROLE: Fiserv (March 2017 – August 2020)
=================================================
  - Built 16 Pivotal Cloud Foundry foundations supporting 7,000+ microservices.
  - Kubernetes self-service onboarding pipeline with Helm, Prometheus, Grafana, AlertManager.
  - Led Azure PaaS initiative using PKS; presented at SpringOne 2019.
  - SLI dashboards with Splunk, Grafana, AlertManager, Prometheus for 14 foundations.
  - Certified Kubernetes Administrator (CKA-2000-008308-0100).

PREVIOUS ROLE: Grange Insurance (August 2006 – March 2017)
===========================================================
  - Exchange/AD administrator; migrated 3,000 mailboxes to Office 365.
  - Built extensive PowerShell automations across AD, Exchange, SharePoint, PeopleSoft.
  - Won Grange Star Award.

EARLIER ROLES:
  - WD Partners (2008): IT Infrastructure Admin, 650 users, 9 locations.
  - BMW Financial (2007-2008): CRM Admin, 100+ server middleware environment.
  - NetJets (2005-2006): Senior Network Admin, 23 public websites, VMware virtualization.
  - Cardinal Health (2002-2005): Migrated 30,000+ mailboxes to Exchange 2000.
  - CBC Companies (1999-2002): PC Tech, became MCP and Citrix Certified.
  - CallTech (1998-1999): First IT job, ISP support for BellSouth.net.

PERSONAL:
  - Grew up in Columbus, Ohio. Eagle Scout. Philmont Scout Ranch 1994.
  - Football through high school: "Act like you have been there."
  - Built first PC in 1998. Self-taught HTML, VB Script, Windows NT.
  - Values: humble, team-oriented, lifelong learner.
"""

SYSTEM_PROMPT = f"""You are an AI assistant on Brian W. Smith's professional portfolio website.
You have comprehensive knowledge of Brian's 25+ year career and help visitors learn about him.
Be enthusiastic, warm, and accurate — make him look great while staying strictly truthful.

Guidelines:
- Speak about Brian in third person (he/him) unless asked a first-person style question.
- Be specific — reference real roles, years, technologies, and achievements.
- If asked something not documented below, say you don't have that specific detail.
- Keep responses concise (2–4 paragraphs) unless the visitor requests more detail.
- If asked "why should I hire Brian?" give a genuine, specific, compelling answer.
- Use markdown formatting (bold, bullets) when it improves readability.

{_CAREER_CONTEXT}"""


@app.route('/api/ask', methods=['POST'])
def ask():
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return {'error': 'GEMINI_API_KEY environment variable is not set'}, 500

    data = request.get_json(silent=True) or {}
    messages = data.get('messages', [])

    clean = [
        {'role': m['role'], 'content': str(m['content'])[:2000]}
        for m in messages[-20:]
        if isinstance(m, dict) and m.get('role') in ('user', 'assistant') and m.get('content')
    ]
    if not clean or clean[-1]['role'] != 'user':
        return {'error': 'Last message must be from user'}, 400

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        system_instruction=SYSTEM_PROMPT,
    )

    gemini_history = [
        {'role': 'model' if m['role'] == 'assistant' else 'user',
         'parts': [m['content']]}
        for m in clean[:-1]
    ]
    last_message = clean[-1]['content']

    def generate():
        for attempt in range(3):
            try:
                chat = model.start_chat(history=gemini_history)
                for chunk in chat.send_message(last_message, stream=True):
                    text = getattr(chunk, 'text', None)
                    if text:
                        yield f"data: {json.dumps({'text': text})}\n\n"
                yield "data: [DONE]\n\n"
                return
            except ResourceExhausted:
                if attempt < 2:
                    time.sleep(2 ** attempt)
                else:
                    yield f"data: {json.dumps({'text': '⚠️ Gemini rate limit hit. Wait a moment and try again.'})}\n\n"
                    yield "data: [DONE]\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'text': f'Error: {e}'})}\n\n"
                yield "data: [DONE]\n\n"
                return

    return Response(
        stream_with_context(generate()),
        content_type='text/event-stream',
        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'},
    )


@app.route('/health')
def health():
    return {'status': 'ok'}


if __name__ == '__main__':
    if not os.environ.get('GEMINI_API_KEY'):
        print('Warning: GEMINI_API_KEY is not set.', file=sys.stderr)
    print('Ask Brian API starting on http://localhost:5002')
    app.run(host='0.0.0.0', port=5002, debug=False)
