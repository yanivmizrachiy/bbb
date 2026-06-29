import path from "node:path";
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import * as schema from "./schema";

// Accept a Postgres URL from DATABASE_URL or from the vars Vercel Postgres /
// Neon inject automatically — so attaching a DB in the dashboard needs zero
// manual env config.
const url =
  process.env.DATABASE_URL ??
  process.env.POSTGRES_URL ??
  process.env.POSTGRES_PRISMA_URL ??
  "";

/** True when a real Postgres server is configured. When false, the app serves
 *  the committed build-time snapshot (see db/data.ts) and this client is unused. */
export const usingServer = /^postgres(ql)?:\/\//.test(url);

type DB = ReturnType<typeof drizzle<typeof schema>>;

// Reuse one pool/connection across dev hot-reloads.
const g = globalThis as unknown as { _db?: DB; _pool?: Pool };

function build(): DB {
  if (!usingServer)
    throw new Error(
      "No Postgres server configured (set DATABASE_URL/POSTGRES_URL). " +
        "Without one the app reads the committed snapshot via db/data.ts; " +
        "the db client is only for a real server (seed/migrate).",
    );
  const pool = g._pool ?? new Pool({ connectionString: url });
  g._pool = pool;
  return drizzle(pool, { schema });
}

function getDb(): DB {
  if (!g._db) g._db = build();
  return g._db;
}

// Lazy proxy: the pool initializes on first *use*, not at import — so build-time
// module analysis never opens a database connection.
export const db: DB = new Proxy({} as DB, {
  get(_t, prop) {
    const real = getDb() as unknown as Record<string | symbol, unknown>;
    const v = real[prop];
    return typeof v === "function" ? (v as (...a: unknown[]) => unknown).bind(real) : v;
  },
});

export async function closeDb() {
  if (g._pool) await g._pool.end();
}

/** Apply versioned Drizzle migrations (server Postgres only). */
export async function migrateDb() {
  const folder = path.join(process.cwd(), "db", "migrations");
  const { migrate } = await import("drizzle-orm/node-postgres/migrator");
  await migrate(getDb() as never, { migrationsFolder: folder });
}
