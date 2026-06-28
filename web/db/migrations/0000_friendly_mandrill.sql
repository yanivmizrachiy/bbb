CREATE TABLE "chapters" (
	"id" serial PRIMARY KEY NOT NULL,
	"subject_key" text NOT NULL,
	"idx" integer NOT NULL,
	"letter" text NOT NULL,
	"title" text NOT NULL,
	"color" text NOT NULL,
	"page" integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE "subjects" (
	"id" serial PRIMARY KEY NOT NULL,
	"key" text NOT NULL,
	"title" text NOT NULL,
	"subtitle" text NOT NULL,
	"icon" text NOT NULL,
	"color" text NOT NULL,
	"orb_light" text NOT NULL,
	"orb_deep" text NOT NULL,
	"questions" integer NOT NULL,
	"chapters" integer NOT NULL,
	"pages" integer NOT NULL,
	"pdf" text NOT NULL,
	"sort" integer DEFAULT 0 NOT NULL,
	CONSTRAINT "subjects_key_unique" UNIQUE("key")
);
