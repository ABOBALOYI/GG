import { describe, it, expect } from 'vitest';
import {
  documentRequirements,
  getDocumentsForGrant,
  getDocumentsByGrantSlug,
} from './documents';

describe('Documents Data', () => {
  /**
   * **Feature: grantguide-sa, Property 9: Document Checklist Generation**
   * **Validates: Requirements 6.1, 6.2**
   * 
   * WHEN a user selects a grant type and scenario THEN the System SHALL 
   * generate a customized document checklist
   */
  it('Property 9: document requirements exist for each grant', () => {
    expect(documentRequirements.length).toBeGreaterThan(0);

    documentRequirements.forEach((req) => {
      expect(req.grantId).toBeDefined();
      expect(req.scenario).toBeTruthy();
      expect(Array.isArray(req.documents)).toBe(true);
      expect(req.documents.length).toBeGreaterThan(0);
    });
  });

  it('Property 9: each document has required fields', () => {
    documentRequirements.forEach((req) => {
      req.documents.forEach((doc) => {
        expect(doc.id).toBeTruthy();
        expect(doc.name).toBeTruthy();
        expect(doc.description).toBeTruthy();
        expect(typeof doc.isRequired).toBe('boolean');
      });
    });
  });

  it('Property 9: getDocumentsForGrant returns correct documents', () => {
    const docs = getDocumentsForGrant(1, 'first_time');

    expect(docs.length).toBeGreaterThan(0);
    docs.forEach((doc) => {
      expect(doc.id).toBeTruthy();
      expect(doc.name).toBeTruthy();
    });
  });

  it('Property 9: getDocumentsByGrantSlug works for known slugs', () => {
    const slugs = ['old-age-grant', 'child-support-grant', 'disability-grant'];

    slugs.forEach((slug) => {
      const docs = getDocumentsByGrantSlug(slug);
      expect(docs.length).toBeGreaterThan(0);
    });
  });

  it('Property 9: returns empty array for unknown grant', () => {
    const docs = getDocumentsByGrantSlug('unknown-grant');
    expect(docs).toEqual([]);
  });

  it('Property 9: ID document is required for all grants', () => {
    documentRequirements.forEach((req) => {
      const hasIdDoc = req.documents.some(
        (doc) => doc.id === 'id' && doc.isRequired
      );
      expect(hasIdDoc).toBe(true);
    });
  });

  it('Property 9: some documents have alternatives listed', () => {
    const allDocs = documentRequirements.flatMap((req) => req.documents);
    const docsWithAlternatives = allDocs.filter(
      (doc) => doc.alternatives && doc.alternatives.length > 0
    );

    expect(docsWithAlternatives.length).toBeGreaterThan(0);
  });
});
