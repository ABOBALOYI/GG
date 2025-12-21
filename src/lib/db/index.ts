import { createClient } from '@libsql/client';

// For local development, use a local SQLite file
// For production, use Turso cloud database
const db = createClient({
  url: process.env.TURSO_DATABASE_URL || 'file:local.db',
  authToken: process.env.TURSO_AUTH_TOKEN,
});

export default db;

// Helper to parse JSON fields from database
export function parseJsonField<T>(value: string | null): T | null {
  if (!value) return null;
  try {
    return JSON.parse(value) as T;
  } catch {
    return null;
  }
}
