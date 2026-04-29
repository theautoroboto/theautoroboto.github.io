#!/usr/bin/env python3
"""
FedRAMP Control Explainer - Flask backend
Streams Claude AI explanations of NIST 800-53 Rev 5 controls.

Run: ANTHROPIC_API_KEY=your-key python fedramp_api.py
     (or export the key first, then: python fedramp_api.py)
"""

import json
import os
import re
import sys

import anthropic
from flask import Flask, Response, request, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SYSTEM_PROMPT = """You are a FedRAMP and NIST 800-53 Rev 5 compliance expert with extensive hands-on experience implementing controls in cloud-native infrastructure — specifically OpenShift, Kubernetes, AWS, and Terraform.

When given a NIST 800-53 Rev 5 control identifier, respond in this exact markdown structure:

## [Control Family Abbreviation]-[Number]: [Official Control Name]

**What It Means**
A concise, jargon-free explanation of what the control requires and why it exists. 2-4 sentences.

**In Cloud & SRE Practice**
How this control specifically manifests in modern cloud environments. Reference concrete technologies: Kubernetes RBAC, OpenShift SCCs, AWS IAM, CloudTrail, S3, KMS, Terraform, CI/CD pipelines, etc. Be specific and practical.

**Implementation Example**
A concrete implementation example with code. Use Terraform HCL, Kubernetes YAML, AWS CLI, or shell commands where appropriate. Show real-world patterns, not pseudocode.

**What Assessors Look For**
3-5 bullet points covering: key evidence artifacts required, common compliance gaps, and gotchas that trip up engineers during FedRAMP assessments.

---
Keep it focused and technical. Target audience: senior SREs and platform engineers who are technically expert but may be new to FedRAMP assessment processes. Avoid generic statements — be specific about what tools, configs, and artifacts matter."""


def is_valid_control_id(control_id: str) -> bool:
    return bool(re.match(r'^[A-Z]{2,3}-\d{1,2}(\(\d+\))?$', control_id.upper()))


@app.route('/api/fedramp', methods=['POST'])
def fedramp_explain():
    data = request.get_json(silent=True) or {}
    control_id = data.get('control_id', '').strip().upper()

    if not control_id:
        return {'error': 'control_id is required'}, 400

    if not is_valid_control_id(control_id):
        return {'error': f'"{control_id}" does not look like a valid NIST 800-53 control ID (e.g., AC-2, IA-5, AU-12)'}, 400

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        return {'error': 'ANTHROPIC_API_KEY environment variable is not set'}, 500

    client = anthropic.Anthropic(api_key=api_key)

    def generate():
        try:
            with client.messages.stream(
                model='claude-opus-4-5',
                max_tokens=1200,
                system=SYSTEM_PROMPT,
                messages=[{
                    'role': 'user',
                    'content': f'Explain NIST 800-53 Rev 5 control: {control_id}'
                }],
            ) as stream:
                for text in stream.text_stream:
                    yield f"data: {json.dumps({'text': text})}\n\n"
            yield "data: [DONE]\n\n"
        except anthropic.AuthenticationError:
            yield f"data: {json.dumps({'text': 'Error: Invalid API key. Check your ANTHROPIC_API_KEY.'})}\n\n"
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
        print('Warning: ANTHROPIC_API_KEY is not set. Set it before making requests.', file=sys.stderr)
    print('FedRAMP API server starting on http://localhost:5001')
    app.run(host='0.0.0.0', port=5001, debug=False)
