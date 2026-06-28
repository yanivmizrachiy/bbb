import path from "node:path";
import { drizzle as drizzlePg } from "drizzle-orm/node-postgres";
import { drizzle as drizzlePglite } from "drizzle-orm/pglite";
import { Pool } from "pg";
import { PGlite } from "@electric-sql/pglite";
import * as schema from "./schema";

const url = process.env.DATABASE_URL ?? "";

/** Use a real Postgres server when DATABASE_URL points to one (docker / hosted);
 *  otherwise fall back to embedded PGlite (real Postgres, zero setup). */
export const usingServer = /^postgres(ql)?:\/\//.test(url);
export const pgliteDir =
  process.env.PGLITE_DIR ?? path.join(process.cwd(), ".pgdata");

type DB = ReturnType<typeof drizzlePglite<typeof schema>>;

// Reuse one client/connection across dev hot-reloads.
const g = globalThis as unknown as {
  _db?: DB;
  _pglite?: PGlite;
  _pool?: Pool;
};

function build(): DB {
  if (usingServer) {
    const pool = g._pool ?? new Pool({ connectionString: url });
    g._pool = pool;
    // The query-builder API is identical across drivers; cast keeps one type.
    return drizzlePg(pool, { schema }) as unknown as DB;
  }
  const client = g._pglite ?? new PGlite(pgliteDir);
  g._pglite = client;
  return drizzlePglite(client, { schema });
}

export const db: DB = g._db ?? build();
if (process.env.NODE_ENV !== "production") g._db = db;

export async function closeDb() {
  if (g._pglite) await g._pglite.close();
  if (g._pool) await g._pool.end();
}
