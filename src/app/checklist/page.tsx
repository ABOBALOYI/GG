'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { getAllGrants } from '@/lib/data/grants';
import { getDocumentsByGrantSlug } from '@/lib/data/documents';
import type { DocumentItem, ChecklistState } from '@/lib/types';

const STORAGE_KEY = 'grantguide_checklist';

export default function ChecklistPage() {
  const [selectedGrant, setSelectedGrant] = useState<string>('');
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [completedItems, setCompletedItems] = useState<string[]>([]);
  const grants = getAllGrants();

  // Load saved state from localStorage
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const state: ChecklistState = JSON.parse(saved);
        setSelectedGrant(state.grantSlug);
        setCompletedItems(state.completedItems);
      } catch {
        // Invalid saved state, ignore
      }
    }

    // Check URL params for pre-selected grant
    const params = new URLSearchParams(window.location.search);
    const grantParam = params.get('grant');
    if (grantParam) {
      setSelectedGrant(grantParam);
    }
  }, []);

  // Update documents when grant changes
  useEffect(() => {
    if (selectedGrant) {
      const docs = getDocumentsByGrantSlug(selectedGrant);
      setDocuments(docs);
    } else {
      setDocuments([]);
    }
  }, [selectedGrant]);

  // Save state to localStorage
  useEffect(() => {
    if (selectedGrant) {
      const state: ChecklistState = {
        grantSlug: selectedGrant,
        scenario: 'first_time',
        completedItems,
        lastModified: new Date().toISOString()
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    }
  }, [selectedGrant, completedItems]);

  const toggleItem = (itemId: string) => {
    setCompletedItems(prev => 
      prev.includes(itemId) 
        ? prev.filter(id => id !== itemId)
        : [...prev, itemId]
    );
  };

  const resetChecklist = () => {
    setCompletedItems([]);
    localStorage.removeItem(STORAGE_KEY);
  };

  const completedCount = documents.filter(d => completedItems.includes(d.id)).length;
  const requiredCount = documents.filter(d => d.isRequired).length;
  const requiredCompleted = documents.filter(d => d.isRequired && completedItems.includes(d.id)).length;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">
        Document Checklist Generator
      </h1>
      <p className="text-gray-600 mb-8">
        Select your grant type to get a personalized checklist of documents you need. 
        Your progress is saved automatically in your browser.
      </p>

      {/* Grant Selection */}
      <section className="mb-8">
        <label htmlFor="grant-select" className="block text-sm font-medium text-gray-700 mb-2">
          Select Grant Type
        </label>
        <select
          id="grant-select"
          value={selectedGrant}
          onChange={(e) => {
            setSelectedGrant(e.target.value);
            setCompletedItems([]);
          }}
          className="w-full md:w-auto px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
        >
          <option value="">Choose a grant...</option>
          {grants.map((grant) => (
            <option key={grant.slug} value={grant.slug}>
              {grant.name}
            </option>
          ))}
        </select>
      </section>

      {/* Checklist */}
      {selectedGrant && documents.length > 0 && (
        <>
          {/* Progress */}
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-6">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">
                Progress: {completedCount} of {documents.length} documents
              </span>
              <span className="text-sm text-gray-500">
                Required: {requiredCompleted}/{requiredCount}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-green-600 h-2 rounded-full transition-all"
                style={{ width: `${(completedCount / documents.length) * 100}%` }}
              />
            </div>
          </div>

          {/* Document List */}
          <section className="space-y-3 mb-8">
            {documents.map((doc) => (
              <div 
                key={doc.id}
                className={`border rounded-lg p-4 transition-colors ${
                  completedItems.includes(doc.id) 
                    ? 'bg-green-50 border-green-200' 
                    : 'bg-white border-gray-200'
                }`}
              >
                <label className="flex items-start gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={completedItems.includes(doc.id)}
                    onChange={() => toggleItem(doc.id)}
                    className="mt-1 h-5 w-5 text-green-600 rounded border-gray-300 focus:ring-green-500"
                  />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className={`font-medium ${completedItems.includes(doc.id) ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                        {doc.name}
                      </span>
                      {doc.isRequired && (
                        <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded">
                          Required
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mt-1">{doc.description}</p>
                    {doc.alternatives && doc.alternatives.length > 0 && (
                      <p className="text-sm text-blue-600 mt-1">
                        Alternative: {doc.alternatives.join(' or ')}
                      </p>
                    )}
                  </div>
                </label>
              </div>
            ))}
          </section>

          {/* Actions */}
          <div className="flex flex-wrap gap-3">
            <button
              onClick={resetChecklist}
              className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Reset Checklist
            </button>
            <Link
              href={`/grants/${selectedGrant}`}
              className="px-4 py-2 text-green-700 border border-green-700 rounded-lg hover:bg-green-50 transition-colors"
            >
              View Grant Details
            </Link>
          </div>

          {/* Completion Message */}
          {requiredCompleted === requiredCount && requiredCount > 0 && (
            <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-4">
              <p className="text-green-800 font-medium">
                ✓ You have all required documents! You&apos;re ready to apply.
              </p>
              <p className="text-green-700 text-sm mt-1">
                Visit your nearest SASSA office with these documents to submit your application.
              </p>
            </div>
          )}
        </>
      )}

      {/* No Grant Selected */}
      {!selectedGrant && (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
          <p className="text-gray-600">
            Select a grant type above to see the required documents.
          </p>
        </div>
      )}

      {/* Privacy Note */}
      <section className="mt-8 text-sm text-gray-500">
        <p>
          <strong>Privacy:</strong> Your checklist progress is saved only in your browser (localStorage). 
          We do not store any of your information on our servers.
        </p>
      </section>
    </div>
  );
}
