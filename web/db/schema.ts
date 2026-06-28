import { pgTable, serial, text, integer, real } from "drizzle-orm/pg-core";

/** One row per subject (נושא) — the catalog that drives the home page. */
export const subjects = pgTable("subjects", {
  id: serial("id").primaryKey(),
  key: text("key").notNull().unique(),
  title: text("title").notNull(),
  subtitle: text("subtitle").notNull(),
  icon: text("icon").notNull(),
  color: text("color").notNull(),
  orbLight: text("orb_light").notNull(),
  orbDeep: text("orb_deep").notNull(),
  questions: integer("questions").notNull(),
  chapters: integer("chapters").notNull(),
  pages: integer("pages").notNull(),
  pdf: text("pdf").notNull(),
  sort: integer("sort").notNull().default(0),
});

/** One row per chapter (פרק) within a subject — drives chapter navigation. */
export const chapters = pgTable("chapters", {
  id: serial("id").primaryKey(),
  subjectKey: text("subject_key").notNull(),
  idx: integer("idx").notNull(),
  letter: text("letter").notNull(),
  title: text("title").notNull(),
  color: text("color").notNull(),
  page: integer("page").notNull(),
  // Clickable hotspot rect (% of the cover image), parsed from viewer.html.
  hotLeft: real("hot_left"),
  hotTop: real("hot_top"),
  hotWidth: real("hot_width"),
  hotHeight: real("hot_height"),
});

export type Subject = typeof subjects.$inferSelect;
export type NewSubject = typeof subjects.$inferInsert;
export type Chapter = typeof chapters.$inferSelect;
export type NewChapter = typeof chapters.$inferInsert;
