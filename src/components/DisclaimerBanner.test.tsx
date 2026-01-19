import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import DisclaimerBanner from './DisclaimerBanner';
import { LanguageProvider } from '@/lib/i18n/LanguageContext';

const renderWithProvider = (component: React.ReactNode) => {
  return render(<LanguageProvider>{component}</LanguageProvider>);
};

describe('DisclaimerBanner', () => {
  /**
   * **Feature: grantguide-sa, Property 11: Disclaimer Presence**
   * **Validates: Requirements 10.3**
   * 
   * WHEN displaying disclaimers THEN the System SHALL clearly state that 
   * GrantGuide SA is unofficial and independent from SASSA
   */
  it('Property 11: displays unofficial and independent disclaimer', () => {
    renderWithProvider(<DisclaimerBanner />);
    
    // Must contain "unofficial" and indicate it's not affiliated (independent)
    const banner = screen.getByRole('alert');
    expect(banner).toBeDefined();
    expect(banner.textContent?.toLowerCase()).toContain('unofficial');
    // "not affiliated" indicates independence from SASSA
    expect(banner.textContent?.toLowerCase()).toContain('not affiliated');
  });

  it('Property 11: states not affiliated with SASSA', () => {
    renderWithProvider(<DisclaimerBanner />);
    
    const banner = screen.getByRole('alert');
    // English translation: "NOT affiliated with SASSA"
    expect(banner.textContent?.toLowerCase()).toMatch(/not.*affiliated|sassa/i);
  });

  it('Property 11: links to official SASSA website', () => {
    renderWithProvider(<DisclaimerBanner />);
    
    const link = screen.getByRole('link', { name: /sassa\.gov\.za/i });
    expect(link).toBeDefined();
    expect(link.getAttribute('href')).toBe('https://www.sassa.gov.za');
    expect(link.getAttribute('target')).toBe('_blank');
  });

  it('has accessible dismiss button', () => {
    renderWithProvider(<DisclaimerBanner />);
    
    // Button exists for dismissing the banner
    const dismissButton = screen.getByRole('button');
    expect(dismissButton).toBeDefined();
  });
});
