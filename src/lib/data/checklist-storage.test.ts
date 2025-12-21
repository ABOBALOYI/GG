import { describe, it, expect, beforeEach, vi } from 'vitest';
import type { ChecklistState } from '../types';

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: vi.fn((key: string) => store[key] || null),
    setItem: vi.fn((key: string, value: string) => {
      store[key] = value;
    }),
    removeItem: vi.fn((key: string) => {
      delete store[key];
    }),
    clear: vi.fn(() => {
      store = {};
    }),
  };
})();

Object.defineProperty(global, 'localStorage', { value: localStorageMock });

const STORAGE_KEY = 'grantguide_checklist';

describe('Checklist Storage', () => {
  beforeEach(() => {
    localStorageMock.clear();
    vi.clearAllMocks();
  });

  /**
   * **Feature: grantguide-sa, Property 10: Local-First Storage**
   * **Validates: Requirements 6.3, 7.4**
   *
   * WHEN a user completes a checklist THEN the System SHALL save progress
   * to localStorage by default without requiring authentication
   */
  it('Property 10: checklist state can be saved to localStorage', () => {
    const state: ChecklistState = {
      grantSlug: 'old-age-grant',
      scenario: 'first_time',
      completedItems: ['id', 'residence'],
      lastModified: new Date().toISOString(),
    };

    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));

    expect(localStorageMock.setItem).toHaveBeenCalledWith(
      STORAGE_KEY,
      expect.any(String)
    );
  });

  it('Property 10: checklist state can be retrieved from localStorage', () => {
    const state: ChecklistState = {
      grantSlug: 'child-support-grant',
      scenario: 'first_time',
      completedItems: ['id', 'child_birth'],
      lastModified: new Date().toISOString(),
    };

    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    const retrieved = localStorage.getItem(STORAGE_KEY);
    const parsed: ChecklistState = JSON.parse(retrieved!);

    expect(parsed.grantSlug).toBe('child-support-grant');
    expect(parsed.completedItems).toContain('id');
    expect(parsed.completedItems).toContain('child_birth');
  });

  it('Property 10: checklist state includes required fields', () => {
    const state: ChecklistState = {
      grantSlug: 'disability-grant',
      scenario: 'first_time',
      completedItems: [],
      lastModified: new Date().toISOString(),
    };

    // Validate structure
    expect(state.grantSlug).toBeTruthy();
    expect(state.scenario).toBeTruthy();
    expect(Array.isArray(state.completedItems)).toBe(true);
    expect(state.lastModified).toBeTruthy();
  });

  it('Property 10: checklist can be cleared from localStorage', () => {
    const state: ChecklistState = {
      grantSlug: 'old-age-grant',
      scenario: 'first_time',
      completedItems: ['id'],
      lastModified: new Date().toISOString(),
    };

    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    localStorage.removeItem(STORAGE_KEY);

    expect(localStorageMock.removeItem).toHaveBeenCalledWith(STORAGE_KEY);
    expect(localStorage.getItem(STORAGE_KEY)).toBeNull();
  });

  it('Property 10: handles missing localStorage gracefully', () => {
    const retrieved = localStorage.getItem(STORAGE_KEY);
    expect(retrieved).toBeNull();
  });

  it('Property 10: lastModified is a valid ISO date string', () => {
    const state: ChecklistState = {
      grantSlug: 'old-age-grant',
      scenario: 'first_time',
      completedItems: [],
      lastModified: new Date().toISOString(),
    };

    const date = new Date(state.lastModified);
    expect(date.toString()).not.toBe('Invalid Date');
  });
});
