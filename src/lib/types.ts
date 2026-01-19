// Grant types
export interface Grant {
  id: number;
  slug: string;
  name: string;
  description: string;
  eligibilityCriteria: EligibilityCriteria;
  disqualifiers: string[];
  incomeThresholds: IncomeThreshold[];
  applicationSteps: ApplicationStep[];
  processingTimeline: string;
  commonMistakes: string[];
  updatedAt: string;
}

export interface EligibilityCriteria {
  ageRequirement?: string;
  citizenshipRequirement: string;
  residencyRequirement: string;
  incomeRequirement?: string;
  additionalCriteria: string[];
}

export interface IncomeThreshold {
  applicantType: string;
  maxIncome: number;
}

export interface ApplicationStep {
  stepNumber: number;
  title: string;
  description: string;
}

// Payment types
export interface PaymentCycle {
  id: number;
  month: number;
  year: number;
  grantId: number;
  grantName: string;
  paymentDates: PaymentDate[];
  notes?: string;
}

export interface PaymentDate {
  method: 'cash' | 'bank' | 'post_office';
  startDate: string;
  endDate: string;
}

// Status types
export interface StatusCode {
  id: number;
  code: string;
  officialMeaning: string;
  simplifiedMeaning: string;
  realWorldPatterns?: string;
  recommendedActions: string[];
  relatedStatusCodes: string[];
}

// Appeal types
export interface AppealGuide {
  id: number;
  grantId: number;
  grantSlug: string;
  grantName: string;
  appealSteps: AppealStep[];
  requiredDocuments: string[];
  timeline: string;
  commonPitfalls: string[];
}

export interface AppealStep {
  stepNumber: number;
  title: string;
  description: string;
}

// Document types
export interface DocumentRequirement {
  id: number;
  grantId: number;
  scenario: string;
  documents: DocumentItem[];
}

export interface DocumentItem {
  id: string;
  name: string;
  description: string;
  isRequired: boolean;
  alternatives?: string[];
}

// FAQ types
export interface FAQ {
  id: number;
  grantId?: number;
  question: string;
  answer: string;
  displayOrder: number;
}

// AI types
export interface AIQuery {
  question: string;
}

export interface AIResponse {
  answer: string;
  // Legacy fields (optional for backward compatibility)
  whatThisMeans?: string;
  whyThisHappens?: string;
  whatYouCanDo?: string[];
  notes?: string;
  disclaimer?: string;
}

// Checklist types (localStorage only)
export interface ChecklistState {
  grantSlug: string;
  scenario: string;
  completedItems: string[];
  lastModified: string;
}
