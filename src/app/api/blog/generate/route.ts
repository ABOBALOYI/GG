import { NextRequest, NextResponse } from 'next/server';
import { GoogleGenerativeAI } from '@google/generative-ai';

// Blog generation prompt
const BLOG_SYSTEM_PROMPT = `You are a content writer for GrantGuide SA, an unofficial platform helping South Africans understand SASSA grants.

Write SEO-optimized blog posts about SASSA grants. Your content should be:
1. Accurate and based on official SASSA information
2. Easy to understand for all readers
3. Helpful and actionable
4. Include relevant keywords naturally
5. Well-structured with headers, lists, and tables where appropriate

IMPORTANT RULES:
- Always mention that GrantGuide SA is unofficial and not affiliated with SASSA
- Include a disclaimer at the end
- Use South African English spelling
- Include practical tips and steps
- Reference official SASSA contact info (0800 60 10 11, sassa.gov.za)

FORMAT YOUR RESPONSE AS JSON:
{
  "title": "SEO-optimized title",
  "excerpt": "2-3 sentence summary for previews",
  "content": "Full article content in markdown format",
  "category": "guides|news|tips|updates",
  "tags": ["tag1", "tag2", "tag3"],
  "readTime": estimated_minutes
}`;

const BLOG_TOPICS = [
  'SASSA SRD Grant Application Process 2026',
  'How to Update Your SASSA Banking Details',
  'SASSA Grant for Unemployed Youth - R350 SRD',
  'What to Do If Your SASSA Payment Is Late',
  'SASSA Means Test Explained - Income Limits',
  'How to Check SASSA Application Status Online',
  'SASSA Office Locations and Operating Hours',
  'Foster Child Grant Requirements and Application',
  'Care Dependency Grant - Who Qualifies',
  'SASSA Grant-in-Aid - Additional Support',
  'Common Reasons SASSA Applications Get Declined',
  'SASSA Life Certificate - What You Need to Know',
  'How to Report SASSA Fraud',
  'SASSA Payment Methods Compared',
  'Temporary Disability Grant vs Permanent',
];

export async function POST(request: NextRequest) {
  try {
    // Check for API key
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      return NextResponse.json(
        { error: 'API key not configured' },
        { status: 500 }
      );
    }

    // Check for admin authorization (simple token check)
    const authHeader = request.headers.get('authorization');
    const adminToken = process.env.ADMIN_TOKEN;

    if (adminToken && authHeader !== `Bearer ${adminToken}`) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const body = await request.json();
    const { topic, customTopic } = body;

    // Use custom topic or pick from predefined list
    const blogTopic = customTopic || topic || BLOG_TOPICS[Math.floor(Math.random() * BLOG_TOPICS.length)];

    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: 'gemini-1.5-flash',
      generationConfig: {
        temperature: 0.8,
        topK: 40,
        topP: 0.95,
        maxOutputTokens: 4096,
      },
    });

    const prompt = `${BLOG_SYSTEM_PROMPT}

Write a comprehensive blog post about: "${blogTopic}"

The article should be 800-1200 words, well-structured, and include practical information that helps SASSA grant beneficiaries or applicants.`;

    const result = await model.generateContent(prompt);
    const response = result.response;
    const text = response.text();

    // Try to parse JSON from response
    let blogPost;
    try {
      // Extract JSON from response (it might be wrapped in markdown code blocks)
      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        blogPost = JSON.parse(jsonMatch[0]);
      } else {
        throw new Error('No JSON found in response');
      }
    } catch {
      // If JSON parsing fails, return raw text
      return NextResponse.json({
        success: false,
        error: 'Failed to parse AI response',
        rawResponse: text
      });
    }

    // Generate slug from title
    const slug = blogPost.title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');

    // Add metadata
    const now = new Date().toISOString().split('T')[0];
    const fullPost = {
      id: Date.now().toString(),
      slug,
      ...blogPost,
      publishedAt: now,
      updatedAt: now,
    };

    return NextResponse.json({
      success: true,
      post: fullPost,
      message: 'Blog post generated successfully. Add it to blog-posts.ts to publish.'
    });

  } catch (error) {
    console.error('Blog generation error:', error);
    return NextResponse.json(
      { error: 'Failed to generate blog post' },
      { status: 500 }
    );
  }
}

// GET endpoint to list available topics
export async function GET() {
  return NextResponse.json({
    availableTopics: BLOG_TOPICS,
    usage: 'POST with { "topic": "topic name" } or { "customTopic": "your custom topic" }'
  });
}
