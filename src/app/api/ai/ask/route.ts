import { NextRequest, NextResponse } from 'next/server';
import { validateInput } from '@/lib/utils/pii-validator';
import { callGemini } from '@/lib/utils/gemini';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { question } = body;

    // Validate question exists
    if (!question || typeof question !== 'string') {
      return NextResponse.json(
        { error: 'invalid_input', message: 'Please provide a question' },
        { status: 400 }
      );
    }

    // Check question length
    if (question.length < 10) {
      return NextResponse.json(
        { error: 'invalid_input', message: 'Please provide more detail in your question' },
        { status: 400 }
      );
    }

    if (question.length > 1000) {
      return NextResponse.json(
        { error: 'invalid_input', message: 'Question is too long. Please keep it under 1000 characters.' },
        { status: 400 }
      );
    }

    // Validate for PII
    const piiCheck = validateInput(question);
    if (!piiCheck.isValid) {
      return NextResponse.json(
        { 
          error: 'pii_detected', 
          message: piiCheck.message || "Please don't share personal information like ID numbers or bank details. We don't need this to help you.",
          piiTypes: piiCheck.piiTypes
        },
        { status: 400 }
      );
    }

    // Call Gemini API
    const response = await callGemini({ question });

    return NextResponse.json({ answer: response.answer });

  } catch (error) {
    console.error('AI API error:', error);
    return NextResponse.json(
      { error: 'ai_unavailable', message: 'AI assistant is temporarily unavailable. Please try again later.' },
      { status: 503 }
    );
  }
}
