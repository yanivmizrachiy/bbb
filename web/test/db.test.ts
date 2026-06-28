import { describe, it, expect, beforeAll, afterAll } from "vitest";
import path from "node:path";
import { PGlite } from "@electric-sql/pglite";
import { drizzle } from "drizzle-orm/pglite";
import { migrate } from "drizzle-orm/pglite/migrator";
import { eq } from "drizzle-orm";
import { subjects, chapters } from "../db/schema";

// Spins up a real PostgreSQL engine in-memory (PGlite), applies the actual
// migrations, and round-trips rows — proving the schema + queries for real.
describe("schema + queries on real Postgres (in-memory PGlite)", () => {
  let client: PGlite;
  let db: ReturnType<typeof drizzle>;

  beforeAll(async () => {
    client = new PGlite();
    db = drizzle(client, { schema: { subjects, chapters } });
    await migrate(db, {
      migrationsFolder: path.join(process.cwd(), "db", "migrations"),
    });
  });

  afterAll(async () => {
    await client.close();
  });

  it("migrates and round-trips a subject + its chapters", async () => {
    await db.insert(subjects).values({
      key: "geometry8",
      title: "גאומטריה לכיתה ח'",
      subtitle: "מעגל",
      icon: "△",
      color: "#0d9488",
      orbLight: "#38bdf8",
      orbDeep: "#0284c7",
      questions: 55,
      chapters: 14,
      pages: 34,
      pdf: "x.pdf",
      sort: 3,
    });
    await db.insert(chapters).values([
      { subjectKey: "geometry8", idx: 0, letter: "א", title: "המעגל וחלקיו", color: "#4f46e5", page: 2 },
      { subjectKey: "geometry8", idx: 1, letter: "ב", title: "היקף", color: "#0d9488", page: 4 },
    ]);

    const got = await db.select().from(subjects).where(eq(subjects.key, "geometry8"));
    expect(got).toHaveLength(1);
    expect(got[0].questions).toBe(55);

    const ch = await db
      .select()
      .from(chapters)
      .where(eq(chapters.subjectKey, "geometry8"));
    expect(ch).toHaveLength(2);
    expect(ch[0].title).toBe("המעגל וחלקיו");
  });

  it("enforces the unique constraint on subject key", async () => {
    await expect(
      db.insert(subjects).values({
        key: "geometry8",
        title: "dup",
        subtitle: "",
        icon: "△",
        color: "#000",
        orbLight: "#000",
        orbDeep: "#000",
        questions: 1,
        chapters: 1,
        pages: 1,
        pdf: "y.pdf",
        sort: 9,
      }),
    ).rejects.toThrow();
  });
});
