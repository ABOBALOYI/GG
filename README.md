# GrantGuide AI

GrantGuide AI is an automated assistance system for South African social grants information. It operates as an independent, unofficial guidance assistant designed to translate verified, publicly available grant information into plain, actionable guidance.

## Core Principles

- **Independence**: Not affiliated with SASSA or the government.
- **Privacy**: Does not request or store sensitive personal data.
- **Accuracy**: Relies on specific Knowledge Base retrieval (RAG).
- **Clarity**: Uses plain English suitable for all literacy levels.

## Tech Stack
- **Framework**: Next.js 15+ (App Router)
- **Styling**: Vanilla CSS (Premium Aesthetics)
- **AI Engine**: Vercel AI SDK + Google Gemini
- **Language**: TypeScript

## Features
- **Knowledge Base RAG**: Retrieves verified grant info to prevent hallucinations.
- **Strict Persona**: Enforced "unofficial guide" rules via System Prompt.
- **Dynamic Content**: Grant detail pages generated from a central data source.
- **Premium UI**: Glassmorphism, animations, and responsive design.

## Getting Started

1.  **Set up Environment**:
    Create a `.env` file in the root and add your Google Gemini API Key:
    ```env
    GOOGLE_GENERATIVE_AI_API_KEY=your_api_key_here
    ```

2.  **Run the development server**:

```bash
npm run dev
```

3.  Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Deployment

### GitHub
1.  Initialize git (if not already): `git init`
2.  Add files: `git add .`
3.  Commit: `git commit -m "chore: prepare for deployment and adsense"`
4.  Create a repo on GitHub and push.

### AWS Amplify
1.  Go to the [AWS Amplify Console](https://console.aws.amazon.com/amplify/home).
2.  Connect your GitHub repository.
3.  Amplify will automatically detect Next.js.
4.  **Environment Variables**: Ensure you add `GOOGLE_GENERATIVE_AI_API_KEY` in the Amplify Console under "Environment variables".
5.  **Build Settings**: Amplify's default settings for Next.js should work. Ensure the build command is `npm run build` and the base directory is `.next`.

## AdSense Readiness
- **Privacy Policy**: Updated with mandatory AdSense disclosures.
- **`ads.txt`**: Located in `public/ads.txt`. (Update with your pub-ID after approval).
- **Sitemap**: Automatically generated at `/sitemap.xml` for crawler discovery.
- **Layout**: AdSense script integrated in `src/app/layout.tsx`.

## System Prompt

The operational persona and rules are defined in `SYSTEM_PROMPT.md`.
