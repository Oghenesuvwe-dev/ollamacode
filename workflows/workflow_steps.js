# OllamaCode Pipedream Workflow
# This file defines the steps for the Pipedream workflow.

# Step 1: Trigger
# Type: GitHub App - New or Updated Pull Request
# Exports: steps.trigger.event.body

# Step 2: Clone & Fetch Diff
import { execa } from 'execa';
import fs from 'fs/promises';

export const cloneRepo = defineComponent({
    async run({ steps, $ }) {
        const repoFullName = steps.trigger.event.body.repository.full_name;
        const branch = steps.trigger.event.body.pull_request.head.ref;
        const repoUrl = `https://x-access-token:${process.env.GITHUB_TOKEN}@github.com/${repoFullName}.git`;

        // Clean up previous runs
        await fs.rm('/tmp/repo', { recursive: true, force: true });

        // Clone depth 1 for speed
        await execa('git', ['clone', '--depth', '1', '--branch', branch, repoUrl, '/tmp/repo']);

        // Get the diff
        // Note: In a real PR event, we might want to fetch the base and head to diff properly
        // For simplicity, we assume we are at HEAD and want to see what changed in the last commit(s)
        // A better approach for PRs is fetching the merge base.

        const { stdout: diff } = await execa('git', ['diff', 'HEAD~1', 'HEAD'], { cwd: '/tmp/repo' });

        return {
            repoPath: '/tmp/repo',
            diffContent: diff,
            prNumber: steps.trigger.event.body.number,
            repoName: repoFullName
        };
    }
});

// Step 3: Static Analysis
// Note: This assumes 'semgrep' and 'bandit' are available in the environment or installed via npm/pip in a previous step
import { execa } from 'execa';

export const staticAnalysis = defineComponent({
    async run({ steps, $ }) {
        const targetDir = steps.clone_repo.repoPath;
        const findings = [];

        // 1. Semgrep
        try {
            // In a real Pipedream env, you might need to install semgrep first or use a container
            const { stdout } = await execa('semgrep', ['scan', '--config=auto', '--json', '--quiet', targetDir]);
            const results = JSON.parse(stdout).results;
            findings.push(...results.map(r => ({ tool: 'semgrep', ...r })));
        } catch (e) {
            console.log("Semgrep skipped or failed:", e.message);
        }

        // 2. Bandit (Python only)
        try {
            const { stdout } = await execa('bandit', ['-r', targetDir, '-f', 'json', '-q']);
            const results = JSON.parse(stdout).results;
            findings.push(...results.map(r => ({ tool: 'bandit', ...r })));
        } catch (e) {
            console.log("Bandit skipped or failed:", e.message);
        }

        return { findings };
    }
});

// Step 4: AI Review (Call Backend)
import axios from 'axios';

export const aiReview = defineComponent({
    async run({ steps, $ }) {
        const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'; // Needs to be a public URL for Pipedream

        const payload = {
            repo_name: steps.clone_repo.repoName,
            pr_number: steps.clone_repo.prNumber,
            diff: steps.clone_repo.diffContent,
            findings: steps.static_analysis.findings
        };

        try {
            const response = await axios.post(`${backendUrl}/api/v1/review`, payload, {
                headers: {
                    'Authorization': `Bearer ${process.env.BACKEND_API_KEY}`
                }
            });
            return response.data;
        } catch (e) {
            throw new Error(`Backend review failed: ${e.message}`);
        }
    }
});
