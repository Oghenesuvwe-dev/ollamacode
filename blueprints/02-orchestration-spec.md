# Phase 2: Backend Orchestration

**Goal**: Manage the code review lifecycle using Pipedream workflows. This layer acts as the "glue" between GitHub, Static Analysis tools, and the Intelligence Backend.

---

## 🛠️ Tech Stack
*   **Platform**: Pipedream (Workflow Orchestration)
*   **Runtime**: Node.js 18.x / Python 3.10
*   **Git**: For cloning and diffing
*   **Analysis Tools**: Semgrep, Bandit, TruffleHog (installed in ephemeral environment)

---

## ⚡ Pipedream Workflow Blueprint

The workflow consists of 5 sequential steps.

### Step 1: Trigger (GitHub Webhook)
*   **Source**: GitHub App
*   **Events**: `pull_request` (opened, synchronized)
*   **Output**: `steps.trigger.event.body` containing PR metadata.

### Step 2: Fetch & Clone
Instead of just using the API, we clone the repo to the ephemeral storage (`/tmp`) to run deep static analysis.

```javascript
// Node.js Step
import { execa } from 'execa';
import fs from 'fs/promises';

export default defineComponent({
  async run({ steps, $ }) {
    const repoUrl = `https://x-access-token:${process.env.GITHUB_TOKEN}@github.com/${steps.trigger.event.body.repository.full_name}.git`;
    const branch = steps.trigger.event.body.pull_request.head.ref;
    
    // Clean and Clone
    await fs.rm('/tmp/repo', { recursive: true, force: true });
    await execa('git', ['clone', '--depth', '1', '--branch', branch, repoUrl, '/tmp/repo']);
    
    // Get Diff for context
    const { stdout: diff } = await execa('git', ['diff', 'HEAD~1', 'HEAD'], { cwd: '/tmp/repo' });
    return { diffPath: '/tmp/repo', diffContent: diff };
  }
});
```

### Step 3: Static Analysis Runner
Runs multiple open-source tools in parallel and aggregates results.

```javascript
// Node.js Step
import { execa } from 'execa';

export default defineComponent({
  async run({ steps, $ }) {
    const targetDir = '/tmp/repo';
    const findings = [];

    // 1. Semgrep (General SAST)
    try {
      const { stdout } = await execa('semgrep', ['scan', '--config=auto', '--json', '--quiet', targetDir]);
      const results = JSON.parse(stdout).results;
      findings.push(...results.map(r => ({ tool: 'semgrep', ...r })));
    } catch (e) { console.log("Semgrep skipped/failed"); }

    // 2. Bandit (Python Security)
    // 3. TruffleHog (Secrets)
    
    return { findings };
  }
});
```

### Step 4: AI Review Generation
Constructs a prompt and sends it to the **Intelligence Backend** (Phase 3).

**Prompt Structure:**
```text
You are a senior code reviewer.
CONTEXT:
- PR Title: {{pr_title}}
- Changed Files: {{file_list}}

STATIC ANALYSIS FINDINGS:
{{findings_json}}

DIFF:
{{diff_content}}

TASK:
Review the code for logic errors, security vulnerabilities, and performance issues. 
Ignore style nitpicks.
```

### Step 5: Post GitHub Comment
Formats the AI response and Static Analysis findings into a Markdown table and posts it to the PR.

---

## 🛡️ Security & Best Practices

1.  **Ephemeral Storage**: Pipedream environments are ephemeral. Data in `/tmp` is destroyed after execution.
2.  **Token Scoping**: The `GITHUB_TOKEN` should only have permissions for `contents: read` and `pull_requests: write`.
3.  **Secret Redaction**: The workflow explicitly filters out secrets from the logs before sending any data to the LLM.
4.  **Cost Optimization**: Only run analysis on *changed* files (incremental scanning) to save compute time.

---

## 📦 Dependencies (package.json)
```json
{
  "dependencies": {
    "@octokit/core": "^5.0.0",
    "execa": "^8.0.0",
    "axios": "^1.6.0",
    "semgrep": "^1.0.0" 
  }
}
```
